import os
import tkinter as tk
from tkinter import filedialog


class ConfigHandler:
    def __init__(self):
        self.hosts = os.getenv('HOSTS')
        self.hosts_list = self.hosts.split(',')
        self.project_directory = ""

    def ask_project_path(self):
        root = tk.Tk()
        root.withdraw()
        self.project_directory = filedialog.askdirectory()

    def check_project_directory(self):
        required_files = os.getenv('REQUIRED_FILES').split(',')
        required_directories = os.getenv('REQUIRED_DIRECTORIES').split(',')


