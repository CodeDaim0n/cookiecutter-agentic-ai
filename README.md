# Agentic AI Template

A powerful template for creating agentic AI systems with multiple agents, tools, and a web interface. Developed by Anjali Jain.

## Features

- Multiple AI agents with different capabilities
- Supervisor agent for routing and coordination
- Customizable tools for each agent
- Web interface with FastAPI
- OpenAI integration
- Structured project layout
- Type hints and documentation
- Logging and monitoring

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/CodeDaim0n/cookiecutter-agentic-ai
cd cookiecutter-agentic-ai
```

2. Run the template processor:
```bash
python replace_cookiecutter.py
```

3. Follow the prompts to provide values for each variable. You can:
   - Press Enter to use the default value
   - Type a new value to override the default

Example:
```
Please provide values for the following variables:
(Press Enter to use default value if available)

Enter value for project_name (default: my-agentic-ai): restaurant_agentic-ai
Enter value for supervisor_name (default: supervisor_agent): supervisor_agent
Enter value for agent_one_name (default: agent_one): customer_support_agent
Enter value for agent_two_name (default: agent_two): kitchen_agent
Enter value for agent_one_tool_one (default: agent_one_tool_one): upsert_customer
Enter value for agent_one_tool_two (default: agent_one_tool_two): upsert_order
Enter value for agent_two_tool_one (default: agent_two_tool_one): get_reciepe
Enter value for agent_two_tool_two (default: agent_two_tool_two): prepare_order
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other configurations
```

6. Run the development server:
```bash
python web/main.py
```

## Project Structure

```
your-project-name/
├── agents/                 # Agent implementations
│   └── core/
│       └── langgraph/     # LangGraph-based agent implementations
├── config/                # Configuration files
├── database/             # Database migrations and schemas
├── logs/                 # Application logs
├── tools/                # Tool implementations
│   ├── common/           # Common utilities
│   └── your-project-name/ # Project-specific tools
├── web/                  # Web interface
│   └── templates/        # HTML templates
└── tests/               # Test files
```

## Development

### Adding New Tools

1. Create a new tool file in `tools/your-project-name/`
2. Add tool configuration to `config/tools.json`
3. Update agent configurations in `config/nodes.json`

### Adding New Agents

1. Create agent implementation in `agents/core/langgraph/`
2. Add agent configuration to `config/nodes.json`
3. Update supervisor routing if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Developed by Anjali Jain 