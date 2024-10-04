import os
import re
import subprocess
from pathlib import Path
from toml_cfg_tool.src.color_codes import BOLD, LINK
from toml_cfg_tool.src.print_colors import print_two_colors

def find_delete_line(file_path, delete_line, new_text=None):
    path = Path(file_path)
    text = path.read_text()
    if new_text:
        text = new_text
    new_lines = [line for line in text.split("\n") if delete_line not in line]
    updated_text = "\n".join(new_lines)
    path.write_text(updated_text)

def loop_replace_text(file_path, old_text_list, new_text_list):
    path = Path(file_path)
    text = path.read_text()
    for i in range(len(old_text_list)):
        new_text = re.sub(old_text_list[i], new_text_list[i], text)
        text = new_text

    if os.path.exists(file_path):
        pass
    else:
        with open(file_path, 'w') as f:
            f.write(text)

    return text

def get_github_repo_info():
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        url = result.stdout.strip()

        match = re.search(r'github\.com[:/](?P<username>[^/]+)/(?P<repo>[^/]+)\.git', url)
        
        if match:
            github_username = match.group("username")
            repo_name = match.group("repo")
            return repo_name, github_username
        else:
            return None, None
    except subprocess.CalledProcessError:
        return None, None

def create_contrib_file():
    delete_line = "### Delete this line"
    src_path = Path(__file__).parent.parent
    file_path = src_path / "src/github_workflows/CONTRIBUTING.md"
    subprocess.run(["cp", file_path, ".github/CONTRIBUTING.md"])
    repo_name, github_username = get_github_repo_info()
    if repo_name is None:
        repo_name = "RepoName"
    if github_username is None:
        github_username = "GitHubUsername"
    old_text_list = ["RepoName", "GitHubUsername"]
    new_text_list = [repo_name, github_username]
    cwd = Path.cwd()
    github_dir = cwd / ".github"
    if github_dir.exists():
        print_two_colors(BOLD, LINK, "Creating CONTRIBUTING.md in .github directory", github_dir)
        github_dir / "CONTRIBUTING.md"
        github_dir.mkdir(exist_ok=True)
        github_file_path = github_dir / "CONTRIBUTING.md"
        text = loop_replace_text(github_file_path, old_text_list, new_text_list)
        find_delete_line(github_file_path, delete_line, text)
    else:
        text = loop_replace_text(file_path, old_text_list, new_text_list)
        find_delete_line(file_path, delete_line, text)
        print("No .github directory found at", cwd)
