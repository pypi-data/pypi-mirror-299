#!/usr/bin/env python3

import os
import sys
from toml_cfg_tool.src.cli import parse_arguments
from toml_cfg_tool.src.bkup import backup_file
from toml_cfg_tool.src.creation import create_setup_cfg_template, create_pyproject_toml_template, create_workflow_files, get_github_repo_url
from toml_cfg_tool.src.color_codes import BOLD, LINK, CYAN
from toml_cfg_tool.src.print_colors import print_two_colors
from toml_cfg_tool.src.updates_cfg import update_setup_cfg
from toml_cfg_tool.src.updates_toml import update_pyproject_toml
from toml_cfg_tool.src.contrib import create_contrib_file
from toml_cfg_tool.src.reader import print_updateable_values 
from pathlib import Path

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_terminal()
    args = parse_arguments()

    print_two_colors(BOLD, CYAN, "Welcome to the toml_cfg_tool!", "This tool is designed to help you manage your project's setup.cfg and pyproject.toml files")

    if args.update_github:
        print_two_colors(BOLD, LINK, "Updating GitHub repository with new values")
        repo_url = get_github_repo_url()
        print_two_colors(BOLD, LINK, "GitHub repository found, updating cfg and toml files to match:", repo_url)
    else:
        repo_url = None
    
    root_dir = Path.cwd()
    if args.show:
        print_updateable_values(root_dir)
        sys.exit(0)

    if args.create_contrib:
        create_contrib_file()

    if args.backup:
        file_path = args.backup 
        backup_file(file_path)

    updates = {}
    if args.author:
        updates['author'] = args.author
    if args.name:
        updates['name'] = args.name
    if args.version:
        updates['version'] = args.version
    if args.description:
        updates['description'] = args.description
    if args.requires_python:
        updates['requires-python'] = args.requires_python
    if args.license:
        updates['license'] = args.license

    if not args.workflow_files:
        pass
    else:
        create_workflow_files()

    if not updates and not args.create_templates:
        sys.exit(0)
    
    files = ["setup.cfg", "pyproject.toml"]
    
    for file in files:
        if args.create_templates:
            if file.endswith(".cfg"):
                create_setup_cfg_template(file, dry_run=args.dry_run, update_github=args.update_github)
            elif file.endswith(".toml"):
                create_pyproject_toml_template(file, dry_run=args.dry_run, update_github=args.update_github)
        
        if os.path.exists(file) and updates:
            print_two_colors(BOLD, LINK, "Updating the following file:", file)
            
            if file.endswith(".cfg"):
                update_setup_cfg(file, repo_url, updates, dry_run=args.dry_run, backup=args.backup, update_github=args.update_github)
            
            elif file.endswith(".toml"):
                update_pyproject_toml(file, repo_url, updates, dry_run=args.dry_run, backup=args.backup, update_github=args.update_github)
        
        elif not os.path.exists(file):
            if not args.create_templates:
                print(f"File not found: {file}\n")

if __name__ == "__main__":
    main()

