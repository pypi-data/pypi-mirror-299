import os




def template_text():
    SETUP_CFG_TEMPLATE = f"""\
[metadata]
name = your_project_name
version = 0.0.1
author = {os.environ.get('USER', 'Your Name')}
author_email = your_email@example.com
description = A one line description of your project.
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/yourusername/your-repo.git
license-expression = MIT
classifiers = 
	Programming Language :: Python :: 3
	License :: OSI Approved :: MIT License
	Operating System :: OS Independent

[tool.setuptools.packages.find]
where = [ ".",]
exclude = [ "tests*", ]

[options]
"""

    PYPROJECT_TOML_TEMPLATE = f"""\
[project]
name = "your_project_name" 
version = "0.0.1"
description = "A one line description of your project"
readme = "README.md"
requires-python = ">=3.10"
# dependencies = [ "", "" ]
[[project.authors]]
name = "{os.environ.get('USER', 'Your Name')}"
email = "your_email@example.com"

[build-system]
requires = [ "setuptools>=61.0", "wheel",]
build-backend = "setuptools.build_meta"

[project.license]
text = "MIT"

[project.urls]
Homepage = "https://github.com/yourusername/your-repo.git"

[project.scripts]
your_project_name = "root_dir.main_script:main"

[tool.setuptools.packages.find]
where = [ ".",]
exclude = [ "tests*",]
    """
    templates = {
        'SETUP_CFG_TEMPLATE': SETUP_CFG_TEMPLATE,
        'PYPROJECT_TOML_TEMPLATE': PYPROJECT_TOML_TEMPLATE
    }
    return templates
