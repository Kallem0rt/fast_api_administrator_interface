import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

path = Path(".")
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


def db_connect():
    engine = create_engine("sqlite:///server.db?check_same_thread=False")
    return engine
