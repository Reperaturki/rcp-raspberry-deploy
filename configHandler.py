import os
import sys
import tkinter as tk
import json
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

        self.local_config_path = ""


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

    def ask_config_path(self):
        root = tk.Tk()
        root.withdraw()
        self.local_config_path = filedialog.askopenfilename()
    def check_config(self) -> bool:
        self.ask_config_path()

        if not self.local_config_path.lower().endswith('.json'):
            print("[ERROR] Selected file is not a JSON file.")
            return False

        if os.path.getsize(self.local_config_path) == 0:
            print("[ERROR] Selected file is empty.")
            return False

        try:
            with open(self.local_config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)

            if not config_data:
                print("[ERROR] JSON file contains no data.")
                return False

            if not isinstance(config_data, dict):
                print("[ERROR] JSON must be an object (start with curly braces {}).")
                print(f"Found type: {type(config_data).__name__}")
                return False

            return True

        except json.JSONDecodeError:
            print("[ERROR] Selected file is not valid JSON.")
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error occurred: {e}")
            return False