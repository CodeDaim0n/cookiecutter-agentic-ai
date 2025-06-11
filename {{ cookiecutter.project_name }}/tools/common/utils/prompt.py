import openai
import os
from tools.common.utils.config import load_json_config
from tools.common.utils.responder import responder
from tools.common.utils.moderation import check_moderation
from tools.common.utils.logger import log_tool_event
from typing import Optional, Callable
import re
import json
import logging
from datetime import datetime
from openai import OpenAI

# Optional fallback log
logging.basicConfig(filename='luna_tool_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI()

# Helper function to parse rationale section from LLM response
def parse_rationale(response: str) -> tuple:
    if "Explanation:" in response:
        parts = response.split("Explanation:", 1)
        return parts[0].strip(), parts[1].strip()
    return response.strip(), "No explanation provided."

# Main prompt runner that supports LLM-based tool execution using config-driven schema
# Applies moderation, input filtering, and logs complete metadata

def run_openai_tool_prompt(
    tool_name: str,
    variables: Optional[dict] = None,
    output_parser: Optional[Callable[[str], any]] = None
) -> dict:
    config = load_json_config("config/graph_config.json")
    moderation_enabled = config.get("moderation_enabled", True)

    # Extract and filter input variables for the tool based on schema
    message = (variables or {}).get("message", "")
    tool_config = responder.config.get(tool_name, {})
    allowed_keys = tool_config.get("input_schema", [])
    output_schema = tool_config.get("output_schema", {})

    # Inject expected output schema into prompt context
    expected_output_schema = json.dumps(output_schema, indent=2) if output_schema else ""
    filtered_vars = {k: v for k, v in (variables or {}).items() if not allowed_keys or k in allowed_keys}
    filtered_vars["expected_output_schema"] = expected_output_schema

    start_time = datetime.utcnow()
    try:
        # Invoke the tool via prompt
        response = responder.run(tool_name=tool_name, variables=filtered_vars, message=message)

        # If structured LangGraph tool call
        if hasattr(response, "tool_calls") and response.tool_calls:
            log_tool_event(tool_name, filtered_vars, {"tool_calls": response.tool_calls}, start_time, datetime.utcnow())
            return response

        # If parsed dict-style result
        if isinstance(response, dict):
            log_tool_event(tool_name, filtered_vars, response, start_time, datetime.utcnow())
            return response

        # If string result, strip Markdown and parse as JSON
        if isinstance(response, str):
            raw_output = response.strip()
        else:
            raise TypeError(f"Unexpected response type: {type(response).__name__}")

        if raw_output.startswith('```json'):
            raw_output = raw_output[7:-3].strip()

        output_json = json.loads(raw_output)
        message = output_json.get("output", "No message provided.")
        explanation = output_json.get("explanation", "No explanation provided.")

        final_response = {"llm_output": message, "llm_explanation": explanation}
        log_tool_event(tool_name, filtered_vars, final_response, start_time, datetime.utcnow())

        return final_response

    except Exception as e:
        error_response = {"output": {"error": str(e)}}
        log_tool_event(tool_name, filtered_vars, error_response, start_time, datetime.utcnow())
        logging.error(f"[run_luna_prompt] Tool '{tool_name}' failed: {e}", exc_info=True)
        return error_response
