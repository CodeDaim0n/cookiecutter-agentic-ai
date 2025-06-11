import importlib
import logging
from typing import Callable, Dict
from langchain_core.tools import StructuredTool
from tools.common.utils.config import load_json_config

logger = logging.getLogger("tool_loader")


def import_from_path(path: str) -> Callable:
    """
    Import a function from a string path like 'tools.luna.planner.plan_day.plan_day'
    """
    module_path, func_name = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


def load_native_tools_from_config(config_path: str) -> Dict[str, StructuredTool]:
    """
    Load and wrap tool functions using import paths in tools.json as StructuredTool instances.
    """
    config = load_json_config(config_path)
    tools = {}

    for tool_def in config.get("tools", []):
        name = tool_def.get("name")
        function_path = tool_def.get("function")

        if not name or not function_path:
            logger.warning(f"Skipping invalid tool definition: {tool_def}")
            continue

        try:
            raw_fn = import_from_path(function_path)
            wrapped_tool = StructuredTool.from_function(raw_fn)
            tools[name] = wrapped_tool
            logger.info(f"✅ Loaded and wrapped native tool: {name} → {function_path}")
        except Exception as e:
            logger.error(f"❌ Failed to import or wrap tool '{name}': {e}")

    return tools
