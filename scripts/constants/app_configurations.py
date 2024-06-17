"""
This file exposes configurations from config file and environments as Class Objects
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Service:
    MODULE_NAME = os.getenv("MODULE_NAME")
    PORT = int(os.getenv("PORT"))
    secret_key = "KLKey"


class Logging:
    level = os.getenv("LOG_LEVEL")
    level = level or "INFO"
    print(f"Logging Level set to: {level}")
    ENABLE_FILE_LOG = os.environ.get("ENABLE_FILE_LOG", False)
    ENABLE_CONSOLE_LOG = os.environ.get("ENABLE_CONSOLE_LOG", True)


class PathToStorage:
    BASE_PATH = os.getenv("BASE_PATH")
    if not BASE_PATH:
        print("Error, environment variable BASE_PATH not set")
        sys.exit(1)
    MOUNT_DIR = os.getenv("MOUNT_DIR")
    if not MOUNT_DIR:
        print("Error, environment variable MOUNT_DIR not set")
        sys.exit(1)
    LOGS_MODULE_PATH = f"{BASE_PATH}/logs{MOUNT_DIR}/"


class Database:
    MONGO_URI = os.getenv("MONGO_URI")