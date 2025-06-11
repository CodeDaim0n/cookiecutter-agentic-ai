# Cookiecutter Agentic AI Template

## Overview

The Cookiecutter Agentic AI Template is a project template that helps you quickly set up a multi-agent AI system. It provides a structured foundation to build AI applications where multiple agents (powered by large language models) can collaborate to solve tasks. Each agent can have specialized capabilities and tools, and a supervisor agent coordinates their efforts. The template includes integration with OpenAI's API out-of-the-box, a FastAPI web interface for interaction, and a robust project structure with best practices (type hints, logging, etc.) to accelerate development of agentic AI systems.

Agentic AI systems are autonomous agents that can reason, plan, and take actions (often via tools) to achieve goals. This template allows you to create such agents (for example, a "ResearchAgent" for web research and an "ActionAgent" for executing tasks) and a supervising agent that decides which agent should handle a given user request. By using this template, you get a head start with a working multi-agent architecture and can focus on implementing your custom logic.

## Features

- **Multiple AI Agents with Specialized Roles**: Scaffold two AI agents (and a supervisor) with distinct capabilities. For example, one agent might handle planning or execution tasks while another focuses on research or analysis. The architecture can be extended to more agents as needed.

- **Supervisor Agent for Coordination**: A top-level agent oversees incoming user requests and routes them to the appropriate specialist agent. This hierarchical approach simplifies multi-agent orchestration and decision-making.

- **Customizable Tools per Agent**: Each agent can use specific tools (functions or external APIs) to enhance its capabilities. The template defines placeholders and examples (e.g. web search, email sending) that you can customize or extend. Tools are configured via JSON and implemented as Python functions for flexibility.

- **FastAPI Web Interface**: A web application (built with FastAPI) is included for interacting with your agents in real time. It provides API endpoints (e.g. for chatbot queries) and a simple web UI to test agent behaviors. This makes it easy to demo and deploy your multi-agent system with a user-friendly interface.

- **OpenAI API Integration**: Built-in integration with OpenAI's API (e.g. GPT-4 or GPT-3.5) for the agents' intelligence. Simply plug in your API key and model of choice, and the agents will use OpenAI under the hood for reasoning and tool usage (including support for function calling to use tools).

- **Structured Project Layout**: The template follows a clean project structure to organize agents, tools, configurations, web app, tests, etc. This encourages good project hygiene and makes it easier to navigate and maintain the codebase.

- **Type Hints and Documentation**: All provided code uses Python type hints to improve clarity and facilitate static analysis/IDE help. Key functions and classes include docstrings. You can easily expand on this for your own code, and generate documentation if desired.

- **Logging and Monitoring**: Comprehensive logging is configured to record agent decisions and tool usage. Each agent action and tool call can be logged (with timestamps and durations) to JSON lines files, enabling you to monitor the system's behavior and performance. This can be extended for production monitoring or debugging complex interactions.

## Getting Started

Follow these steps to create a new project using the Cookiecutter Agentic AI Template.

### 1. Install Cookiecutter (if you don't have it)

Cookiecutter is a command-line utility to generate projects from templates. Install it via pip:

```bash
pip install cookiecutter
```

### 2. Generate a New Project

Use cookiecutter to create a project from this template repository:

```bash
cookiecutter https://github.com/CodeDaim0n/cookiecutter-agentic-ai
```

When you run this command, you will be prompted to enter several configuration values for your new project:

- `project_name`: The name of your project (also used as the main Python package/folder name)
- `supervisor_name`: The name for the supervisor agent (e.g. supervisor_agent by default)
- `agent_one_name`: Name of the first agent (e.g. agent_one or something descriptive like planner_agent)
- `agent_two_name`: Name of the second agent (e.g. agent_two or research_agent)
- `agent_one_tool_one`: Name for the first tool of agent one (e.g. agent_one_tool_one or a descriptive name like schedule_tool)
- `agent_one_tool_two`: Name for the second tool of agent one
- `agent_two_tool_one`: Name for the first tool of agent two
- `agent_two_tool_two`: Name for the second tool of agent two

**Note**: You can accept the default names (shown in parentheses) or choose your own. The template will use these names to generate files and code placeholders accordingly.

### 3. Install Project Dependencies

After generation, navigate into your new project directory:

```bash
cd your-project-name
pip install -r requirements.txt
```

This will install all required Python packages (FastAPI, LangChain/LangGraph, OpenAI, Pydantic, etc.) for your project.

### 4. Configure Environment Variables

The project uses environment variables for configurable settings such as the OpenAI API key and model. Copy the example environment file and update it:

```bash
cp .env.example .env
```

Open the newly created `.env` file in a text editor and set your OpenAI API credentials and any other relevant settings. At minimum, you should provide:

- `OPENAI_API_KEY` – your OpenAI API key
- `OPENAI_MODEL` – the model ID you want to use (e.g. gpt-3.5-turbo-0613 or gpt-4-0613, preferably one that supports function calling for tool use)
- (Other environment variables may be present for database or other configurations; adjust as needed.)

### 5. Run the Development Server

Start the FastAPI web server to interact with your agents:

```bash
python web/main.py
```

This will launch the app (using Uvicorn under the hood) on the default address `http://127.0.0.1:8000`. You should see log output indicating the server is running. Open a browser and navigate to `http://127.0.0.1:8000` to access the web interface.

### 6. Test the Setup

Try out the system via the web UI or API. For example, using the web interface, you can enter a query and see how the system responds (more on usage below). You can also directly call the API endpoint (e.g. using curl or a tool like Postman):

```bash
curl -X POST "http://127.0.0.1:8000/api/agent" \
-H "Content-Type: application/json" \
-d '{"agent_name": "supervisor_agent", "message": "Hello world", "identifier": "user123"}'
```

This sends a sample request to the supervisor agent. The response (in JSON) should come back with an output from one of the agents. If you see a coherent reply or structured output, your setup is working!

## Project Structure

When you generate a project, it will have a well-organized directory structure as follows:

```
your-project-name/
├── agents/                     # Agent implementations
│   └── core/
│       └── langgraph/         # Core agent logic built on LangGraph
├── config/                    # Configuration files for agents, tools, etc.
├── database/                  # Database files or migrations
├── logs/                      # Logs generated by agents and tools
├── tools/                     # Tool implementations for agents
│   ├── common/               # Common utilities
│   └── your_project_name/    # Project-specific tools
├── web/                      # Web server (FastAPI) and UI files
│   └── templates/            # HTML templates for the web interface
└── tests/                    # Test suite for agents and tools
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

## Customization

One of the main benefits of this template is how easily you can customize and extend it to fit your needs. Below are key ways to tailor the system:

### Customizing Agents

By default, you have two example agents plus the supervisor. You can change their behavior or add new agents:

#### Renaming or Repurposing Agents

The names you provided at project creation determine the agent identifiers. You can change agent descriptions and roles in `config/nodes.json` and adjust their prompt behavior in `config/openai_config.json`. For example, you might turn the first agent into a "PlanningAgent" that handles scheduling and emailing, and the second into a "ResearchAgent" that handles answering factual questions via web search. Update their description in `nodes.json` accordingly to reflect their purpose.

#### Modifying Agent Prompts

Open `config/openai_config.json` and you will find an entry for each agent (keyed by the agent's id). This includes the system prompt (called `input_template` here) and the model to use. You can edit the prompt to give the agent a different personality or instructions. For instance, if agent one should be more formal or constrained, adjust its prompt template. You can also change which OpenAI model is used per agent (by default they all reference `${OPENAI_MODEL}`, but you could specify a different model name per agent if needed and have multiple OpenAI API keys or systems).

#### Adding a New Agent

If your application demands more than two specialized agents, you can certainly add more.

**Create the Agent Logic**: Develop the new agent's class or builder. Often, you can follow the pattern in `agents/core/langgraph/react_agent_builder.py` to create another agent type or use one of the LangGraph prebuilt agents. You may not need to write much code if the agent is similar to existing ones; sometimes it's just configuration.

**Register in Configuration**: Add a new entry in `config/nodes.json` for your agent. Give it a unique id (name) and specify its type (likely "react_agent" for an LLM-driven agent with tools, or another type if you implement differently), description, and the list of tool names it can use.

**Prompt and Model Setup**: Add a corresponding entry in `config/openai_config.json` for the agent. Define its prompt template (how it should behave) and model or any special parameters. Also ensure any tools it will use are defined in `tools.json` (see next section).

**Include in Supervisor's purview**: Update the supervisor agent's entry in `nodes.json` so that its "agents" list includes the new agent's ID. This way, the supervisor knows it can route tasks to the new agent. You might also want to tweak the supervisor's prompt in `openai_config.json` to account for the new agent, perhaps by mentioning its role so the supervisor can properly choose it.

**Frontend/UI (Optional)**: If you're using the provided web UI for testing, you might want to add the new agent to the dropdown or selection mechanism so you can directly test it. The `index.html` is simple and can be modified to list the new agent name.

After adding a new agent, restart the server and test it out with some queries specific to its function.

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

**Expanding Logging**: You can add additional logging in your own code as needed. For example, if you want to log when an agent makes a certain decision or if you want to log the content of messages for debugging, you can use the logging module. The `logger.py` sets up two loggers (`tool_logger` and `agent_logger`). You can use them or create new ones for different subsystems.

**External Monitoring**: For production systems, you might integrate with monitoring tools or APM (Application Performance Monitoring). Since the app is FastAPI-based, you could incorporate middleware for logging request metrics or integrate with services like Prometheus/Grafana for metrics. Additionally, consider using OpenAI's observability tools or LangSmith (from LangChain) for tracing and debugging agent behavior in depth. The template's use of LangChain/LangGraph means you could hook into those frameworks' callbacks to log tool usage or agent thoughts in real-time, or even visualize them.

**Error Handling**: Monitor the logs for any errors or exceptions (e.g., tool function errors or API call issues). The FastAPI app will return an HTTP 500 if something goes wrong server-side. By default, the `call_agent` endpoint wraps calls in a try/except and will return a JSON error message if an exception is thrown. In a real deployment, you might want more robust error handling, such as returning a friendly message to the user or implementing a fallback behavior if a tool fails (for instance, if the web search fails, maybe have the agent apologize or try an alternative approach).

## Contributing

Contributions to improve this template are welcome! If you have ideas, bug fixes, or new features, please follow these steps:

1. **Fork the Repository**: Create a fork of the cookiecutter template repository on GitHub.

2. **Create a Branch**: Make a feature branch for your changes (e.g., `feature/improve-logging` or `bugfix/fix-tool-schema`).

3. **Commit Changes**: Make clear commits with descriptive messages explaining your modifications.

4. **Push and Open a PR**: Push your branch to your fork and open a Pull Request to the main repository. Describe the changes and why they are beneficial. Maintainers will review your PR and discuss any needed adjustments.

5. **Ensure Tests Pass**: If you add functionality, try to add or update tests. Make sure pytest runs without failures. This makes it easier for your contribution to be accepted.

You can also open issues on the repo if you find problems or have questions. We appreciate feedback and contributions from the community to make this template better for everyone.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it as per the terms of the license. See the LICENSE file in the repository for the full license text.

## Credits

This template was created and is maintained by Anjali Jain (and contributors). If you use this template for your project or research, a shout-out or attribution is appreciated but not required. We hope this template accelerates your development of powerful AI agent systems – happy building!

---

# Tutorial: Building an Agentic AI System with the Cookiecutter Template

Welcome to the tutorial! In this guide, we will walk through the process of using the Cookiecutter Agentic AI Template to build and deploy a multi-agent AI application. By the end of this tutorial, you will have a running system with multiple AI agents that can be interacted with via a web interface or API, and you'll understand how to customize the system for your own real-world use cases.

## What This Tutorial Covers:

- Installation of the template and initial project setup
- Customizing the agents and their tools to fit your needs
- Utilizing the supervisor agent to manage multi-agent workflows
- Deploying the FastAPI web application for your agent system
- Integrating OpenAI and configuring it properly (API keys, models, etc.)
- Setting up logging and monitoring to keep an eye on your system
- A walkthrough of an example scenario using the agents in a real-world task

Let's get started!

## 1. Installation and Setup

Before diving into coding, let's set up the environment and generate a project using the cookiecutter template.

### Prerequisites

- Python 3.9+ installed on your system. (Python 3.10 or 3.11 is recommended for compatibility with the latest libraries.)
- An OpenAI API key if you intend to use OpenAI's language models (which this template is configured for)
- (Optional) Git if you want to version control your new project or if installing the template via a Git URL

### Step 1: Install Cookiecutter

If you haven't already installed Cookiecutter, do so via pip:

```bash
pip install cookiecutter
```

Cookiecutter is the tool that will use the template to generate your project files.

### Step 2: Generate a New Project

Run the cookiecutter command with the template's repository URL:

```bash
cookiecutter https://github.com/CodeDaim0n/cookiecutter-agentic-ai
```

When you run this, cookiecutter will download the template and prompt you for configuration values. Here's an example of filling it out:

```
project_name [my-agentic-ai]: planner-bot
supervisor_name [supervisor_agent]: supervisor_agent
agent_one_name [agent_one]: planner_agent
agent_two_name [agent_two]: research_agent
agent_one_tool_one [agent_one_tool_one]: plan_event_tool
agent_one_tool_two [agent_one_tool_two]: send_email_tool
agent_two_tool_one [agent_two_tool_one]: web_search_tool
agent_two_tool_two [agent_two_tool_two]: analyze_data_tool
```

In the above example:
- We named our project "planner-bot". This will be the folder name and main package name
- We kept the supervisor agent name as default ("supervisor_agent")
- We named the first agent "planner_agent" (imagining it will handle scheduling and emailing tasks)
- We named the second agent "research_agent" (for handling web searches or data analysis)
- For agent one's tools, we used "plan_event_tool" and "send_email_tool"
- For agent two's tools, we used "web_search_tool" and "analyze_data_tool"

You can choose names relevant to your intended use case. If you're unsure, you can stick with the defaults and rename things later in the code.

Cookiecutter will create a new directory named after your `project_name` (e.g., `planner-bot/`) containing the generated project.

### Step 3: Set Up the Python Environment

Navigate into your new project directory and install the required dependencies:

```bash
cd planner-bot # use your project folder name
pip install -r requirements.txt
```

This will install all the necessary libraries listed in `requirements.txt`. Notable ones include FastAPI, Uvicorn, LangChain and LangGraph, OpenAI, Pydantic, etc. It might take a minute to install them all.

**Tip**: It's good practice to do this in a Python virtual environment (using `venv` or `conda`) to avoid conflicts with other projects. For example:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

The template uses a `.env` file to manage configuration such as API keys. If your project directory contains an `.env.example` file, copy it to `.env`:

```bash
cp .env.example .env
```

If there is no `.env.example`, you can create a file named `.env` at the project root.

Open the `.env` file in an editor and add the necessary configuration. For example:

```
OPENAI_API_KEY=<your-openai-api-key-here>
OPENAI_MODEL=gpt-4-0613
# (Optional) other config values
```

Replace `<your-openai-api-key-here>` with your actual API key from OpenAI. The `OPENAI_MODEL` is set to a GPT-4 variant in this example; you can choose the model you prefer (ensure it supports function calling if you plan on using the tools mechanism — for instance, `gpt-3.5-turbo-0613` also supports function calls).

You might see other environment variables in the code (for database URL, etc.), but those are optional or for advanced usage. The critical ones are the OpenAI settings.

Make sure to never commit your `.env` file to version control (the template's `.gitignore` should exclude it) because it contains sensitive keys.

### Step 5: Initial Project Run

With dependencies installed and the environment configured, it's time to run the application and ensure everything is working:

Start the FastAPI app by running the `main.py`:

```bash
python web/main.py
```

On the first run, you should see output indicating Uvicorn (the ASGI server) is starting up, for example:

```
INFO: Started server process [12345]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

This means the server is up on port 8000.

Open your web browser and go to `http://127.0.0.1:8000`. You should see a simple page titled something like "planner-bot Agent Tester" (with your project name). There will likely be a text input for your message and maybe a dropdown to select an agent. By default, select the supervisor agent and enter a test message, such as "Hello". Submit the form (or hit Enter).

If everything is set up correctly, you should see a response appear, possibly something like a JSON output or a greeting generated by the agent. This indicates the whole chain (supervisor -> agent -> OpenAI -> response) is functioning.

### Step 6: Troubleshooting Setup Issues

**No response or error on UI**: If the page isn't loading or you get an error, check the terminal where the server is running. FastAPI will log any exceptions. Common issues could be missing API key, or a mistake in the `.env` file. Fix the error (for example, ensure `OPENAI_API_KEY` is set and valid) and try again.

**API call using curl not working**: Double-check the JSON syntax and the URL. Ensure the server is running. You might also test using an API client like Postman or HTTPie for easier debugging.

**Dependency errors**: If `pip install` failed for some reason (like a compilation error or version conflict), make sure you're using a compatible Python version. You can also try upgrading pip (`pip install --upgrade pip`) and reinstalling. The requirements are pinned to versions that should work together, so use the specified versions if possible.

**OpenAI errors or no output**: If your OpenAI key is set but the agent isn't responding, it could be the OpenAI API is failing. The console might show an error from the OpenAI library. Possible issues: wrong model name, expired key, or hitting rate limits. Try a simpler model (like `gpt-3.5-turbo`) to verify, and ensure your key is active. Also, the first call with a new key might be slow if the OpenAI API is warming up; give it a few seconds.

Once the basic setup is verified, you're ready to customize the system to do something truly useful.

## 2. Customizing Agents and Tools

Now comes the fun part: tailoring the template's generic agents to your specific needs. Out of the box, the system is somewhat generic (the agents don't have domain-specific knowledge beyond what the AI model knows, and the tool stubs do minimal work). To make the system perform a real task, you'll want to implement the tools and possibly adjust the agent prompts/logic.

### Understanding the Default Agents and Tools

By default, assuming you used names like we did in the example:

- **Supervisor Agent**: This agent's job is to read the user's request and decide which agent should handle it. It does not directly answer the query, but rather forwards it.
- **Planner Agent (Agent One in our example)**: Intended to handle "planning or structured tasks". It has tools `plan_event_tool` and `send_email_tool` plus an email sending capability configured (via `openai_mcp_send_email_tool` in config). Think of it as the action-oriented agent.
- **Research Agent (Agent Two in our example)**: Intended for "analysis or research". It has tools `web_search_tool` and `analyze_data_tool` plus a web search capability. Think of it as an information-gathering agent.

The separation of concerns means if a query is more about looking up information, the supervisor should pick the Research Agent; if it's about performing an action or planning something, it should pick the Planner Agent. This is guided by the system prompts we saw in `openai_config.json`:

- The Planner Agent's prompt mentions its tools (planning and email) and says "focus on helping the user move forward with a concrete task"
- The Research Agent's prompt mentions its tools (search and analysis) and says "focus on helping the user with information"

These instructions help the AI pick the right approach.

### Customizing Agent Behavior

Let's say we want the Planner Agent to be very formal and always confirm actions, while the Research Agent should cite sources in answers.

#### Editing Prompts

Open `config/openai_config.json`. Find the section for your `planner_agent`. You might see something like:

```json
"planner_agent": {
  "model": "${OPENAI_MODEL}",
  "input_template": "You are planner_agent. The user said: '{{ message }}'. You can use tools such as plan_event_tool and send_email_tool... Always focus on helping the user move forward with a concrete task."
}
```

You can modify this `input_template`. For example:

```json
"input_template": "You are a planning assistant AI. Your job is to help the user plan events and handle communications. The user said: '{{ message }}'. Be very formal and polite in your responses. If you need to use a tool (like planning something or sending an email), do so. Always confirm with the user when an action is completed."
```

This will bias the Planner Agent to behave more formally and confirm actions.

Similarly for the Research Agent:

```json
"input_template": "You are a research assistant AI. The user said: '{{ message }}'. You have access to web_search_tool and analyze_data_tool. Use these to find factual information. Provide clear answers and cite the source of the information if relevant."
```

This might encourage the agent to say something like "According to [Source], ..." in its output (though remember, the AI will do its best to follow the instruction; it doesn't automatically get sources unless the tool fetches them).

#### Changing Agent Tools

Perhaps you want both agents to have access to a shared tool, like a `calculator_tool` for simple math. You could create the tool and add it to both agents' tool lists in `nodes.json`. This would allow either agent to use that capability.

#### Adding Memory or Context

By default, each API call to the agent is stateless (aside from the `identifier` which could be used to track a user). If you want agents to have memory of past interactions or a long conversation, you'd need to implement that, possibly by storing conversation history keyed by `identifier` and feeding relevant history into the prompt. This is more advanced and not directly provided by the template, but the hooks are there (you have `identifier` and you could modify the agent dispatcher to pull past logs from a database or memory and include it in the context). LangChain offers memory modules that you could integrate if needed.

### Implementing Tool Functions

The template provides placeholders for tool functions, but it's up to us to fill them in with actual code. Let's implement the tools from our Planner and Research agent example:

#### Plan Event Tool (`plan_event_tool`)

Suppose this tool should take a `user_id` and a `context` (maybe context includes what event to plan) and return some plan or confirmation.

Open `tools/your_project_name/plan_event_tool.py`. Inside, it might look like:

```python
def plan_event_tool(user_id: str, context: str) -> Dict[str, Any]:
    """
    Executes a planning-related action based on input context.
    """
    # TODO: implement tool logic here
    return {"output": "Plan created (placeholder)"}
```

We can implement a simple logic: just return a message that it's done, or integrate with an external calendar API if we want to be fancy. For now, let's say:

```python
# For demonstration, let's assume context is something like "meeting with John on Tuesday at 10"
plan_details = context # in reality, you might parse or use an API
# Here you would add the event to a calendar, etc. We'll simulate that:
confirmation = f"Scheduled: {plan_details}"
return {"output": confirmation}
```

This is a stub implementation. You could integrate a real calendar service here.

#### Send Email Tool (`send_email_tool`)

This could call an email API (like SendGrid, or use SMTP). For the sake of example:

Open `send_email_tool.py` and implement:

```python
def send_email_tool(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Sends an email with the given subject and body to the recipient.
    """
    # Here you'd integrate with an email sending service.
    # For now, we'll just pretend and return a success message.
    try:
        # email_service.send(to=recipient, subject=subject, body=body)
        status = "sent"
    except Exception as e:
        status = f"failed: {str(e)}"
    
    return {"output": f"Email {status} to {recipient}"}
```

We also need to adjust the `tools.json` entry for `send_email_tool` if it expects different inputs. Maybe originally it was using the MCP approach. If we bypass that and implement directly, ensure `tools.json` has an entry:

```json
{
  "name": "send_email_tool",
  "description": "Sends an email to a specified recipient.",
  "function_path": "tools.your_project_name.send_email_tool.send_email_tool",
  "input_schema": {
    "recipient": "string",
    "subject": "string",
    "body": "string"
  },
  "output_schema": {
    "structure": {
      "output": "string"
    }
  }
}
```

And in `nodes.json`, ensure `send_email_tool` is listed in the Planner Agent's tools. (The template might have had a more complex setup with `openai_mcp_send_email_tool`. You can simplify by using your direct `send_email_tool` instead, or keep their approach if you plan to integrate with a specific platform.)

#### Web Search Tool (`web_search_tool`)

The template likely provided `openai_web_search_tool.py` that uses OpenAI's web browsing. If you have internet access for the agent (note: OpenAI's new web browsing requires certain conditions or the use of Plugins or GPT-4 browsing), or you could integrate a third-party API (like SerpAPI or Bing API).

Let's assume we want to use an external search API. You could do something like:

```python
import requests

def web_search_tool(query: str) -> Dict[str, Any]:
    """
    Searches the web for the query and returns a summary of results.
    """
    # For demonstration, call a hypothetical search API
    response = requests.get("https://api.example.com/search", params={"q": query, "api_key": "..."})
    data = response.json()
    
    # parse data to get top result
    if data.get("results"):
        top_result = data["results"][0]
        summary = top_result.get("snippet", "No summary available.")
        source = top_result.get("url", "")
        return {"output": summary, "source": source}
    else:
        return {"output": "No results found.", "source": ""}
```

Update `tools.json` accordingly for `web_search_tool`'s input/output. Also ensure the Research agent's prompt or output format might mention using the "source".

If not using an external API, you might choose to use the OpenAI API to do a web search by giving the model access to a plugin or by using the (beta) browsing. That can be complicated, so using a simple API as shown might be more straightforward for now.

#### Data Analysis Tool (`analyze_data_tool`)

Maybe this tool takes some data (or reference to data) and analyzes it. For instance:

```python
def analyze_data_tool(data: str) -> Dict[str, Any]:
    """
    Analyzes the given data (e.g., text or numbers) and returns insights.
    """
    # Dummy implementation: maybe count words or detect sentiment
    analysis = {}
    analysis['word_count'] = len(data.split())
    # You could integrate a sentiment model or custom logic here.
    return {"output": f"Analyzed data with {analysis['word_count']} words."}
```

This is simplistic, but you get the idea. Adapt the implementation to what you need (maybe this tool could parse a CSV, or do some calculations, etc., depending on your project).

After implementing and adjusting the tools, restart the server to load the new code. Try queries that force the agents to use these tools. For example:

- "Plan a meeting with John next Tuesday at 10 AM." The supervisor should route this to Planner Agent, which should then use `plan_event_tool` (and possibly `send_email_tool` if it decides to send an invite). You should see in the logs that those tools were invoked, and the response might combine their outputs.
- "Find me the capital of France." The supervisor should route to Research Agent, which would use `web_search_tool` to find information, and return the answer (e.g., "Paris") possibly with a source.

### Testing and Iteration

It's likely you'll need to iterate on prompts and tool implementations to get the desired behavior:

- If the agent isn't using a tool when it should, you might need to adjust the prompt to more strongly suggest the tool usage (or check that the tool is correctly listed in config and that the OpenAI model has function calling enabled)
- If the agent output is not formatted correctly or missing fields, make sure the output from your tool matches what the agent expects (and that the agent prompt knows how to format the final answer)
- Use the logs extensively. For instance, if the agent returned something odd, check `agent_logs.jsonl` to see what it was trying to do. You might find it attempted a tool call but maybe failed. Then check `tool_logs.jsonl` for that tool call, see the inputs it got. This will inform you whether the issue is in the prompt, the tool code, or elsewhere.

## 3. Using the Supervisor Agent

The Supervisor Agent is a central piece of this system's architecture. Let's delve deeper into how to use it effectively and understand its role.

### Role of the Supervisor

The supervisor agent acts as a gatekeeper and router:

- It receives every user query (when you use the UI or call the API with `agent_name` set to the supervisor)
- It analyzes the query in the context of what each specialized agent can do
- It decides which agent (or potentially multiple in sequence, though the default design is one agent per query) should handle the query
- It then formulates a request to that agent, including relevant context and the user's message, and waits for the result
- Finally, it returns that result back to the user (sometimes with minimal processing or formatting)

In our configuration, the supervisor's decision is primarily guided by the list of agents in `nodes.json` (which agents exist) and its prompt in `openai_config.json`. The prompt is something like "Your job is to decide which agent to call based on the user's input: '...'. Pass the context to the appropriate agent. Do not respond yourself." This means the LLM (GPT-4 or whichever model you chose) will actually output which agent it thinks is best suited. The `agent_dispatcher.py` likely reads that output and then invokes the chosen agent accordingly.

### Using the Supervisor in Practice

When building a user-facing application, you will almost always want to send user queries to the supervisor. That gives you the flexibility to have multiple agents and let the system decide the best one to use. The user doesn't have to choose the agent; they just ask a question or give a command, and the behind-the-scenes orchestration happens automatically.

For example, if you had a chat assistant built with this system:

- The user types: "Could you find me some recent articles on climate change and schedule a meeting to discuss them next week?"
- This query has two parts: information gathering (articles on climate change) and scheduling a meeting
- The supervisor might split this into two decisions or pick one agent to start with. It's possible the template's out-of-the-box logic might not handle a request that complex perfectly (it might choose one agent and ignore the second part unless programmed for multi-step reasoning)
- However, an advanced approach could be: Supervisor sees "find articles" and "schedule meeting". It might first route to the Research Agent for the first part. After getting info, it could route to Planner Agent for the second part. Achieving this might require the supervisor to iterate or you to implement a chaining mechanism. By default, it likely picks just one agent. In our case, maybe it sees "articles" and chooses ResearchAgent, which returns some article summaries. If the user then says "Great, now schedule a meeting next Tuesday to discuss", that second request would be routed to PlannerAgent.

The key point is, by using the supervisor, your system can gracefully handle whatever the user asks by delegating to the right component.

### Direct Agent Use Cases

There are scenarios, especially in testing or if you expose a developer API, where calling an agent directly might make sense. For instance, if you want to build a UI where an expert user can specifically query the ResearchAgent ("just search the web for X, I don't need planning"), you could allow direct queries to that agent. The included web UI actually allows selecting a specific agent, which is useful for debugging or specific control. But in a polished production setting, you'd usually hide that and have the logic auto-select.

### Fine-Tuning Supervisor Decisions

If you find the supervisor sometimes chooses the wrong agent for a given query, you have a few options:

**Improve the prompt**: Add more guidance in the supervisor's `input_template`. For example, explicitly list keywords or scenarios: "If the query involves searching information or asking questions, choose the ResearchAgent. If it involves scheduling, planning, or actions like sending emails, choose the PlannerAgent." The LLM will then better understand the criteria.

**Tool signals**: The way the system is set up, the supervisor might actually be implemented by giving the LLM "functions" corresponding to each agent (similar to how we give tools to agents). If so, it might be choosing by deciding to "call" an agent-function. Ensure the descriptions of those "agent functions" (likely derived from the agent descriptions in `nodes.json`) are clear. E.g., if ResearchAgent's description is "Handles analysis, triage, or research", you might refine that to "Handles questions that involve looking up information or analyzing data".

**Post-processing override**: If needed, you (as the developer) can always override the decision. For critical applications, you might not want an LLM to have full control of who handles what. You could implement rules in the `agent_dispatcher` code. For instance, a simple keyword route: if message contains "search" or "find" => ResearchAgent, if contains "schedule" or "email" => PlannerAgent. And otherwise fall back to the LLM's decision. This hybrid approach can combine deterministic safety with AI flexibility. However, implementing this requires modifying the Python code, and the template is your playground to do so if required.

In summary, using the supervisor is straightforward (just send all queries to it), but ensuring it routes queries correctly might take some iteration with prompts and possibly code. The template gives you a starting point that works for basic distinctions.

## 4. Deploying the FastAPI Web Interface

Thus far, we've been running the app in development mode on our local machine. To make this system available to end users or a larger audience, you'll want to deploy it.

The web interface (both the API and the basic HTML page) is built with FastAPI, which is production-ready and can be deployed to many environments (cloud servers, container platforms, etc.). Here are some guidelines for deploying:

### Using Uvicorn/Hypercorn in Production

In development we used:

```bash
python web/main.py
```

This is convenient, but in production, you'll likely run Uvicorn (or another ASGI server like Hypercorn or Gunicorn with uvicorn workers) more directly and probably behind a process manager or inside a container.

For example, using Uvicorn via command line:

```bash
uvicorn planner_bot.web.main:app --host 0.0.0.0 --port 8000 --workers 4
```

This command will serve the app on all network interfaces (so it's accessible externally if the port is open) and use 4 worker processes to handle requests (taking advantage of multiple CPU cores). Adjust the number of workers based on your machine.

If using Gunicorn, you might do:

```bash
gunicorn -k uvicorn.workers.UvicornWorker planner_bot.web.main:app --workers 4 --bind 0.0.0.0:8000
```

Both achieve similar outcomes. The key is to have a process manager keep these running (if deploying manually on a VM, something like systemd or supervisor can ensure the process stays up).

### Environment Configuration for Deployment

Make sure to set environment variables in the production environment:

- The `OPENAI_API_KEY` and other secrets should be provided in a secure manner. If using a cloud service, use their secret management. If using Docker, pass them in via `-e` or docker compose.
- If you plan to connect to a database or other services, ensure those credentials/URLs are set as well.

### Dockerizing (Optional)

A common approach is containerization. You could create a Dockerfile for the project. For instance:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Expose port (if needed for documentation; actual publish in run command)
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "planner_bot.web.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build this with:

```bash
docker build -t planner-bot-app .
```

Run it with:

```bash
docker run -d -p 8000:8000 -e OPENAI_API_KEY=<key> -e OPENAI_MODEL=<model> planner-bot-app
```

Now your app is running in a container, accessible on port 8000. Make sure to include any other environment variables or files (like if you rely on `.env`, you might copy it or use `-e` flags).

### Scalability Considerations

**State**: The app itself is stateless (each request is independent, except for logs written to disk). If you scale to multiple instances (containers or processes), be mindful that logs will be separate per instance unless you centralize them. Also, if you add a database for memory, that becomes a point of coordination.

**Concurrency**: Each Uvicorn worker can handle many concurrent requests (the heavy lifting is the OpenAI API calls, which are I/O bound, so async concurrency helps). By default, the template likely uses async calls to OpenAI via LangChain, which is good. If using CPU-bound tools or long in-Python processing, consider offloading those to background threads or processes.

**Timeouts**: In production, you might want to enforce a timeout on agent responses (so one query doesn't hang forever). Uvicorn/Gunicorn can have timeouts, and OpenAI calls can accept a timeout parameter. Consider setting these to reasonable values.

### Web Interface Improvements

The provided HTML page is very basic. For a polished deployment, you might want to create a nicer UI:

- You could build a single-page application (SPA) with React/Vue/Angular that communicates with the FastAPI backend
- Or enhance the Jinja2 template with better styling (maybe using Bootstrap) and make it a simple chat UI
- Make sure to handle streaming responses or loading indicators as needed (especially if some queries take a while due to external API calls)

For internal or admin use, the basic interface might be fine. For a public product, investing in a better UI/UX is worthwhile.

### Security

If deploying publicly:

- Add proper authentication if needed. As is, the API is open (which might be fine for a free tool, but not if misuse is a concern)
- Consider rate limiting or usage tracking, especially since each request potentially uses OpenAI credits. You don't want someone spamming your endpoint and running up a huge bill. Tools like FastAPI's slowapi or an API gateway can enforce limits
- Use HTTPS (either run behind a reverse proxy like Nginx/Traefik or use something like Uvicorn behind an SSL-terminating load balancer)
- Keep your OpenAI API key safe. On the server, it should be an environment variable. Do not expose it to the client-side

Once deployed, monitor the application. Use the logs (you might push them to a service or at least watch them) to see usage patterns and errors.

## 5. Integration with OpenAI

We've touched on this in various sections, but let's focus on the OpenAI integration aspects specifically, to ensure everything is clear and you're making the most of it.

### Setting Up OpenAI Credentials

By now, you should have set `OPENAI_API_KEY` in your environment. The template likely uses `openai` Python package to call the API. If your key is loaded in the env, it will pick it up (OpenAI's library can auto-read `OPENAI_API_KEY` or you might see code that explicitly loads it via the `config.py` utility).

If you have multiple OpenAI accounts or keys, just ensure the one you're using has access to the models you want (e.g., GPT-4 is still limited to certain users or requires a request for access).

### Choosing the Right Model

In `OPENAI_MODEL` you specify which model to use for all agents (unless overridden in config).

- For many tasks, `gpt-3.5-turbo-0613` (the version with function calling support) is a good starting point. It's fast and cost-effective
- If you need better reasoning, `gpt-4-0613` is more reliable but slower and more expensive
- You can also experiment with other models (or even open-source ones via LangChain, though the template is geared towards OpenAI out-of-the-box). The LangChain integration means you could swap in, say, an Anthropic model or others by adjusting code, but that's beyond this tutorial's scope

To set a different model per agent, you can replace `${OPENAI_MODEL}` in `openai_config.json` with a specific model name string for each agent. For example, maybe:

```json
"supervisor_agent": { "model": "gpt-4-0613", ... },
"planner_agent": { "model": "gpt-3.5-turbo-0613", ... },
"research_agent": { "model": "gpt-3.5-turbo-0613", ... }
```

This uses GPT-4 for the supervisor (ensuring the best reasoning for routing), and GPT-3.5 for the worker agents to save costs.

### Function Calling Mechanism

The template heavily uses OpenAI's function calling. Here's how it works in context:

- We define functions (tools) in our code
- We define their interface (name, description, parameters) in `tools.json`
- LangChain/LangGraph takes those and, when sending a prompt to the OpenAI model, it includes these as available "functions" the model can choose to call
- The model, if it decides a tool is needed, will respond with a special message indicating a function call (including the function name and arguments)
- The LangChain/agent executor sees this and actually calls the corresponding Python function (the one we implemented)
- The function returns a result (which we often format as a JSON with an "output" field)
- The agent then gets that result and continues the conversation (e.g., it may incorporate the result into its final answer to the user)
- Finally, the agent returns an answer (often after possibly using multiple tools in sequence)

For example, if the user asks "What's 5+5?" and there's a calculator tool:

- The agent's LLM sees it could just answer or use the calculator function
- If prompt told it that using calculator is preferred for accuracy, it might respond with a function call `calculator_tool` with arguments `{"expression": "5+5"}`
- Our system calls `calculator_tool` Python function, gets result `{"output": 10}`
- The LLM then gets to see that result and might respond with "The result is 10."

Understanding this helps when debugging. If an agent isn't using a tool you expect, either it didn't think it needed it, or maybe the tool wasn't properly defined. Check that the name in `tools.json` exactly matches the function name and that it's listed in the agent's tools list.

### Moderation and Safety

The `tools/common/utils/moderation.py` suggests there's a content moderation step. Often, developers incorporate a check using OpenAI's Moderation API to filter out disallowed content. If a user inputs something against policy (e.g., hate speech, requests for illicit behavior), you might want the agent to refuse or a filter to block it.

The template likely has something like:

- Before sending a user query to OpenAI, call moderation API. If flagged, either modify the prompt or refuse
- After getting a response, maybe check it as well

If your use case is sensitive or public-facing, ensure to test and possibly strengthen these moderation steps. It's both for compliance with OpenAI's terms and to avoid bad outputs to users.

### Costs and Monitoring Usage

Using OpenAI's API costs money per token. Keep track of how many tokens your application is using:

- Each request might involve the system prompt, user message, and tool/function definitions (which can be many tokens if you have lots of tools)
- Each tool function call also incurs additional prompts and responses
- If an agent loops or tries multiple tools, tokens add up

OpenAI provides usage dashboards, or you can integrate with their usage API. The template's logging of events with timestamps can help you calculate approximate tokens (if you log the prompt content and response length, etc., though it currently logs only a summary).

If this is a hobby project, set some monthly budget and monitor. If it's for a business, consider strategies to optimize:

- Use cheaper models when appropriate
- Limit the length of outputs or the number of steps an agent can take
- Possibly implement caching for repeated questions or use retrieval augmentation to reduce calls

## 6. Logging and Monitoring Setup

Logging, as we have, is great for debugging. Monitoring is about keeping your system reliable and performant in production. Let's discuss a basic setup using what's provided and suggest enhancements:

### Built-in Logging Recap

**Agent Events**: Logged to `logs/agent_logs.jsonl`. Each event includes `agent_name`, `message` (the user's query to that agent), `context` (likely any additional context given, like tool outputs or prior conversation snippet), `output` (the agent's answer or decision), and timing info.

**Tool Events**: Logged to `logs/tool_logs.jsonl`. Includes `tool_name`, input request (arguments passed), response (the return from the function), and timing.

Since these are JSONL, you can load them into any log analysis tool or even a Pandas dataframe for analysis. For instance, you could periodically run a script to parse these and extract metrics: average tool call duration, which tools are used most, etc.

### Live Monitoring

For a more real-time monitor:

**Log streaming**: Use something like ELK stack (Elasticsearch, Logstash, Kibana) or any cloud logging service (like AWS CloudWatch, Loggly, etc.) to aggregate logs. Ship the JSONL entries to a dashboard where you can search and visualize them. This helps in quickly identifying issues (e.g., a spike in errors or an unusual pattern of usage).

**Metrics**: Decide on key metrics. Possibly: number of requests per minute, number of times each tool is used, average latency of responses, error rates. You can instrument these. For example, you could increment a counter every time `agent_dispatch` is called (count total queries). If using a tool like Prometheus, you would expose an endpoint with metrics or use pushgateway. Or simpler, use logs: count entries in `agent_logs` to derive how many queries, and subtract fails to get success count.

**Health checks**: Implement a simple endpoint like `/health` in FastAPI that returns OK, which you can use for uptime monitoring (some service pinging it periodically to ensure the app is responsive).

### Notifications and Alerts

For a production system, set up alerts for:

- When your OpenAI usage hits certain thresholds (OpenAI might allow setting soft limits)
- When the application returns errors above a certain rate (if many 500 responses or exceptions)
- When latency goes too high (if calls are taking too long, maybe OpenAI is slow or a tool is hanging)

While the template doesn't include a full monitoring solution, it lays the groundwork with logs. For serious deployments, consider integrating Sentry (for error tracking), Prometheus/Grafana (for metrics), or even LangChain's own LangSmith to monitor agent chains.

### Debugging in Depth

At times, you'll want to see exactly why an agent responded a certain way. Logs provide some info, but sometimes the raw prompt and the raw completion are needed:

- You could modify the code to log the full prompt that goes to OpenAI and the raw response (maybe with a debug log level). Be cautious with logging full content if it includes sensitive user data
- LangChain often has verbose settings or callback handlers. You could enable a LangChain tracer or their debug logging to get more insight
- If an agent is misbehaving, try replicating the prompt in the OpenAI playground or with a simplified script to see how it behaves, and adjust accordingly

### Maintenance

Over time, maintain your `logs/` directory. It will grow with each request. You might implement log rotation (maybe compress and archive logs daily, or clear out old logs after some time). The template isn't likely to have done that for you, so it's up to you to manage log size so you don't fill up disk space.

In summary, logging and monitoring might not be the most exciting part, but it is crucial for a reliable AI application. The provided logging is a great start. Augment it with external tools as needed for your use case.

## 7. Real-World Use Case Walkthroughs

To solidify our understanding, let's walk through a couple of example scenarios using the system. These will illustrate how the pieces come together for a practical task.

### Scenario 1: Personal Assistant for Scheduling and Information

**Use case**: You want an AI assistant that can handle both looking up information and scheduling tasks for you. For instance, planning a meeting and gathering relevant info for that meeting.

**Agents Setup**: You have a PlannerAgent (with tools to schedule and email) and a ResearchAgent (with tools to search info).

**User Query**: "Please find a good Italian restaurant in my area and schedule a dinner with my friend next Friday at 7 PM. Also, email me the restaurant details."

**Step 1 (Supervisor)**: The user sends this query. The supervisor agent receives it. The query actually has two distinct tasks (find restaurant info, and schedule a dinner + email details). The supervisor must decide which agent to handle it, or in an ideal situation, orchestrate both. The default supervisor might try to pick one agent. There's an ambiguity: it's both a research and a planning task. Depending on how we configured the prompts:

The supervisor might lean towards the PlannerAgent because "schedule a dinner" and "email me" sound like tasks.

Suppose it chooses PlannerAgent.

**Step 2 (PlannerAgent reasoning)**: The PlannerAgent gets the full query. Its prompt says it can plan events and send emails, and it has those tools. But it sees "find a good Italian restaurant" – that might require web search, which is not in its tools. The PlannerAgent might attempt to do it anyway; since it only has `plan_event_tool` and `send_email_tool`, it might not have the ability to search in its toolkit. It could respond with something general or, if designed well, it might realize "I don't have a web search, maybe I should defer this". However, the current template doesn't have a mechanism for agents to talk to each other directly.

If PlannerAgent tries to handle everything, it might produce an answer without actual info (maybe making something up, which isn't ideal).

Alternatively, if we had extended the logic, the supervisor could have broken it down (not default though).

**Potential Solution**: To handle complex multi-part queries like this, one approach is to require the user (or an intermediate step) to issue two queries: one to search, another to schedule. Or enhance the system such that the PlannerAgent could call the ResearchAgent as a tool (this is an advanced concept: an agent calling another agent, which can be done via a tool interface or orchestrator logic).

For now, assume the user asks one thing at a time.

**Revised Use case flow**:

The user first asks: "Find a good Italian restaurant in my area."

- Supervisor routes to ResearchAgent (seeing "find...restaurant")
- ResearchAgent uses `web_search_tool` with query "good Italian restaurant in [my area]"
- The tool returns maybe a list or a top result (e.g., "Luigi's Trattoria - 4.5 stars, location downtown")
- ResearchAgent responds: "I found a great Italian restaurant: Luigi's Trattoria, rated 4.5 stars, located downtown." (This is delivered to the user.)

The user then asks: "Schedule a dinner there with my friend next Friday at 7 PM and email me the details."

- Supervisor sees "schedule ... and email" -> routes to PlannerAgent
- PlannerAgent receives the request. It might not know the previous conversation (unless we implemented memory), so the user would need to specify "there" refers to Luigi's Trattoria, or ideally we have conversation context. Let's assume context was maintained or the user said "at Luigi's Trattoria"
- PlannerAgent uses `plan_event_tool` to add the event (maybe it just pretends or uses an API)
- It then uses `send_email_tool` to send details (to user's email, which maybe it knows from `identifier` or user profile)
- The agent then outputs: "I have scheduled a dinner at Luigi's Trattoria for next Friday at 7 PM and sent you an email with the details."

This response goes to the user. The logs show two tool uses for that query.

This scenario shows a multi-step interaction where each agent shines in its area. It highlights the need for either memory or the user to break down queries. In current form, our system doesn't carry over information between calls (unless we code it to do so). So instructing users (or designing a UI) to handle one task per query might be necessary or implement a context passing.

### Scenario 2: IT Support Bot

Imagine using this template to build an IT support assistant that:

- One agent can troubleshoot issues (through a Q&A knowledge base or scripted logic)
- Another agent can perform actions like creating a ticket or resetting a password via tools

Let's say:

- **Agent One**: TroubleshooterAgent (tools: maybe a knowledge base search, or just rely on the LLM knowledge)
- **Agent Two**: OpsAgent (tools: `reset_password_tool`, `create_ticket_tool`)
- The supervisor will decide if the user is asking a question (likely troubleshooting) vs asking for an action to be done

**User Query**: "My internet is slow and I keep disconnecting from VPN. What can I do?"

- **Supervisor**: sees a problem description -> routes to TroubleshooterAgent
- **TroubleshooterAgent**: maybe uses a knowledge base tool to search company docs or, if none, just uses LLM knowledge. It responds with some advice: "It could be due to X, try Y. If the issue persists, we can reset your VPN credentials."

The user then says: "Can you reset my VPN account? My username is john_doe."

- **Supervisor**: sees "reset ... account" -> routes to OpsAgent
- **OpsAgent**: uses `reset_password_tool` with user "john_doe". That tool might call an internal API to reset the password (or for demo, just returns a dummy new password)
- **OpsAgent** returns: "I've reset your VPN password and emailed the new credentials to your registered email."
- Meanwhile, the tool might also trigger the email (if implemented)

The interaction shows how two different agents handle different aspects (one purely informational, one action-oriented).

This scenario demonstrates a clear separation: the user query determines which route. It also shows how you might incorporate actual business logic (integrating with IT systems via tools).

### Key Takeaway

In a real-world deployment, you'll likely script or guide the user through interactions that align with the agent capabilities. The more you expand the system (more agents, more tools), the more flexible it becomes. But complexity grows, so test thoroughly each addition. The template is a starting structure - building a full product requires thinking through flows like these and possibly adding supporting infrastructure (like databases for knowledge or context, authentication for secure actions, etc.).

## Conclusion

In this tutorial, we've covered the journey from starting a new project with the Cookiecutter Agentic AI Template to customizing it and deploying a functional multi-agent AI application. Let's recap the major points:

**Installation and Setup**: Using Cookiecutter to generate the project, installing dependencies, and configuring environment variables (especially for OpenAI access).

**Project Structure**: Understanding how the template organizes code, with separation of agents, tools, configs, and the web interface. This structure is key to maintainability as you expand your project.

**Customization**: Adapting the generic template to a real use case by editing prompts, implementing tool logic, adding new tools or agents, and fine-tuning the agent behaviors. This is where your project becomes unique and valuable.

**Using the System**: Relying on the supervisor agent to route tasks, and knowing how to interact via the web UI or API. We emphasized that typically users will go through the supervisor for a seamless experience.

**FastAPI Deployment**: Running the web app locally and considerations for deploying it to production, including using Uvicorn/gunicorn, Docker, and ensuring security and scalability.

**OpenAI Integration**: Managing API keys, choosing models, and leveraging function calling to enable tool usage. Also, handling moderation and keeping an eye on costs.

**Logging & Monitoring**: Utilizing the built-in logging for debugging and setting up monitoring to keep your system reliable in the long run. This included suggestions for analyzing logs and getting alerts on issues.

**Examples**: We walked through hypothetical scenarios to illustrate how the agents and tools could work together to solve user requests in the real world, highlighting the strengths of the multi-agent approach as well as its current limitations (like lack of memory without further extension).

With this knowledge, you should be well-equipped to build upon the template. Here are some next steps and tips as you continue your development:

- **Start simple**: implement a basic version of your target use case with minimal tools, ensure it works end-to-end, then iterate
- **Test often**: use the provided tests and add more. For each new tool or agent, write a test for it. This saves time in the long run
- **Keep the user in mind**: how will they interact with this system? Do they need a more elaborate UI or instructions? Maybe integrate this into a chat platform (Slack, etc.) using the API
- **Stay updated**: The AI field moves fast. New OpenAI model versions or LangChain/LangGraph improvements could benefit your project. Keep an eye on those libraries' release notes for features like better function calling support or new agent patterns
- **Optimize prompts**: A lot of the "magic" comes from prompt engineering. Don't hesitate to refine the prompts in `openai_config.json` as you see how the AI behaves. Small changes in wording can lead to big differences in results.

We hope this tutorial has been helpful. Building agentic AI systems can be challenging, but with the right structure and tools, it becomes an achievable task. Good luck with your project, and happy coding!
