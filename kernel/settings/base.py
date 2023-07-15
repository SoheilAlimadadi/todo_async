from pathlib import Path

from utils.config_parser import config

# project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# FastAPI host and port
HOST = config.get_value("settings.fastapi", 'HOST')
PORT = config.get_value("settings.fastapi", "PORT")
