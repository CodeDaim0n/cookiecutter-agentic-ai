# Agentic AI CookieCutter Template

A powerful cookiecutter template for creating agentic AI systems with multiple agents, tools, and a web interface. Developed by Anjali Jain.

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

1. Install cookiecutter:
```bash
pip install cookiecutter
```

2. Create a new project:
```bash
cookiecutter https://github.com/yourusername/cookiecutter-agentic-ai-final
```

3. Follow the prompts to configure your project:
   - `project_name`: Name of your project
   - `supervisor_name`: Name of the supervisor agent
   - `agent_one_name`: Name of the first agent
   - `agent_two_name`: Name of the second agent
   - `agent_one_tool_one`: Name of the first tool for agent one
   - `agent_one_tool_two`: Name of the second tool for agent one
   - `agent_two_tool_one`: Name of the first tool for agent two
   - `agent_two_tool_two`: Name of the second tool for agent two

4. Navigate to your project directory and install dependencies:
```bash
cd your-project-name
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