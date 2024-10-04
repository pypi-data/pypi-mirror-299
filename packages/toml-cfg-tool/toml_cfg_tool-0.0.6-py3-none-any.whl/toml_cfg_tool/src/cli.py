# ./src/cli.py 
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Update metadata fields in setup.cfg and pyproject.toml or create template files, including GitHub Actions workflow files...")
    
    parser.add_argument("--author", type=str, help="Update the project author.")
    parser.add_argument("--name", type=str, help="Update the project name.")
    parser.add_argument("--version", type=str, help="Update the project version.")
    parser.add_argument("--description", type=str, help="Update the project description.")
    parser.add_argument("--requires-python", type=str, help="Update the required Python version.")
    parser.add_argument("--license", type=str, help="Update the project license.")
    parser.add_argument("--workflow_files", action="store_true", help="Add GitHub Actions workflow files, and scripts.")
    parser.add_argument("--create-templates", action="store_true", help="Create template setup.cfg and pyproject.toml files if they do not exist.")
    parser.add_argument("--create-contrib", action="store_true", help="Create a CONTRIBUTING.md file if it does not exist.")
    parser.add_argument("--backup", action="store_true", help="Backup existing configuration files before making changes.")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing to files.")
    parser.add_argument("--show", action="store_true", help="Show the current configurations that the script can update.")
    
    return parser.parse_args()

