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

### Option 1: Using the Template Processor (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/CodeDaim0n/cookiecutter-agentic-ai
cd cookiecutter-agentic-ai
```

2. Edit `cookiecutter.json` with your desired values:
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

3. Copy the template processor script:
```bash
cp replace_cookiecutter.py ..
cd ..
```

4. Run the template processor from the parent directory:
```bash
python replace_cookiecutter.py
```

The script will:
- Find the template directory
- Replace all cookiecutter variables in files and folder names
- Rename the project directory to your specified name

5. Install dependencies:
```bash
cd your-project-name
pip install -r requirements.txt
```

6. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other configurations
```

7. Run the development server:
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