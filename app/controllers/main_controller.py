from flask import Blueprint, current_app, render_template

main = Blueprint("main", __name__)


@main.get("/")
def index():
    return render_template(
        "index.html",
        accounts=current_app.config["TRACKED_ACCOUNTS"],
    )
