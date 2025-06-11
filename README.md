# Agentic AI Template

A powerful template for creating agentic AI systems with multiple agents, tools, and a web interface. Developed by Anjali Jain.

## Features

* Multiple AI agents with different capabilities
* Supervisor agent for intelligent routing and coordination
* Customizable tools for each agent
* Web interface built with FastAPI
* Seamless OpenAI integration with function calling
* Structured project layout and type-hinted code
* Comprehensive logging and monitoring

## 🔍 Differentiation from Traditional LangGraph

While this template leverages the core LangGraph framework for agent orchestration, it extends and enhances the standard LangGraph approach in several important ways:

1. **Automated Project Scaffold**
   Uses Cookiecutter to generate a fully scaffolded project—with directories, config files, tool stubs, logging setup, and a FastAPI interface—so you don’t start from a blank LangGraph codebase.

2. **Supervisor Agent Layer**
   Implements a dedicated supervisor agent to automatically route user requests to specialized worker agents. Traditional LangGraph examples often demonstrate single-agent chains or uncoordinated tool use without a routing layer.

3. **Schema-Driven Tool Registry**
   Tools are declared in `config/tools.json` with clear input/output schemas. LangGraph by itself requires manual registration of each function and custom prompt crafting for tool calls.

4. **Out‑of‑the‑Box Web Interface**
   Ships with a REST API endpoint (`/api/agent`) and an HTML testing UI. Standard LangGraph demos are typically code-driven notebooks or scripts without a user-facing layer.

5. **Opinionated Logging & Monitoring**
   Preconfigured JSONL logs for agent actions and tool invocations—ensuring observability from day one. LangGraph leaves logging implementation entirely up to the developer.

6. **Developer Experience Enhancements**

   * Type-hinted stubs and auto-generated docstrings to speed development.
   * Example Pytest suite for automated testing.
   * Environment-variable management (`.env`) and security best practices built in.

By combining these enhancements with LangGraph’s powerful agent orchestration under the hood, this template accelerates the development of robust, multi-agent AI systems with minimal boilerplate.

## Quick Start

### Minimal Setup

Follow the steps below for a fast local setup:

1. Clone the repo and process the template (as above).
2. Install dependencies and configure `.env`.
3. Run `python web/main.py` and access `http://127.0.0.1:8000`.

### Full Tutorial

For an in‑depth guide covering advanced usage—including agent and tool customization, supervisor routing, deployment, and monitoring—refer to the **Tutorial** section below or see [docs/TUTORIAL.md](docs/TUTORIAL.md).

---

## Tutorial

This tutorial expands on the Quick Start with detailed instructions and examples.

### 1. Installation & Initial Run

1. Install Cookiecutter: `pip install cookiecutter`
2. Generate project: `cookiecutter https://github.com/CodeDaim0n/cookiecutter-agentic-ai`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` with your OpenAI credentials.
5. Start the server: `python web/main.py`
6. Open the UI or POST to `/api/agent` to verify setup.

### 2. Customizing Agents & Tools

* **Agents:**

  * Edit `config/nodes.json` to add or rename agents.
  * Adjust prompts and models in `config/openai_config.json`.
* **Tools:**

  * Implement Python stubs in `tools/<project>/`.
  * Define schema in `config/tools.json` and assign tools in `config/nodes.json`.

### 3. Supervisor Usage

Always send user queries to `supervisor_agent` via the UI or API. The supervisor will delegate to the appropriate worker agent based on content. Adjust its routing prompt in `config/openai_config.json` as needed.

### 4. Deployment

* **Production server:**

  ```bash
  uvicorn <project>.web.main:app --host 0.0.0.0 --port 80 --workers 4
  ```
* **Docker:** see the provided `Dockerfile` for containerization.
* **Security:** use HTTPS, manage secrets in environment variables.

### 5. Logging & Monitoring

* Logs are written to `logs/agent_logs.jsonl` and `logs/tool_logs.jsonl`.
* Integrate with ELK/Prometheus/Sentry for dashboards and alerts.

### 6. Example Scenario

**Use case:** Schedule a meeting with email and research lookup:

1. Query "Find an Italian restaurant in London." → routed to `research_agent`.
2. Query "Schedule dinner there next Friday at 7 PM and email me details." → routed to `planner_agent`.

Review logs to trace tool calls and agent decisions.

---

## Project Structure

```
your-project-name/
├── agents/                 # Agent implementations
│   └── core/
│       └── langgraph/      # LangGraph-based agent logic
├── config/                 # Configuration files
├── database/               # Database migrations and schemas
├── logs/                   # Application logs
├── tools/                  # Tool implementations
│   ├── common/             # Common utilities
│   └── your-project-name/  # Project-specific tools
├── web/                    # Web interface (FastAPI + HTML)
│   └── templates/          # HTML templates
└── tests/                  # Test suite
```

## Development

### Adding New Tools

1. Create a new tool file in `tools/your-project-name/`.
2. Add tool configuration to `config/tools.json`.
3. Update agent configurations in `config/nodes.json`.
4. Adjust prompt templates in `config/openai_config.json`.

### Adding New Agents

1. Add agent entry in `config/nodes.json`.
2. Define prompts and model settings in `config/openai_config.json`.
3. Include new agent in supervisor routing if applicable.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed by Anjali Jain
