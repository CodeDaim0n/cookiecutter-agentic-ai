import importlib
import logging
import pprint
from typing import Any, Dict, Callable
from pydantic import create_model, Field, BaseModel
from langchain_core.runnables.config import RunnableConfig

logger = logging.getLogger("tool_wrappers")
logger.setLevel(logging.INFO)


def parse_type(type_str: Any) -> type:
    if isinstance(type_str, str):
        return {
            "str": str,
            "string": str,
            "int": int,
            "integer": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "object": dict,
        }.get(type_str.lower(), Any)
    return Any


def generate_tool_wrapper(name: str, func: Callable, input_schema: Any, output_schema: Dict[str, Any]) -> Callable:
    logger.debug(f"Generating tool wrapper for: {name}")

    # Input model
    input_fields = {}
    if isinstance(input_schema, list):
        logger.warning(f"Tool '{name}' uses list-style input_schema; defaulting all fields to str")
        input_fields = {field_name: (str, Field(..., description=field_name)) for field_name in input_schema}
    elif isinstance(input_schema, dict):
        input_fields = {
            k: (parse_type(v), Field(..., description=k))
            for k, v in input_schema.items()
        }
    else:
        raise ValueError(f"Unsupported input_schema type for tool '{name}': {type(input_schema)}")

    InputModel = create_model(f"{name}_Input", **input_fields, __base__=BaseModel)
    InputModel.__doc__ = f"Input model for {name}"

    # Output model
    output_fields = {
        k: (parse_type(v), Field(..., description=k))
        for k, v in output_schema.get("structure", {}).items()
    }
    OutputModel = create_model(f"{name}_Output", **output_fields, __base__=BaseModel)
    OutputModel.__doc__ = f"Output model for {name}"

    def tool_wrapper(config: RunnableConfig, **kwargs):
        log_prefix = f"[{name}]"
        call_config = config.get("configurable", {})

        # Use OpenAI-generated call_id if available
        openai_call_id = config.get("call_id", f"{name}_default_fallback")

        try:
            logger.info(f"{log_prefix} ✅ CONFIG BEFORE TOOL EXECUTION:\n{pprint.pformat(call_config, indent=2)}")

            validated_input = InputModel(**call_config)
            logger.info(f"{log_prefix} 🔍 Tool input validated: {validated_input.dict()}")

            result = func(**validated_input.dict())
            logger.info(f"{log_prefix} 🧪 Raw result: {result}")

            validated_output = OutputModel(**result)
            logger.info(f"{log_prefix} 🛠️ TOOL VALIDATED OUTPUT:\n{pprint.pformat(validated_output.dict(), indent=2)}")

            return {
                "type": "function_call_output",
                "call_id": openai_call_id,
                "output": validated_output.dict()
            }

        except Exception as e:
            logger.error(f"{log_prefix} ❌ Tool execution failed: {e}", exc_info=True)
            fallback = {
                key: None for key in output_schema.get("structure", {}).keys()
            }
            return {
                "type": "function_call_output",
                "call_id": openai_call_id,
                "output": fallback
            }

    tool_wrapper.__name__ = name
    tool_wrapper.__doc__ = func.__doc__ or f"Tool wrapper for {name}"
    tool_wrapper.__annotations__ = {
        "config": RunnableConfig,
        "return": OutputModel
    }

    return tool_wrapper


def load_tools_from_config(config_path: str) -> Dict[str, Callable]:
    logger.info(f"📦 Loading tools from config: {config_path}")
    import json
    with open(config_path, "r") as f:
        config = json.load(f)["tools"]

    loaded_tools = {}
    for tool_def in config:
        logger.debug(f"Processing tool: {tool_def['name']}")
        module_path, func_name = tool_def["function"].rsplit(".", 1)
        mod = importlib.import_module(module_path)
        func = getattr(mod, func_name)

        wrapped = generate_tool_wrapper(
            name=tool_def["name"],
            func=func,
            input_schema=tool_def.get("input_schema", {}),
            output_schema=tool_def.get("output_schema", {})
        )
        loaded_tools[tool_def["name"]] = wrapped
        logger.info(f"✅ Wrapped tool: {tool_def['name']} → {tool_def['function']}")

    return loaded_tools
