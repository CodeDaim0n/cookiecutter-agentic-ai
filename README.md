# Multi Agent Supervisor(tool-calling) Agentic AI Template

A powerful template for creating agentic AI systems with multiple agents, tools, and a web interface. Developed by Anjali Jain.

## Features

* Multiple AI agents with different capabilities
* Supervisor agent for intelligent routing and coordination
* Customizable tools for each agent
* Web interface built with FastAPI
* Seamless OpenAI integration with function calling
* Structured project layout and type-hinted code
* Comprehensive logging and monitoring

## 🔍 Config Driven LangGraph Supervisor (with agent as tools) along with Builtin Open AI Tools support
### <div align="center"> Langgraph Multi agent
<div align="center">
   <img src="https://github.com/langchain-ai/langgraph-supervisor/blob/main/static/img/supervisor.png" 
     alt="LangGraph Supervisor Architecture" 
     width="600" 
     style="display: block; margin: 0 auto;" />


 

### <div align="center"> Langgraph Multi Agent Architecture

<div align="center">
   <img src="https://github.com/langchain-ai/langgraph-supervisor/blob/main/static/img/full_history.png" 
     alt="LangGraph Multi agent" 
     width="600" 
     style="display: block; margin: 0 auto;" />
 <br />
  <small>Source: <a href="https://github.com/langchain-ai/langgraph-supervisor/blob/main/static/img/full_history.png">LangGraph multi agent architecture</a></small>
</div>

While this template leverages the core LangGraph framework for agent orchestration, it extends and enhances the standard LangGraph approach in several important ways:

1. **Automated Project Scaffold**
   Uses Cookiecutter to generate a fully scaffolded project—with directories, config files, tool stubs, logging setup, and a FastAPI interface—so you don’t start from a blank LangGraph codebase.

2. **Low code config driven approach**
   Implements prebuilt supervisor agent and react agents using config driven approach. Scalalble and can use a centralized tool library.

3. **Schema-Driven Tool Registry**
   Tools are declared in `config/tools.json` with clear input/output schemas. LangGraph by itself requires manual registration of each function and custom prompt crafting for tool calls.

4. **Out‑of‑the‑Box FAST API Endpoint and Tester**
   Ships with a REST API endpoint (`/api/agent`) and an HTML testing UI. Standard LangGraph demos are typically code-driven notebooks or scripts without a user-facing layer.

5. **Opinionated Logging & Monitoring**
   Preconfigured JSONL logs for agent actions and tool invocations—ensuring observability from day one. LangGraph leaves logging implementation entirely up to the developer.

6. **Developer Experience Enhancements**

   * Type-hinted stubs and auto-generated docstrings to speed development.
   * Example Pytest suite for automated testing.
   * Environment-variable management (`.env`) and security best practices built in.

By combining these enhancements with LangGraph’s powerful agent orchestration under the hood, this template accelerates the development of robust, multi-agent AI systems with minimal boilerplate.

## Quick Start

### 1. Installation & Initial Run

#### 1. Clone the repository:
```bash
git clone https://github.com/CodeDaim0n/cookiecutter-agentic-ai
cd cookiecutter-agentic-ai
```

#### 2. Edit `cookiecutter.json` with your desired values:
```json
{
  "project_name": "your-project-name",
  "supervisor_name": "your-supervisor-name",
  "agent_one_name": "your-agent-one-name",
  "agent_two_name": "your-agent-two-name",
  "agent_one_tool_one": "your-agent-one-tool-one",
  "agent_one_tool_two": "your-agent-one-tool-two",
  "agent_two_tool_one": "your-agent-two-tool-one",
  "agent_two_tool_two": "your-agent-two-tool-two"
}
```

#### 3. Copy the template processor script:
```bash
cp replace_cookiecutter.py ..
cd ..
```

#### 4. Run the template processor from the parent directory:
```bash
python replace_cookiecutter.py
```

The script will:
- Find the template directory
- Replace all cookiecutter variables in files and folder names
- Rename the project directory to your specified name
- Preserve any Jinja2 variables that are not cookiecutter variables
- Handle both file contents and directory names
- Create a backup of the original template directory

Note: The script will create a backup of your template directory before making any changes. If you need to restore the original template, you can find it in the `cookiecutter-agentic-ai-backup` directory.

#### 5. Install dependencies:
```bash
cd your-project-name
pip install -r requirements.txt
```

#### 6. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other configurations
```
Open the newly created .env file in a text editor and set your OpenAI API credentials and any other relevant settings. At minimum, you should provide:

OPENAI_API_KEY – your OpenAI API key
OPENAI_MODEL – the model ID you want to use (e.g. gpt-3.5-turbo-0613 or gpt-4-0613, preferably one that supports function calling for tool use)
(Other environment variables may be present for database or other configurations; adjust as needed.)
#### 7. Run the development server:
```bash
python web/main.py
```
This will launch the app (using Uvicorn under the hood) on the default address http://127.0.0.1:8000. You should see log output indicating the server is running. Open a browser and navigate to http://127.0.0.1:8000 to access the web interface.

#### 8. Test the Setup
Try out the system via the web UI or API. For example, using the web interface, you can enter a query and see how the system responds (more on usage below). You can also directly call the API endpoint (e.g. using curl or a tool like Postman):
bashcurl -X POST "http://127.0.0.1:8000/api/agent" \
-H "Content-Type: application/json" \
-d '{"agent_name": "supervisor_agent", "message": "Hello world", "identifier": "user123"}'
This sends a sample request to the supervisor agent. The response (in JSON) should come back with an output from one of the agents. If you see a coherent reply or structured output, your setup is working!

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
Let's break down some of these components:

### agents/core/langgraph/

Contains the classes and functions that construct your agents and the supervisor using the LangGraph framework. Notable files include:

- `supervisor_agent_builder.py` – Defines how the supervisor agent is created and how it routes requests
- `react_agent_builder.py` – Defines how a generic reactive agent (one that can use tools via the ReAct paradigm or OpenAI function calling) is created
- `agent_dispatcher.py` – The central dispatcher that receives a user request and orchestrates the supervisor/agent interaction. The FastAPI endpoint calls this to get a response from the system

### config/

Contains JSON configuration files that define the behavior of the system:

- `nodes.json` – Defines the agents (nodes) in the system, their type, description, and which tools each has access to. By default it has an entry for the supervisor and two agents
- `tools.json` – Defines the available tools and their details, such as name, description, the function that implements the tool, and input/output schemas for each tool. This is used to inform the agents (and the OpenAI function-calling API) about what tools can do
- `openai_config.json` – Defines prompt templates and parameters for each agent and tool when interacting with the OpenAI API. For example, it includes system prompts for the supervisor and agents, instructing their behavior, and templates for how to invoke certain tools (like web search or email) using the function calling feature

### database/

(Optional) Contains database setup or seed data. By default there's a `seed.sql` which could be used to initialize a database. The template doesn't heavily use a database out of the box, but this directory is provided for you to store any data or setup scripts if your agents/tools require a database (for example, to store long-term memory or user data).

### logs/

Will be created at runtime to store log files. The template's logging utility writes two main log files here:

- `agent_logs.jsonl` – Logs of each agent's activity (when an agent is invoked, what output it produced, how long it took, etc.), one JSON record per event
- `tool_logs.jsonl` – Logs of each tool invocation (which agent/tool was used, input parameters, output, timing, etc.)

These logs are extremely useful for debugging and monitoring the behavior of your agents, especially in complex multi-step scenarios.

### tools/common/

Utility modules to support tool and agent functionality. For instance:

- `config.py` (for loading config and environment variables via python-dotenv)
- `logger.py` (sets up logging as mentioned)
- `moderation.py` (handles content moderation via OpenAI's safety API before/after agent calls)
- `prompt.py` (utilities for constructing prompts or calling the OpenAI API)
- `tool_loader.py` and `tool_wrappers.py` (helpers to integrate your Python tool functions with the OpenAI function-calling mechanism, likely using LangChain's StructuredTool)

### tools/your_project_name/

This is where the actual tool functions for your agents reside. By default, the template provides:

- An `openai_web_search_tool.py` – an example implementation of a web search tool using OpenAI (if OpenAI has web search capabilities or via integration)
- Stubs for each tool you named in the cookiecutter prompts (e.g. if you left defaults, you'd see files like `agent_one_tool_one.py`, etc.). These files include function definitions (with type hints and docstrings) that you should implement. For example, if `agent_one_tool_one` is meant to "plan something", you would add code inside that function to perform the planning (or call an external API, etc.). By default, the stubs might just return a placeholder or have a TODO note
- The template also references an `openai_mcp_send_email_tool` (Multi-Channel Platform email tool) in the config. This tool is configured to demonstrate how an agent could send emails via an external service (e.g., Zapier or another API). You can implement this if needed by integrating with an email-sending service

### web/

The FastAPI application that ties everything together:

- `main.py` – The FastAPI app definition. It sets up an API endpoint (`POST /api/agent`) that accepts a request with `agent_name`, `message`, and an optional `identifier` (user ID or session ID). The endpoint uses the agent_dispatch function to process the request and returns the agent's response. There's also a simple GET endpoint for the root (`/`) which serves the HTML interface
- `templates/index.html` – A basic web interface for testing your agents. It has a simple form (or script) where you can input an agent name and message, and it will display the response. By default, you might select the supervisor agent and input a query

### tests/

Contains unit tests to verify that the agent system works. The template includes example tests (using pytest) for calling the react agent and the supervisor agent. You can run pytest to ensure everything is functioning, and use this area to add your own tests as you develop new features or tools.

## Usage

Once your project is up and running, here's how you can use and interact with your multi-agent system:

### Web Interface

Open your browser to `http://127.0.0.1:8000` (or the appropriate host/port if you changed it). You'll see a simple interface (titled with your project name and "Agent Tester"). Here you can input a message and select which agent to send it to. For typical use, you would choose the supervisor agent and enter a user query. The supervisor will process your request and route it to one of the specialized agents behind the scenes. The response will then be displayed on the page. This is a quick way to manually test queries and see how the system responds.

### API Endpoint

The core functionality is exposed via a REST API endpoint at `POST /api/agent`. You can integrate this into other applications or services. The request JSON should include:

- `agent_name`: The name of the agent you want to invoke (e.g. "supervisor_agent" to let the system decide, or you can directly call "agent_one" or "agent_two" for testing specific agents)
- `message`: The user's message or query you want the agent to handle
- `identifier`: (Optional) An ID for the user or session. This could be used by agents for context or personalization, or for logging purposes. If not needed, it can be omitted or set to null

Example using curl:

```bash
curl -X POST "http://127.0.0.1:8000/api/agent" \
-H "Content-Type: application/json" \
-d '{"agent_name": "supervisor_agent", "message": "Book a meeting with John for next week", "identifier": "user123"}'
```

This would send the request "Book a meeting with John for next week" to the supervisor agent, which might decide this is a task for the planning agent (agent one) and delegate it accordingly. The JSON response will contain the result. For instance, the planning agent might respond with a structured output confirming the meeting scheduled (depending on your tool implementation).

### Interpreting Responses

By default, agents are designed to return responses in a structured JSON format (this is guided by the prompt templates and tools configuration). For example, an agent's answer might look like:

```json
{
  "output": "Scheduled a meeting with John on Tue 12th at 10 AM. Invitation sent via email.",
  "explanation": "I used the calendar tool to find a free slot and the email tool to send the invite."
}
```

The exact structure of the output depends on the `agent_output_schema` defined in the prompts and how you implement the tools. You can adjust this schema as needed for your application. The important part is that the system encourages well-structured outputs for easier parsing and handling downstream.

### Agent Direct Calls

While the typical flow is to always send user queries to the supervisor agent, you can also directly query a specific agent via the API (by setting `agent_name` to your agent's id). This will bypass the supervisor and invoke the chosen agent with the message. Direct calls can be useful for debugging a single agent's behavior or if you design your system such that users sometimes address a specific agent. Keep in mind if you call an agent directly, the supervisor's logic (like deciding which agent fits best) is skipped entirely.

### Logs and Monitoring

As you use the system, check the `logs/` directory for the JSONL log files. They will record each step:

- An entry in `agent_logs.jsonl` every time an agent (including the supervisor) processes a request, showing the input and output
- An entry in `tool_logs.jsonl` every time a tool function is executed by an agent, including input parameters and results

These logs are useful for understanding what happened internally. For instance, if an agent's response is not what you expect, you can look at the logs to see what tools it tried to use or if it encountered an error or a content moderation block. For real-time debugging, you can keep a terminal open with `tail -f logs/agent_logs.jsonl` to watch agent actions as they happen.

### Running Tests

Use the included tests to verify system integrity, especially after you make changes. Run `pytest` in the project directory. The provided tests ensure that the core agent dispatch and a basic agent-tool interaction work as intended. You should expand the test suite with scenarios specific to your use cases as you develop new capabilities.

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

### Customizing Tools

Tools are how agents interact with the world or perform specific functions (searching the web, sending an email, performing calculations, etc.). Customizing tools allows you to extend what your agents can do:

#### Implementing Tool Logic

In the `tools/your_project_name/` directory, you'll find Python files for each tool. Initially, these may be stubs with function definitions. You should edit these files and implement the actual logic. For example, if you have a `send_email_tool.py`, integrate it with an email service or SMTP server. If you have a `web_search_tool.py`, you might call an external search API or use OpenAI's built-in browsing (if available).

Each tool function should accept certain parameters (as defined in the function signature and the `input_schema` in config) and return a result (which will be given to the agent). Make sure to handle errors or exceptions inside tools so that the agent can handle tool failures gracefully (you can return an error message in the output, etc., or log and raise).

#### Defining New Tools

To add a completely new tool:

**Create the Function**: Write a new Python function (and file) in `tools/your_project_name/`. For consistency, name the file and function something descriptive of the tool's purpose. Use type hints for inputs and outputs, and document it with a docstring.

**Register in tools.json**: Open the `config/tools.json` file and add a new entry in the "tools" list. Each tool entry needs:

- A unique name (this is what the agent will refer to when deciding to use it)
- A description (used in the OpenAI function calling to describe what the tool does)
- A `function_path` which points to your Python function. For example, `"tools.your_project_name.my_new_tool.my_new_tool"` (format is `<python_module_path>.<function_name>`)
- An `input_schema` defining what inputs the tool expects (name and type for each parameter)
- An `output_schema` defining the structure of the tool's return value
- If the tool calls an external service or requires special handling, also specify if it requires user approval or any constraints (the template includes examples where `tool_choice` is set to "required", meaning the agent must use that tool for certain queries)

**Assign to Agents**: If this tool is meant for certain agents to use, add the tool's name to the appropriate agent's tool list in `config/nodes.json`. For instance, if you make a `calculator_tool` and only your Agent Two should use it, add "calculator_tool" to Agent Two's "tools" list in `nodes.json`.

**Update Prompts (if needed)**: You might want to update the agent's prompt in `openai_config.json` to mention the new capability or adjust instructions.

After adding a tool, reload or restart your application. The agent (through LangChain/LangGraph) will now be aware of the new tool when reasoning.


#### Tool Security and Moderation

Be mindful that giving agents tools (especially powerful ones like file access, network calls, or email) can introduce risks. The template includes a `moderation.py` that can check content via OpenAI's content moderation API. It's a good idea to ensure your agent cannot misuse tools. For critical tools, you might implement a confirmation step or constraints. For example, you might have the agent propose an action and require a user click or approval before actually executing a very sensitive tool. This can be implemented at the application layer (outside the agent) if needed.

#### Fine-Tuning Tool Behavior

The template uses the OpenAI function calling feature via LangChain. Each tool's `input_schema` and `output_schema` in `tools.json` should match what your Python function expects/returns. If you change the function signature or return structure, update the schemas so the agent knows how to call it correctly and interpret the results. This ensures that the LLM chooses the right arguments and reads results properly.

### Adjusting OpenAI Settings

The integration with OpenAI can be tuned for your needs:

**Model Choice**: In your `.env` (or directly in `openai_config.json`), set which model to use. GPT-4 tends to be more capable, especially for complex reasoning and understanding when to use tools, whereas GPT-3.5 (with function calling) is faster and cheaper but may be less reliable. You could use GPT-4 for the supervisor and GPT-3.5 for the worker agents if cost is a concern, by specifying different model values for each agent in `openai_config.json`.

**Temperature and Other Parameters**: The template might not expose these in config by default, but you can certainly adjust how "creative" or deterministic the AI responses are by setting the temperature, max tokens, etc. If using LangChain, these could be set in the agent builder or the prompt configuration. For instance, you could modify the code in `prompt.py` or the LangChain ChatOpenAI instantiation to set `temperature=0` for the supervisor (to make it deterministic) and a higher value for a creative agent, etc.

**Rate Limits and API Keys**: If you expect high volume usage, consider OpenAI rate limits. You might implement retries or handling for rate limit errors in the prompt utilities. If you have multiple API keys, you could distribute calls among them or use proxies. These are advanced topics, but keep them in mind as you scale.

### Logging and Monitoring

Logging is already enabled in the template. All agent and tool events are logged to files. Here are some tips for using this for monitoring:

**Viewing Logs**: As mentioned, you can tail the JSONL files or write a simple script to parse and aggregate them. They contain timestamps and durations which can help identify performance bottlenecks (e.g., if a certain tool call is slow or if an agent is taking a long time to respond).

## Contributing

Contributions to improve this template are welcome! If you have ideas, bug fixes, or new features, please follow these steps:

1. **Fork the Repository**: Create a fork of the cookiecutter template repository on GitHub.

2. **Create a Branch**: Make a feature branch for your changes (e.g., `feature/improve-logging` or `bugfix/fix-tool-schema`).

3. **Commit Changes**: Make clear commits with descriptive messages explaining your modifications.

4. **Push and Open a PR**: Push your branch to your fork and open a Pull Request to the main repository. Describe the changes and why they are beneficial. Maintainers will review your PR and discuss any needed adjustments.

5. **Ensure Tests Pass**: If you add functionality, try to add or update tests. Make sure pytest runs without failures. This makes it easier for your contribution to be accepted.

## Credits & Attribution

This project is built upon the **Cookiecutter Agentic AI Template** created by:
- **Anjali Jain** (Original Creator)
- **Contributors** to the Cookiecutter Agentic AI Template

### Original Template
- Repository: https://github.com/CodeDaim0n/cookiecutter-agentic-ai
- License: MIT License
- Created by: Anjali Jain

### Acknowledgments
We acknowledge and thank the original creators for providing the foundational framework that made this project possible.

You can also open issues on the repo if you find problems or have questions. We appreciate feedback and contributions from the community to make this template better for everyone.
