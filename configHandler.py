import os
import sys
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

def require_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        print(f"[ERROR] Missing environment variable: {key}", file=sys.stderr)
        sys.exit(1)
    return value

class ConfigHandler:
    def __init__(self):
        load_dotenv()
        self.ssh_user = require_env('SSH_USER')
        self.ssh_password = require_env('SSH_PASSWORD')

        self.service_to_restart = require_env('SERVICE_TO_RESTART')

        self.hosts_list = require_env('RASPI_HOSTS').split(',')

        self.required_files = require_env('REQUIRED_FILES').split(',')
        self.required_directories = require_env('REQUIRED_DIRECTORIES').split(',')

        self.destination_directory = require_env('DESTINATION_DIRECTORY')

        self.project_directory = ""

    def ask_project_path(self):
        root = tk.Tk()
        root.withdraw()
        self.project_directory = filedialog.askdirectory()

    def check_project_directory(self) -> bool:
        self.ask_project_path()

        for required_file in self.required_files:
            if not os.path.exists(os.path.join(self.project_directory, required_file)):
                print(os.path.join(self.project_directory + required_file))
                print(f"[ERROR] One of the required files is missing: {required_file}")
                return False

        for required_directory in self.required_directories:
            if not os.path.exists(os.path.join(self.project_directory, required_directory)):
                print(f"[ERROR] One of the required directories is missing: {required_directory}")
                return False

        return True