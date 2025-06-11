import json
import logging
from typing import Any, Dict
from jinja2 import Template
from pydantic import create_model
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from langgraph_supervisor import create_supervisor
from tools.common.utils.config import load_json_config
from tools.common.utils.tool_loader import load_native_tools_from_config
from agents.core.langgraph.react_agent_builder import create_configured_react_agent

logger = logging.getLogger("{{ cookiecutter.project_name }}_supervisor_builder")
logging.basicConfig(level=logging.INFO)

class LoggingWrapper(Runnable):
    def __init__(self, wrapped_model: Runnable):
        self.wrapped = wrapped_model

    def invoke(self, input: Any, config=None) -> Any:
        response = self.wrapped.invoke(input, config)
        logger.info("🧠 [OpenAI] Raw model output:")
        try:
            logger.info(json.dumps(response.model_dump(), indent=2))
        except Exception:
            logger.info(str(response))
        return response

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


def extract_output_schema(tool_names, tools_config) -> str:
    merged: Dict[str, dict] = {}
    for tool_def in tools_config["tools"]:
        name = tool_def["name"]
        if name not in tool_names:
            continue
        struct = tool_def.get("output_schema", {}).get("structure", {})
        merged[name] = struct
    return json.dumps(merged, indent=2)


def create_supervisor_agent(agent_name: str, context: dict = None):
    tools_config = load_json_config("config/tools.json")
    openai_config = load_json_config("config/openai_config.json")
    nodes_config = load_json_config("config/nodes.json").get("nodes", [])

    agent_node = next((n for n in nodes_config if n["id"] == agent_name), None)
    if not agent_node or agent_node.get("type") != "supervisor":
        raise ValueError(f"'{agent_name}' is not a valid supervisor in nodes.json")

    prompt_cfg = openai_config.get(agent_name)
    tool_names = agent_node.get("tools", [])
    agent_output_schema = extract_output_schema([agent_name], tools_config)
    output_schema = extract_output_schema(tool_names, tools_config)

    context = context or {}
    if "message" in context:
        context["user_input"] = context["message"]
    if "customer_id" in context:
        context["user_id"] = context["customer_id"]
    context["expected_output_schema"] = output_schema
    context["agent_output_schema"] = agent_output_schema

    rendered_prompt = Template(prompt_cfg.get("prompt") or prompt_cfg.get("input_template", "")).render(**context)

    native_tools = load_native_tools_from_config("config/tools.json")
    tools = [native_tools[t] for t in tool_names if t in native_tools]

    model = LoggingWrapper(ChatOpenAI(
        model=prompt_cfg.get("model", "gpt-4o-mini"),
        temperature=prompt_cfg.get("temperature", 0.3),
        use_responses_api=True
    ))

    from pydantic import create_model
    agent_schema_map = json.loads(agent_output_schema)
    json_schema_obj = agent_schema_map.get(agent_name, {})
    props = json_schema_obj.get("properties", {})
    required_fields = set(json_schema_obj.get("required", []))
    from typing import Any as _Any
    pydantic_fields = {}
    for field_name, subschema in props.items():
        ttype = subschema.get("type")
        pytype = str if ttype == "string" else bool if ttype == "boolean" else int if ttype == "integer" else list if ttype == "array" else dict if ttype == "object" else _Any
        default = ... if field_name in required_fields else None
        pydantic_fields[field_name] = (pytype, default)

    SupervisorOutput = create_model(f"{agent_name}Output", **pydantic_fields)
    full_agent_schema = SupervisorOutput.schema()

    sub_agents = []
    for sub_agent_id in agent_node.get("agents", []):
        sub_agent = create_configured_react_agent(sub_agent_id, context)
        sub_agent.name = sub_agent_id
        sub_agents.append(sub_agent)

    from langgraph.prebuilt.chat_agent_executor import AgentStateWithStructuredResponse

    return create_supervisor(
        agents=sub_agents,
        model=model,
        tools=tools,
        prompt=rendered_prompt,
        response_format=(rendered_prompt, full_agent_schema),
        parallel_tool_calls=True,
        supervisor_name=agent_name,
        output_mode="last_message",
        add_handoff_messages=True,
        add_handoff_back_messages=True,
        state_schema=AgentStateWithStructuredResponse
    ).compile()
