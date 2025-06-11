from agents.core.langgraph.supervisor_agent_builder import create_configured_supervisor

agent = create_configured_supervisor("{{ cookiecutter.supervisor_name }}")
result = agent.invoke({"message": "I'm overwhelmed", "identifier": "2"})

print(result)
