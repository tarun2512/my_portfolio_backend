"""
This file exposes configurations from config file and environments as Class Objects
"""
import shutil

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
import os.path
import sys
from configparser import BasicInterpolation, ConfigParser
from urllib.parse import urlparse


class EnvInterpolation(BasicInterpolation):
    """
    Interpolation which expands environment variables in values.
    """

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)

        if not os.path.expandvars(value).startswith("$"):
            return os.path.expandvars(value)
        else:
            return


try:
    config = ConfigParser(interpolation=EnvInterpolation())
    config.read("conf/application.conf")
except Exception as e:
    print(f"Error while loading the config: {e}")
    print("Failed to Load Configuration. Exiting!!!")
    sys.stdout.flush()
    sys.exit()


class Service:
    MODULE_NAME = config["SERVICE"]["name"]
    HOST = config.get("SERVICE", "host")
    PORT = config.getint("SERVICE", "port")
    secret_key = config.get("SERVICE", "secret_key", fallback=True)


class Logging:
    level = config.get("LOGGING", "level", fallback="INFO")
    level = level or "INFO"
    print(f"Logging Level set to: {level}")
    ENABLE_FILE_LOG = os.environ.get("ENABLE_FILE_LOG", False)
    ENABLE_CONSOLE_LOG = os.environ.get("ENABLE_CONSOLE_LOG", True)


class PathToStorage:
    BASE_PATH = config.get("DIRECTORY", "base_path")
    if not BASE_PATH:
        print("Error, environment variable BASE_PATH not set")
        sys.exit(1)
    MOUNT_DIR = config.get("DIRECTORY", "mount_dir")
    if not MOUNT_DIR:
        print("Error, environment variable MOUNT_DIR not set")
        sys.exit(1)
    LOGS_MODULE_PATH = f"{BASE_PATH}/logs{MOUNT_DIR}/"


class Database:
    MONGO_URI = config["DATABASE"]["MONGO_URI"]