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

### 1. Clone the repository:
```bash
git clone https://github.com/CodeDaim0n/cookiecutter-agentic-ai
cd cookiecutter-agentic-ai
```

 ### 2. Edit `cookiecutter.json` with your desired values:
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

Copy the template processor script:
```bash
cp replace_cookiecutter.py ..
cd ..
```

 Run the template processor from the parent directory:
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
- `OPENAI_MODEL` – the model ID you want to use (e.g. gpt-4o or gpt-4o-mini, preferably one that supports function calling for tool use)
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

In the `tools/your_project_name/` directory, you'll find Python files for each tool. Initially, these may be stubs with function definitions. You should edit these files and implement the actual logic. For example, you have a mcp.py which includes `send_email` function, via zapier mcp. If you have a `openai_web_search_tool.py`to use OpenAI's built-in browsing (if available).

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

**Model Choice**: In your `.env` (or directly in `openai_config.json`), set which model to use. GPT-4o tends to be more capable, especially for complex reasoning and understanding when to use tools, whereas GPT-4o-mini (with function calling) is faster and cheaper . You could use GPT-4o for the supervisor and GPT-4o-mini for the worker agents if cost is a concern, by specifying different model values for each agent in `openai_config.json`.

**Temperature and Other Parameters**: The template expose some of these in openai_config, but you can certainly adjust how "creative" or deterministic the AI responses are by setting the temperature, max tokens, etc. If using LangChain, these could be set in the agent builder or the prompt configuration. For instance, you could modify the code in `prompt.py` or the LangChain ChatOpenAI instantiation to set `temperature=0` for the supervisor (to make it deterministic) and a higher value for a creative agent, etc.

**Rate Limits and API Keys**: If you expect high volume usage, consider OpenAI rate limits. You might implement retries or handling for rate limit errors in the prompt utilities.I haven't parameterised it but pkan to do it in future.These are advanced topics, but keep them in mind as you scale.

### Logging and Monitoring

Logging is already enabled in the template. All agent events are logged to files. Here are some tips for using this for monitoring:

**Viewing Logs**: As mentioned, you can tail the JSONL files or write a simple script to parse and aggregate them. They contain timestamps and durations which can help identify performance bottlenecks (e.g., if a certain tool call is slow or if an agent is taking a long time to respond).

**Expanding Logging**: You can add additional logging in your own code as needed. For example, if you want to log when an agent makes a certain decision or if you want to log the content of messages for debugging, you can use the logging module. The `logger.py` sets up two loggers (`tool_logger` and `agent_logger`). You can use them or create new ones for different subsystems.

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
