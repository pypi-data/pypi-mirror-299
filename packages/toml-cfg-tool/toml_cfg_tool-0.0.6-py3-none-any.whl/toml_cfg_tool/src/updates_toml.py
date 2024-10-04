# ./toml_cfg_tool/src/updates_toml.py 
import toml 
from toml_cfg_tool.src.bkup import backup_file
from urllib.parse import urlparse
from toml_cfg_tool.src.color_codes import BOLD, CYAN, ORANGE
from toml_cfg_tool.src.print_colors import print_two_colors


def update_pyproject_toml(file_path, repo_url, updates, dry_run=False, backup=False):
    
    parsed_url = urlparse(repo_url)
    hostname = parsed_url.hostname
    if hostname and (hostname == "github.com" or hostname.endswith(".github.com")):
        config = toml.load(file_path)
        config['project']['urls']['Homepage'] = repo_url
        with open(file_path, 'w') as f:
            toml.dump(config, f)
    
    if backup:
        backup_file(file_path)

    try:
        with open(file_path, 'r') as f:
            config = toml.load(f)
    except toml.TomlDecodeError as e:
        print_two_colors(ORANGE, BOLD, f"Error parsing {file_path}:", e)
        return
    except Exception as e:
        print_two_colors(ORANGE, BOLD, f"Failed to read {file_path}:", e)
        return

    project = config.get('project', {})
    changed = False

    if 'author' in updates:
        if 'authors' not in project:
            print_two_colors(ORANGE, BOLD, "Authors section not found in pyproject.toml", "Creating new section.")
            project['authors'] = {'name': updates['author'], 'email': 'your_email@example.com'}
        else:
            project['authors'][0]['name'] = updates['author']
        changed = True

    if 'name' in updates:
        project['name'] = updates['name']
        changed = True

    if 'version' in updates:
        project['version'] = updates['version']
        changed = True
    if 'description' in updates:
        project['description'] = updates['description']
        changed = True
    if 'requires-python' in updates:
        project['requires-python'] = updates['requires-python']
        changed = True
    if 'license' in updates:
        if isinstance(project.get('license', None), dict):
            project['license']['text'] = updates['license']
        else:
            project['license'] = {'text': updates['license']}
        changed = True

    if changed:
        config['project'] = project
        if dry_run:
            print_two_colors(ORANGE, BOLD, "Dry Run:", "Changes not written to pyproject.toml.")
        else:
            try:
                with open(file_path, 'w') as f:
                    toml.dump(config, f)
                # loop over the changes and print them with print_two_colors and their keys and values 
                for key, value in updates.items():
                    print_two_colors(BOLD, CYAN, f"Updated pyproject.toml [{key}]:", value)
            except Exception as e:
                print_two_colors(ORANGE, BOLD, "Failed to update pyproject.toml:", e)
    else:
        print_two_colors(ORANGE, BOLD, "No changes made to pyproject.toml.", "")

