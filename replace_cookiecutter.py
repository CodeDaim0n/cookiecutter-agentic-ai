import json
import os
import re
import shutil

def get_user_input(variable_name, default_value=None):
    prompt = f"Enter value for {variable_name}"
    if default_value:
        prompt += f" (default: {default_value})"
    prompt += ": "
    
    value = input(prompt).strip()
    return value if value else default_value

def replace_in_string(s, variables):
    pattern = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")
    return pattern.sub(lambda m: str(variables.get(m.group(1), m.group(0))), s)

def replace_vars_in_file(filepath, variables):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = replace_in_string(content, variables)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

def process_directory(root, variables):
    # First, rename files and directories (bottom-up to avoid path issues)
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        # Rename files
        for filename in filenames:
            new_filename = replace_in_string(filename, variables)
            if new_filename != filename:
                os.rename(
                    os.path.join(dirpath, filename),
                    os.path.join(dirpath, new_filename)
                )
        # Rename directories
        for dirname in dirnames:
            new_dirname = replace_in_string(dirname, variables)
            if new_dirname != dirname:
                os.rename(
                    os.path.join(dirpath, dirname),
                    os.path.join(dirpath, new_dirname)
                )
    # Now, replace in file contents
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Only process text-like files
            if filename.endswith(('.py', '.json', '.md', '.txt', '.yaml', '.yml', '.html')):
                replace_vars_in_file(filepath, variables)

def collect_variables():
    variables = {}
    print("\nPlease provide values for the following variables:")
    print("(Press Enter to use default value if available)\n")
    
    # Define default variables
    default_vars = {
        "project_name": "my-agentic-ai",
        "supervisor_name": "supervisor_agent",
        "agent_one_name": "agent_one",
        "agent_two_name": "agent_two",
        "agent_one_tool_one": "agent_one_tool_one",
        "agent_one_tool_two": "agent_one_tool_two",
        "agent_two_tool_one": "agent_two_tool_one",
        "agent_two_tool_two": "agent_two_tool_two"
    }
    
    for var_name, default_value in default_vars.items():
        value = get_user_input(var_name, default_value)
        variables[var_name] = value
    
    return variables

if __name__ == "__main__":
    # Get values from user
    variables = collect_variables()
    
    # Process the current directory
    process_directory(".", variables)
    print("\nTemplate variables replaced in file/folder names and contents!") 