# ./src/updates_cfg.py 
import configparser 
import os 
import shutil 
from toml_cfg_tool.src.bkup import backup_file
from toml_cfg_tool.src.color_codes import BOLD, CYAN, LINK, ORANGE, END
from toml_cfg_tool.src.print_colors import print_two_colors
from toml_cfg_tool.src.creation import get_github_repo_url

def update_setup_cfg(file_path, updates, dry_run=False, backup=False):
    
    repo_url = get_github_repo_url()
    if "github.com" in repo_url:
        config = configparser.ConfigParser()
        config.read(file_path)
        config['metadata']['url'] = repo_url
        with open(file_path, 'w') as f:
            config.write(f)
        print_two_colors(BOLD, LINK, "Updated setup.cfg with GitHub repository URL:", repo_url)
    
    if backup:
        backup_file(file_path)
    
    config = configparser.ConfigParser()
    config.read(file_path)
    
    changed = False
    
    if 'metadata' not in config:
        config['metadata'] = {}
    
    metadata = config['metadata']
    if 'author' in updates:
        metadata['author'] = updates['author']
        changed = True
        
        print_two_colors(BOLD, CYAN, "Updating setup.cfg [metadata] author to:", updates['author'])

    if 'name' in updates:
        metadata['name'] = updates['name']
        changed = True
        
        print_two_colors(BOLD, CYAN, "Updating setup.cfg [metadata] name to:", updates['name'])
    
    if 'version' in updates:
        metadata['version'] = updates['version']
        changed = True
            
        print_two_colors(BOLD, CYAN, "Updating setup.cfg [metadata] version to:", updates['version'])
    
    if 'description' in updates:
        metadata['description'] = updates['description']
        changed = True
    
        print_two_colors(BOLD, CYAN, "Updating setup.cfg [metadata] description to:", updates['description'])
    
    if 'license' in updates:
        metadata['License-Expression'] = updates['license']
        changed = True
        
        print_two_colors(BOLD, CYAN, "Updating setup.cfg [metadata] License-Expression to:", updates['license'])

    if 'name' in updates:
        if 'options.entry_points' not in config:
            config['options.entry_points'] = {}
            
        options_entry_points = config['options.entry_points']
        options_entry_points['console_scripts'] = f"{updates['name']} = dir_with_entry_script.entry_script_name:main"
        changed = True
        
        print_two_colors(BOLD, CYAN, "Updating setup.cfg [options.entry_points] console_scripts to:", f"{updates['name']} = dir_with_entry_script.entry_script_name:main")
    
    if 'options' not in config:
        config['options'] = {}
    
    options = config['options']

    if 'requires-python' in updates:
        options['python_requires'] = updates['requires-python']
        changed = True
        
        print_two_colors(BOLD, CYAN, "Updating setup.cfg [options] python_requires to:", updates['requires-python'])
    
    if changed:
        if dry_run:
            print("{BOLD}Dry run enabled. No changes made to setup.cfg.{END}\n")
        else:
            try:
                with open(file_path, 'w') as configfile:
                    config.write(configfile)
                print(f"{BOLD}setup.cfg updated.{END}\n")
            except Exception as e:
                print(f"{ORANGE}Error updating setup.cfg:{END}{BOLD} {e}{END}\n")
    else:
        print(f"{BOLD}No changes needed in setup.cfg{END}\n")
