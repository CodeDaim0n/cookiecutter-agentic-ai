# tools/common/utils/responder.py

from tools.openai.response_engine import OpenAIResponder

# Initialize responder instance with config
responder = OpenAIResponder(config_path="config/openai_config.json")
