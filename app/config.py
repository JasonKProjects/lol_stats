import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    RIOT_API_KEY = os.getenv("RIOT_API_KEY", "")
    RIOT_REGION = os.getenv("RIOT_REGION", "americas")
    DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    TRACKED_ACCOUNTS = [
        {"game_name": "TouchMyFro", "tag_line": "SWEDE"},
        {"game_name": "Focn2", "tag_line": "NA1"},
        {"game_name": "M0zzle", "tag_line": "top"},
        {"game_name": "beat u drunk", "tag_line": "1or12"},
        {"game_name": "Formula1Fan", "tag_line": "FRARI"},
    ]
