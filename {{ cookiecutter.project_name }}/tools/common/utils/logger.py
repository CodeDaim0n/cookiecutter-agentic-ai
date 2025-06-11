import logging
import json
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name: str, filename: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(LOG_DIR / filename, mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

tool_logger = setup_logger("tool_logger", "tool_logs.jsonl")
agent_logger = setup_logger("agent_logger", "agent_logs.jsonl")

def log_tool_event(tool_name: str, request: dict, response: dict, start_time: datetime, end_time: datetime):
    log_entry = {
        "type": "tool",
        "tool_name": tool_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": (end_time - start_time).total_seconds(),
        "request": request,
        "response": response
    }
    tool_logger.info(json.dumps(log_entry, ensure_ascii=False))

def log_agent_event(agent_name: str, message: str, context: dict, output: dict, start_time: datetime, end_time: datetime):
    log_entry = {
        "type": "agent",
        "agent_name": agent_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": (end_time - start_time).total_seconds(),
        "message": message,
        "context": context,
        "output": output
    }
    agent_logger.info(json.dumps(log_entry, ensure_ascii=False))
