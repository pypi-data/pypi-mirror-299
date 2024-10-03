# ./src/creation.py 
import os
import shutil
import datetime 
import subprocess
import toml
import configparser
from pathlib import Path
from toml_cfg_tool.src.config import template_text 
from toml_cfg_tool.src.color_codes import BOLD, CYAN, LINK, ORANGE, END
from toml_cfg_tool.src.print_colors import print_two_colors

SETUP_CFG_TEMPLATE = template_text()['SETUP_CFG_TEMPLATE']
PYPROJECT_TOML_TEMPLATE = template_text()['PYPROJECT_TOML_TEMPLATE']

def get_github_repo_url():
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip() if result.stdout else "No GitHub repository found."
    except subprocess.CalledProcessError:
        return "Not a Git repository."

def create_setup_cfg_template(file_path, dry_run=False):
    if os.path.exists(file_path):
        print_two_colors(BOLD, ORANGE, "setup.cfg already exists.", "Skipping template creation.")
        return
    print_two_colors(BOLD, LINK, "Creating template setup.cfg at", file_path)
    if dry_run:
        print_two_colors(BOLD, CYAN, "[Dry Run]", "Template not written.")
        return
    try:
        with open(file_path, 'w') as f:
            f.write(SETUP_CFG_TEMPLATE)
        print_two_colors(BOLD, LINK, "Template setup.cfg created successfully.", file_path)
    except Exception as e:
        print_two_colors(ORANGE, BOLD, "Failed to create setup.cfg:", e)

    repo_url = get_github_repo_url()
    if "github.com" in repo_url:
        config = configparser.ConfigParser()
        config.read(file_path)
        config['metadata']['url'] = repo_url
        with open(file_path, 'w') as f:
            config.write(f)
        print_two_colors(BOLD, LINK, "Updated setup.cfg with GitHub repository URL:", repo_url)

def create_pyproject_toml_template(file_path, dry_run=False):
    if os.path.exists(file_path):
        print_two_colors(BOLD, ORANGE, "pyproject.toml already exists.", "Skipping template creation.")
        return
    print_two_colors(BOLD, LINK, "Creating template pyproject.toml at", file_path)
    if dry_run:
        print_two_colors(BOLD, CYAN, "[Dry Run]", "Template not written.")
        return
    try:
        with open(file_path, 'w') as f:
            f.write(PYPROJECT_TOML_TEMPLATE)
        print_two_colors(BOLD, LINK, "Template pyproject.toml created successfully.", file_path)
    except Exception as e:
        print_two_colors(ORANGE, BOLD, "Failed to create pyproject.toml:", e)
# format of the project.urls section in pyproject.toml
#  [project.urls]
# Homepage = "https://github.com/yourusername/your-repo"
   
    repo_url = get_github_repo_url()
    if "github.com" in repo_url:
        config = toml.load(file_path)
        config['project']['urls']['Homepage'] = repo_url
        with open(file_path, 'w') as f:
            toml.dump(config, f)
        print_two_colors(BOLD, LINK, "Updated pyproject.toml with GitHub repository URL:", repo_url)


def create_workflow_files():
    root = Path(__file__).parent.parent
    src = root / "src/github_workflows"
    cwd = Path.cwd()
    github = cwd / ".github"
    workflow_dest = cwd / ".github/workflows"
    script_dest = cwd / ".github/scripts"
    workflow_files = ["check-pr-title.yml", "label-issues.yml", "python-publish.yml"]
    script_files = ["version_checker.py"]
        
    if not os.path.exists(github):
        print_two_colors(BOLD, LINK, "Folder not found:", github)
        return

    if not os.path.exists(workflow_dest):
        print_two_colors(BOLD, LINK, f"Creating folder:", workflow_dest)
        os.makedirs(workflow_dest)

    if not os.path.exists(script_dest):
        print_two_colors(BOLD, LINK, f"Creating folder:", script_dest)
        os.makedirs(script_dest)

    for file in workflow_files:
        src_file = os.path.join(src, file)
        src_filename = os.path.basename(src_file)
        dest_file = os.path.join(workflow_dest, file)
        copy_dict = { "Copying": src_filename, "to": dest_file }
        for key, value in copy_dict.items():
            print_two_colors(BOLD, LINK, key, value)
        shutil.copyfile(src_file, dest_file)

    for file in script_files:
        src_file = os.path.join(src, file)
        src_filename = os.path.basename(src_file)
        dest_file = os.path.join(script_dest, file)
        copy_dict = { "Copying": src_filename, "to": dest_file }
        for key, value in copy_dict.items():
            print_two_colors(BOLD, LINK, key, value)
        shutil.copyfile(src_file, dest_file)
