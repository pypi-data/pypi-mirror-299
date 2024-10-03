import os

def template_text():
    SETUP_CFG_TEMPLATE = f"""\
[metadata]
name = your_project_name
version = 1.0.0 
author = {os.environ.get('USER', 'Your Name')}
author_email = your_email@example.com 
description = A one line description of your project
long_description = file: README.md 
long_description_content_type = text/markdown
url = https://github.com/yourusername/your-repo
License-Expression = MIT
classifiers =
    Programming Language :: Python :: 3 
    License :: OSI Approved :: MIT License 
    Operating System :: OS Independent

[options]
packages = find:
include_package_data = True
python_requires = >=3.7
# install_requires =
#     required_dependency1
#     required_dependency2

[options.entry_points]
console_scripts =
    project_name = dir_with_entry_script.entry_script_name:main
    """

    PYPROJECT_TOML_TEMPLATE = """\
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your_project_name"
version = "1.0.0"
description = "A one line description of your project"
readme = "README.md"
requires-python = ">=3.7"
# dependencies = [ "required_dependency1", "required_dependency2" ]
[[project.authors]]
name = "Your Name"
email = "your_email@example.com"
[project.license]
text = "MIT"
[project.urls]
Homepage = "https://github.com/yourusername/your-repo"
[project.scripts]
project_name = "dir_with_entry_script.entry_script_name:main"

[tool.setuptools.packages.find]
where = ["."]
exclude = ["tests*"]
    """
    templates = {
        'SETUP_CFG_TEMPLATE': SETUP_CFG_TEMPLATE,
        'PYPROJECT_TOML_TEMPLATE': PYPROJECT_TOML_TEMPLATE
    }
    return templates
