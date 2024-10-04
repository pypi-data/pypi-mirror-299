# ./src/creation.py 
import os
import shutil
import subprocess
import toml
import configparser
import glob
from pathlib import Path
from urllib.parse import urlparse
from toml_cfg_tool.src.config import template_text 
from toml_cfg_tool.src.color_codes import BOLD, CYAN, LINK, ORANGE
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
        git_url = result.stdout.strip()
        return git_url if result.stdout else "No GitHub repository found."
    except subprocess.CalledProcessError:
        return "Not a Git repository."

def create_setup_cfg_template(file_path, dry_run=False):
    if os.path.exists(file_path):
        print_two_colors(BOLD, ORANGE, "setup.cfg already exists.", "Skipping template creation.")
        return
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

    parsed_url = urlparse(repo_url)
    if parsed_url.hostname and parsed_url.hostname.endswith("github.com"):
        config = configparser.ConfigParser()
        config.read(file_path)
        config['metadata']['url'] = repo_url
        with open(file_path, 'w') as f:
            config.write(f)

def create_pyproject_toml_template(file_path, dry_run=False):
    if os.path.exists(file_path):
        print_two_colors(BOLD, ORANGE, "pyproject.toml already exists.", "Skipping template creation.")
        return
    if dry_run:
        print_two_colors(BOLD, CYAN, "[Dry Run]", "Template not written.")
        return
    try:
        with open(file_path, 'w') as f:
            f.write(PYPROJECT_TOML_TEMPLATE)
        print_two_colors(BOLD, LINK, "Template pyproject.toml created successfully.", file_path)
    except Exception as e:
        print_two_colors(ORANGE, BOLD, "Failed to create pyproject.toml:", e)
   
    repo_url = get_github_repo_url()
    parsed_url = urlparse(repo_url)
    if parsed_url.hostname and parsed_url.hostname.endswith("github.com"):
        config = toml.load(file_path)
        config['project']['urls']['Homepage'] = repo_url
        with open(file_path, 'w') as f:
            toml.dump(config, f)

def create_workflow_files():
    root = Path(__file__).parent.parent
    src = root / "src/github_workflows"
    cwd = Path.cwd()
    github = cwd / ".github"
    workflow_dest = cwd / ".github/workflows"
    script_dest = cwd / ".github/scripts"
    workflow_files = glob.glob(f"{src}/*.yml")
    script_files = glob.glob(f"{src}/*.sh") + glob.glob(f"{src}/*.py")

    # Get the basenames of the current workflow and script files for comparison
    current_workflow_files = [os.path.basename(f) for f in glob.glob(f"{workflow_dest}/*.yml")]
    current_script_files = [os.path.basename(f) for f in glob.glob(f"{script_dest}/*.sh") + glob.glob(f"{script_dest}/*.py")]

    if not os.path.exists(github):
        print_two_colors(BOLD, LINK, "Folder not found:", github)
        return

    if not os.path.exists(workflow_dest):
        print_two_colors(BOLD, LINK, f"Creating folder:", workflow_dest)
        os.makedirs(workflow_dest)

    if not os.path.exists(script_dest):
        print_two_colors(BOLD, LINK, f"Creating folder:", script_dest)
        os.makedirs(script_dest)

    skip_counter = 0

    # Copy workflow files only if they don't already exist
    for file in workflow_files:
        if os.path.basename(file) in current_workflow_files:
            skip_counter += 1
            continue
        print_two_colors(BOLD, LINK, "Copying", file)
        print_two_colors(BOLD, LINK, "to", workflow_dest)
        new_file = workflow_dest / os.path.basename(file)
        shutil.copyfile(file, new_file)

    # Copy script files only if they don't already exist
    for file in script_files:
        if os.path.basename(file) in current_script_files:
            skip_counter += 1
            continue
        print_two_colors(BOLD, LINK, "Copying", file)
        print_two_colors(BOLD, LINK, "to", script_dest)
        new_file = script_dest / os.path.basename(file)
        shutil.copyfile(file, new_file)

    if skip_counter == len(workflow_files) + len(script_files):
        print_two_colors(BOLD, ORANGE, "All workflow and script files already exist.", "Skipping copy.")
