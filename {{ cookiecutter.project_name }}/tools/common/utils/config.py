# tools/common/utils/config.py

import json
import os

def load_json_config(path: str) -> dict:
    """Load a JSON configuration file from the given path."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load config {path}: {e}")
        return {}
