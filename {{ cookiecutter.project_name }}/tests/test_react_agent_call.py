from agents.core.langgraph.agent_dispatcher import agent_dispatch
import logging
logging.basicConfig(level=logging.DEBUG)

response = agent_dispatch(
    agent_name="{{ cookiecutter.agent_one_name }}",
    message="give me some resources for my interview preparation",
    identifier=2
 )

print("\n✅ Final Output:\n", response)

