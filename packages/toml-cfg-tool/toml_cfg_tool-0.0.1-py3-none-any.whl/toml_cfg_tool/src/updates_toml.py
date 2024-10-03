# ./toml_cfg_tool/src/updates_toml.py 
import toml 
from toml_cfg_tool.src.bkup import backup_file
from toml_cfg_tool.src.color_codes import BOLD, CYAN, LINK, ORANGE, END
from toml_cfg_tool.src.print_colors import print_two_colors
from toml_cfg_tool.src.creation import get_github_repo_url


def update_pyproject_toml(file_path, updates, dry_run=False, backup=False):
    repo_url = get_github_repo_url()
    
    if "github.com" in repo_url:
        config = toml.load(file_path)
        config['project']['urls']['Homepage'] = repo_url
        with open(file_path, 'w') as f:
            toml.dump(config, f)
        print_two_colors(BOLD, LINK, "Updated pyproject.toml with GitHub repository URL:", repo_url)
    
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
        print_two_colors(BOLD, CYAN, "Updating pyproject.toml [project.authors] name to:", updates['author'])
        if 'authors' not in project:
            print_two_colors(ORANGE, BOLD, "Authors section not found in pyproject.toml", "Creating new section.")
            project['authors'] = {'name': updates['author'], 'email': 'your_email@example.com'}
        else:
            project['authors'][0]['name'] = updates['author']
            print_two_colors(BOLD, CYAN, "Updating pyproject.toml [project.authors] name to:", updates['author'])
        changed = True

    if 'name' in updates:
        print_two_colors(BOLD, CYAN, "Updating pyproject.toml [project.scripts] project_name to:", updates['name'])
        project['name'] = updates['name']
        if 'scripts' in project:
            script_name = updates['name'] + '.' + updates['name'] + ':main'
            print_two_colors(ORANGE, BOLD, "Updating pyproject.toml [project.scripts] entry_script_name to:", script_name)
            print(project['scripts'])
            # print the title, eg [project.scripts]
            print (f"project.scripts: {project['scripts']}")
            project['scripts'] = {updates['name']: script_name}
        changed = True

    if 'version' in updates:
        print_two_colors(BOLD, CYAN, "Updating pyproject.toml [project] version to:", updates['version'])
        project['version'] = updates['version']
        changed = True
    if 'description' in updates:
        print_two_colors(BOLD, CYAN, "Updating pyproject.toml [project] description to:", updates['description'])
        project['description'] = updates['description']
        changed = True
    if 'requires-python' in updates:
        print_two_colors(BOLD, CYAN, "Updating pyproject.toml [project] requires-python to:", updates['requires-python'])
        project['requires-python'] = updates['requires-python']
        changed = True
    if 'license' in updates:
        print_two_colors(BOLD, CYAN, "Updating pyproject.toml [project] license to:", updates['license'])
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
                print_two_colors(BOLD, CYAN, "pyproject.toml updated successfully.", "Changes written to file.")
            except Exception as e:
                print_two_colors(ORANGE, BOLD, "Failed to update pyproject.toml:", e)
    else:
        print_two_colors(ORANGE, BOLD, "No changes made to pyproject.toml.", "")

