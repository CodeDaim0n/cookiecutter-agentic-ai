import json
import logging
from typing import Any
from jinja2 import Template
from pydantic import create_model, BaseModel, Field
from langchain_core.runnables import Runnable
from langchain_core.runnables.base import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.common.utils.config import load_json_config
from tools.common.utils.tool_loader import load_native_tools_from_config
from tools.common.utils.tool_wrappers import parse_type

logger = logging.getLogger("{{ cookiecutter.project_name }}_react_agent")
logging.basicConfig(level=logging.INFO)

class LoggingWrapper(Runnable):
    def __init__(self, wrapped_model: Runnable):
        self.wrapped = wrapped_model

    def invoke(self, input: Any, config: RunnableConfig = None) -> Any:
        response = self.wrapped.invoke(input, config)
        logger.info("🧠 [OpenAI] Raw model output:")
        try:
            logger.info(json.dumps(response.model_dump(), indent=2))
        except Exception:
            logger.info(str(response))
        return response

    def __getattr__(self, name):
        return getattr(self.wrapped, name)

def build_dynamic_state_schema(tool_names, tools_config):
    all_fields = {
        "messages": (list, Field(default_factory=list)),
        "remaining_steps": (int, Field(default=5))
    }
    for tool_def in tools_config["tools"]:
        if tool_def["name"] in tool_names:
            for field, typ in tool_def.get("input_schema", {}).items():
                if field not in all_fields:
                    all_fields[field] = (parse_type(typ), Field(...))
    return create_model("AgentState", **all_fields, __base__=BaseModel)

def extract_output_schema(tool_names, tools_config):
    merged_structure = {}
    for tool_def in tools_config["tools"]:
        if tool_def["name"] in tool_names:
            structure = tool_def.get("output_schema", {}).get("structure", {})
            merged_structure[tool_def["name"]] = structure
    return json.dumps(merged_structure, indent=2)

def create_configured_react_agent(agent_name: str, context: dict = None):
    tools_config = load_json_config("config/tools.json")
    openai_config = load_json_config("config/openai_config.json")
    nodes_config = load_json_config("config/nodes.json").get("nodes", [])

    agent_node = next((n for n in nodes_config if n["id"] == agent_name), None)
    if not agent_node or agent_node.get("type") != "react_agent":
        raise ValueError(f"'{agent_name}' is not a valid react_agent in nodes.json")

    agent_cfg = agent_node
    prompt_cfg = openai_config.get(agent_name)
    if not prompt_cfg:
        raise ValueError(f"No config found for agent '{agent_name}' in openai_config.json")

    tool_names = agent_cfg.get("tools", [])
    output_schema = extract_output_schema(tool_names, tools_config)
    agent_output_schema = extract_output_schema([agent_name], tools_config)

    context = context or {}
    context["expected_output_schema"] = output_schema
    context["agent_output_schema"] = agent_output_schema

    raw_prompt = prompt_cfg.get("prompt") or prompt_cfg.get("input_template", "You are a helpful assistant.")
    rendered_prompt = Template(raw_prompt).render(**context)

    model = LoggingWrapper(ChatOpenAI(model=prompt_cfg.get("model", "gpt-4o-mini"), temperature=prompt_cfg.get("temperature", 0.3), use_responses_api=True))

    native_tools = load_native_tools_from_config("config/tools.json")
    tools = [native_tools[t] for t in tool_names if t in native_tools]

    return create_react_agent(model=model, tools=tools, prompt=rendered_prompt)
