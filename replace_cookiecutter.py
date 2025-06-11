import json
import os
import re
import shutil
import sys

def debug_print(message):
    print(f"[DEBUG] {message}")

def find_template_directory():
    debug_print("Looking for template directory")
    current_dir = os.getcwd()
    debug_print(f"Current directory: {current_dir}")
    
    # Look for directory containing cookiecutter.json
    for root, dirs, files in os.walk(current_dir):
        if "cookiecutter.json" in files:
            debug_print(f"Found cookiecutter.json in: {root}")
            return root
    
    debug_print("No cookiecutter.json found in current directory or subdirectories")
    return None

def load_variables_from_json(template_dir):
    json_path = os.path.join(template_dir, "cookiecutter.json")
    debug_print(f"Loading variables from: {json_path}")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            variables = json.load(f)
        debug_print(f"Loaded variables: {variables}")
        return variables
    except Exception as e:
        debug_print(f"Error loading cookiecutter.json: {type(e).__name__}: {str(e)}")
        print("Error: Could not load cookiecutter.json")
        sys.exit(1)

def replace_in_string(s, variables):
    debug_print(f"Replacing variables in string: {s[:100]}...")
    # Only replace {{ cookiecutter.variable_name }} format
    pattern = re.compile(r"\{\{\s*cookiecutter\.([a-zA-Z0-9_]+)\s*\}\}")
    matches = pattern.findall(s)
    if matches:
        debug_print(f"Found variables to replace: {matches}")
    result = pattern.sub(lambda m: str(variables.get(m.group(1), m.group(0))), s)
    if result != s:
        debug_print(f"String was modified. Before: {s[:100]}... After: {result[:100]}...")
    return result

def replace_vars_in_file(filepath, variables):
    debug_print(f"\nProcessing file: {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        debug_print(f"File content length: {len(content)} characters")
        
        new_content = replace_in_string(content, variables)
        if new_content != content:  # Only write if changes were made
            debug_print(f"Changes detected in {filepath}")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
            # Print the changes for debugging
            print("Changes made:")
            for var_name, value in variables.items():
                if f"{{{{ cookiecutter.{var_name} }}}}" in content:
                    print(f"  - Replaced {{{{ cookiecutter.{var_name} }}}} with {value}")
        else:
            debug_print(f"No changes needed in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        debug_print(f"Exception details: {type(e).__name__}: {str(e)}")

def process_directory(root, variables):
    debug_print(f"\nStarting to process directory: {root}")
    if not os.path.exists(root):
        debug_print(f"Directory does not exist: {root}")
        print(f"Error: Directory {root} does not exist!")
        return

    debug_print(f"Variables available: {variables}")
    
    # First, rename files and directories (bottom-up to avoid path issues)
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        debug_print(f"\nProcessing directory: {dirpath}")
        debug_print(f"Found directories: {dirnames}")
        debug_print(f"Found files: {filenames}")
        
        # Rename files
        for filename in filenames:
            debug_print(f"\nProcessing file: {filename}")
            new_filename = replace_in_string(filename, variables)
            if new_filename != filename:
                debug_print(f"Renaming file: {filename} -> {new_filename}")
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {str(e)}")
                    debug_print(f"Exception details: {type(e).__name__}: {str(e)}")
        
        # Rename directories
        for dirname in dirnames:
            debug_print(f"\nProcessing directory: {dirname}")
            new_dirname = replace_in_string(dirname, variables)
            if new_dirname != dirname:
                debug_print(f"Renaming directory: {dirname} -> {new_dirname}")
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {str(e)}")
                    debug_print(f"Exception details: {type(e).__name__}: {str(e)}")
    
    # Now, replace in file contents
    debug_print("\nStarting to process file contents")
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Only process text-like files
            if filename.endswith(('.py', '.json', '.md', '.txt', '.yaml', '.yml', '.html')):
                debug_print(f"Found text file to process: {filepath}")
                replace_vars_in_file(filepath, variables)

if __name__ == "__main__":
    debug_print("Script started")
    debug_print(f"Current working directory: {os.getcwd()}")
    
    # Find the template directory
    template_dir = find_template_directory()
    if not template_dir:
        print("Error: Could not find template directory (directory containing cookiecutter.json)")
        sys.exit(1)
    
    debug_print(f"Found template directory: {template_dir}")
    
    # Load variables from cookiecutter.json
    variables = load_variables_from_json(template_dir)
    
    # Create new project directory
    new_project_dir = variables["project_name"]
    parent_dir = os.path.dirname(template_dir)
    new_path = os.path.join(parent_dir, new_project_dir)
    
    debug_print(f"Creating new project directory: {new_path}")
    try:
        # Copy the template directory to the new location
        shutil.copytree(template_dir, new_path)
        print(f"Created new project directory: {new_project_dir}")
        
        # Process the new directory
        debug_print("Processing new project directory")
        process_directory(new_path, variables)
        
        print("\nTemplate variables replaced in file/folder names and contents!")
        print(f"\nYour new project is ready at: {new_path}")
        print("\nNext steps:")
        print("1. cd into your new project directory")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Set up your environment variables")
        print("4. Run the development server: python web/main.py")
        
    except Exception as e:
        debug_print(f"Error during directory creation: {type(e).__name__}: {str(e)}")
        print(f"Error creating project directory: {str(e)}")
        sys.exit(1) 