# ./src/bkup.py
import os
import shutil
from toml_cfg_tool.src.color_codes import BOLD, CYAN, LINK, ORANGE
from toml_cfg_tool.src.print_colors import print_two_colors

def backup_file(file_path):
    if file_path.endswith(".*"):
        file_path = file_path[:-2]
    backup_path = f"{file_path}.bak"
    if os.path.exists(backup_path):
        print_two_colors(ORANGE, LINK, "Backup file already exists:\n", backup_path)
        return
    try:
        shutil.copy(file_path, backup_path)
        print_two_colors(BOLD, CYAN, "Created backup for ", file_path)
    except Exception:
        print_two_colors(ORANGE, LINK, "Error creating backup for ", file_path)
