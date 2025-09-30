from fabric import Connection
from configHandler import ConfigHandler


def deploy():
    cfg_handler = ConfigHandler()

    for host in cfg_handler.hosts_list:
        print("Establishing connection to " + host)

        try:

        except Exception as e:
            print("Failed while copying src to host: " + host)