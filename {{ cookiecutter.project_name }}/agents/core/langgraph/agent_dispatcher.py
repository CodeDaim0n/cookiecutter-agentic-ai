import json
import os
from agents.core.langgraph.react_agent_builder import create_configured_react_agent
from agents.core.langgraph.supervisor_agent_builder import create_supervisor_agent
from utils.config import load_json_config
from utils.logger import log_agent_event
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()

NODES_CONFIG_PATH = "config/nodes.json"
nodes_config = load_json_config(NODES_CONFIG_PATH).get("nodes", [])
AGENT_TYPE_MAP = {
    node["id"]: node["type"]
    for node in nodes_config
    if node["type"] in {"react_agent", "supervisor"}
}

logger = logging.getLogger("{{ cookiecutter.project_name }}_agent_dispatch")
logger.setLevel(logging.INFO)

def agent_dispatch(agent_name: str, message: str, context: dict = {}) -> dict:
    '''
    Dispatch an agent based on the agent name and message.
    '''
    start_time = datetime.utcnow()

    if not agent_name or not message:
        return {"error": "Missing required field (agent_name, message)"}

    context.update({
        "message": message,
        "identifier": context.get("identifier"),
    })

    logger.info(f"[agent_dispatch] Dispatching {agent_name} for identifier: {context.get('identifier')}")
    agent_type = AGENT_TYPE_MAP.get(agent_name)

    if not agent_type:
        return {"error": f"Unknown agent or type for '{agent_name}'"}

    try:
        if agent_type == "react_agent":
            agent = create_configured_react_agent(agent_name, context)
        elif agent_type == "supervisor":
            agent = create_supervisor_agent(agent_name, context)
        else:
            return {"error": f"Unsupported agent type: {agent_type}"}

        initial_state = {
            "messages": [{"role": "user", "content": message}],
            **context
        }

        output = agent.invoke(initial_state, config={"configurable": context})

    except Exception as e:
        output = {"error": str(e)}
    finally:
        end_time = datetime.utcnow()
        try:
            log_agent_event(
                agent_name=agent_name,
                message=message,
                context=json.loads(json.dumps(context, default=str)),
                output={
                    "request": json.loads(json.dumps(initial_state, default=str)),
                    "response": json.loads(json.dumps(output, default=str))
                },
                start_time=start_time,
                end_time=end_time
            )
        except Exception as log_err:
            logger.error(f"[agent_dispatch] Logging failed: {log_err}")

    return output
