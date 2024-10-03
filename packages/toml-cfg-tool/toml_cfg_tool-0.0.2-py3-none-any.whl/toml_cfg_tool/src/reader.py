import toml 
from toml_cfg_tool.src.print_colors import print_two_colors
from toml_cfg_tool.src.color_codes import ORANGE, BOLD

def read_updateable_toml_values(file_path):
    file_path = file_path / 'pyproject.toml'
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
    values = {
        'author': project.get('authors', [{}])[0].get('name', ''),
        'name': project.get('name', ''),
        'version': project.get('version', ''),
        'description': project.get('description', ''),
        'requires-python': project.get('requires-python', ''),
        'license': project.get('license', {}).get('text', '')
    }
    return values

def print_updateable_values(file_path):
    values = read_updateable_toml_values(file_path)
    if values:
        print('Updateable values:')
        for key, value in values.items():
            print_two_colors(BOLD, ORANGE, f'{key}:', value)
    else:
        print('No updateable values found.')
