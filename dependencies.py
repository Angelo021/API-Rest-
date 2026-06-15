from fastapi import Depends
from app.core.config import Config

def get_config():
    return Config()