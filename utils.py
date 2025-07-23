import logging
from pathlib import Path
import json
import shutil
import os

# -------------------------------
# Logger Setup
# -------------------------------
def init_logging():
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "global.log"
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logger initialized.")

# -------------------------------
# Log Helper Functions
# -------------------------------
def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def get_log_file_path() -> Path:
    return Path(__file__).resolve().parent.parent / "logs" / "global.log"

def read_log_content(max_lines: int = 500) -> str:
    log_path = get_log_file_path()
    if not log_path.exists():
        return "Log file not found."
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return "".join(lines[-max_lines:])
    except Exception as e:
        return f"Failed to read log file: {e}"

# -------------------------------
# Project Management Functions
# -------------------------------
def is_valid_project(project_path: str) -> bool:
    """
    Check if the given directory is a valid Papyrus project.
    Criteria:
    - Must contain 'project_config.json'
    - Must contain 'Scripts' folder
    """
    p = Path(project_path)
    config = p / "project_config.json"
    scripts = p / "Scripts"
    return config.is_file() and scripts.is_dir()

def create_project(project_name: str, target_dir: str, template_path: str) -> bool:
    """
    Create a new project directory structure based on template.
    Returns True if successful, False otherwise.
    """
    try:
        full_path = Path(target_dir) / project_name
        if full_path.exists():
            log_error(f"Project creation failed: {full_path} already exists.")
            return False
        full_path.mkdir(parents=True, exist_ok=False)
        (full_path / "Scripts").mkdir()
        (full_path / "Resources").mkdir()
        shutil.copy2(template_path, full_path / "project_config.json")
        log_info(f"Project created at {full_path}")
        return True
    except Exception as e:
        log_error(f"Exception during project creation: {e}")
        return False

# -------------------------------
# Settings Management Functions
# -------------------------------
def load_settings(settings_path: str) -> dict:
    """
    Load settings from JSON file.
    Returns dict or empty dict if not found or error.
    """
    p = Path(settings_path)
    if not p.is_file():
        return {}
    try:
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log_error(f"Failed to load settings: {e}")
        return {}

def save_settings(settings_path: str, settings: dict) -> bool:
    """
    Save settings dict to JSON file.
    Returns True if successful.
    """
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
        log_info(f"Settings saved to {settings_path}")
        return True
    except Exception as e:
        log_error(f"Failed to save settings: {e}")
        return False
