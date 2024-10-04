# ./src/updates_cfg.py 
import configparser 
from toml_cfg_tool.src.bkup import backup_file
from toml_cfg_tool.src.color_codes import BOLD, CYAN, ORANGE, END
from toml_cfg_tool.src.print_colors import print_two_colors

def update_setup_cfg(file_path, repo_url, updates, dry_run=False, backup=False):
    
    from urllib.parse import urlparse
    parsed_url = urlparse(repo_url)
    if parsed_url.hostname and parsed_url.hostname.endswith("github.com"):
        config = configparser.ConfigParser()
        config.read(file_path)
        config['metadata']['url'] = repo_url
        with open(file_path, 'w') as f:
            config.write(f)
    
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

    if 'name' in updates:
        metadata['name'] = updates['name']
        changed = True
    
    if 'version' in updates:
        metadata['version'] = updates['version']
        changed = True
            
    if 'description' in updates:
        metadata['description'] = updates['description']
        changed = True
    
    if 'license' in updates:
        metadata['License-Expression'] = updates['license']
        changed = True
    
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
                # loop over items changed to True and print them with print_two_colors 
                for key, value in updates.items():
                    if key in ['author', 'name', 'version', 'description', 'license', 'requires-python']:
                        print_two_colors(BOLD, CYAN, f"Updated setup.cfg [metadata] {key} to:", value)
            except Exception as e:
                print(f"{ORANGE}Error updating setup.cfg:{END}{BOLD} {e}{END}\n")
    else:
        print(f"{BOLD}No changes needed in setup.cfg{END}\n")
