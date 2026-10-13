import json
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _load_tracked_accounts():
    accounts = json.loads(os.getenv("TRACKED_ACCOUNTS", "[]"))
    if not isinstance(accounts, list) or any(
        not isinstance(account, dict)
        or not isinstance(account.get("game_name"), str)
        or not isinstance(account.get("tag_line"), str)
        for account in accounts
    ):
        raise ValueError(
            "TRACKED_ACCOUNTS must be a JSON array of objects with "
            "game_name and tag_line strings."
        )
    return accounts


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    RIOT_API_KEY = os.getenv("RIOT_API_KEY", "")
    RIOT_REGION = os.getenv("RIOT_REGION", "americas")
    DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    TRACKED_ACCOUNTS = _load_tracked_accounts()
