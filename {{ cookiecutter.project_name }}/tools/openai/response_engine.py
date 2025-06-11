from langchain_openai import ChatOpenAI
import json
from jinja2 import Template
import os
from dotenv import load_dotenv
load_dotenv()


class OpenAIResponder:
    def __init__(self, config_path="config/openai_config.json", tools_path="config/tools.json"):
        self.config = self._load_config(config_path)
        self.tools = self._load_config(tools_path)

    def _load_config(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def render_template(self, template_str: str, variables: dict) -> str:
        template = Template(template_str)
        return template.render(**variables)

    def get_tool_schema(self, tool_name: str) -> dict:
        for tool in self.tools.get("tools", []):
            func_name = tool.get("function", "")
            if func_name.split(".")[-1] == tool_name:
                raw_schema = tool.get("output_schema", {})
                if "structure" in raw_schema:
                    flattened = raw_schema["structure"]
                    if isinstance(flattened, dict) and "output" in flattened:
                        output_fields = flattened["output"]
                        explanation_field = {"explanation": "string"} if "explanation" in flattened else {}
                        return {"output": output_fields, **explanation_field}
                    return flattened
                return raw_schema
        return {}

    

    def run(self, tool_name: str, variables=None, vector_store_ids=None) -> dict:
        print("\n🛠️ [DEBUG] inside run:")
        cfg = self.config.get(tool_name)
        if not cfg:
            raise ValueError(f"Tool '{tool_name}' not found in config")

        variables = variables or {}
        
        print("\n🔍 [DEBUG] Tool:", tool_name)
        for k, v in variables.items():
            print(f"   {k}: ({type(v).__name__}) {repr(v)[:300]}")

        
        # Schema injection for debugging context
        output_schema = self.get_tool_schema(tool_name)
        variables["expected_output_schema"] = json.dumps(output_schema, indent=2) if output_schema else ""

        # Prompt rendering
        input_text = self.render_template(cfg["input_template"], variables)
        if not isinstance(input_text, str):
            input_text = str(input_text)

        print("\n📝 [DEBUG] Rendered Prompt:\n", input_text[:1000])

        model_name = cfg.get("model", "gpt-4o-mini")
        tools = cfg.get("tools", [])
        print("\n🛠️ [DEBUG] Tools to Pass:", json.dumps(tools, indent=2))

        if vector_store_ids:
            for tool in tools:
                if isinstance(tool, dict) and tool.get("type") == "file_search":
                    tool["vector_store_ids"] = vector_store_ids
        print("\n🛠️ [DEBUG] before llm:")
        llm = ChatOpenAI(model=model_name, temperature=0.3, use_responses_api=True)
        config = {"tools": tools}
        config["tool_choice"] = cfg.get("tool_choice")
        llm_with_tools = llm.bind_tools(tools)
        print("\n🛠️ [DEBUG] after Tools to Pass:", json.dumps(tools, indent=2))
        response = llm_with_tools.invoke([{"role": "user", "content": input_text}], config=config)

        print("\n✅ [DEBUG] Raw response content:", response.content)

        # Extract fallback or structured content
        if isinstance(response.content, list):
            for part in response.content:
                if isinstance(part, dict) and part.get("type") == "text":
                    return {"output": {"fallback_message": part["text"]}}
            return {"output": {"fallback_message": str(response.content)}}
        elif hasattr(response, "content"):
            return {"output": {"fallback_message": response.content}}
        else:
            return {"output": {"fallback_message": str(response)}}
