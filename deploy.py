import sys
import time
import os
from fabric import Connection
from configHandler import ConfigHandler


def put_dir(connection: Connection, local_dir: str, remote_dir: str):
    base_name = os.path.basename(local_dir)
    local_dir = os.path.abspath(local_dir)

    for root, dirs, files in os.walk(local_dir):
        relative_path = os.path.relpath(root, local_dir)
        remote_path = os.path.join(remote_dir, base_name, relative_path).replace("\\", "/")

        connection.run(f"mkdir -p '{remote_path}'")

        for file in files:
            local_file = os.path.join(root, file)
            remote_file = os.path.join(remote_path, file).replace("\\", "/")
            connection.put(local_file, remote_file)


def deploy():
    cfg_handler = ConfigHandler()
    if not cfg_handler.check_project_directory():
        sys.exit(1)

    for host in cfg_handler.hosts_list:
        print("Deploy started for the host: " + host)
        try:
            connection = Connection(host, port=22, user=cfg_handler.ssh_user,
                                    connect_kwargs={"password": cfg_handler.ssh_password})

            for required_file in cfg_handler.required_files:
                connection.put(os.path.join(cfg_handler.project_directory, required_file), cfg_handler.destination_directory)

            if cfg_handler.required_directories and cfg_handler.required_directories[0] != "":
                for required_directory in cfg_handler.required_directories:
                    put_dir(connection, os.path.join(cfg_handler.project_directory, required_directory),
                            cfg_handler.destination_directory)
            else:
                print("No directories to deploy - skipping directory deployment")

            connection.run(f"sudo systemctl restart {cfg_handler.service_to_restart}")
            connection.close()

            print("Deploy finished successfully for the host: " + host)
        except Exception as e:
            print(f"[ERROR] Deploy failed for the host: {host} || {e}")