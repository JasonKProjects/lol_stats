from dataclasses import asdict

from flask import Blueprint, current_app, jsonify, render_template

from app.services.riot_api import RiotAPIError, get_account_by_riot_id

main = Blueprint("main", __name__)


@main.get("/")
def index():
    return render_template(
        "index.html",
        accounts=current_app.config["TRACKED_ACCOUNTS"],
    )


@main.get("/api/accounts/<string:game_name>/<string:tag_line>")
def account_by_riot_id(game_name: str, tag_line: str):
    api_key = current_app.config["RIOT_API_KEY"]
    if not api_key:
        return jsonify(error="RIOT_API_KEY is not configured."), 503

    try:
        account = get_account_by_riot_id(
            game_name,
            tag_line,
            api_key,
            current_app.config["RIOT_REGION"],
        )
    except RiotAPIError as error:
        return jsonify(error=str(error)), error.status_code

    return jsonify(asdict(account))
