# League Stats

A fun personal project for Jason to experiment with random League of Legends stats using Riot's free-tier developer API. The app is built with Flask and organized in an MVC-style structure.

## Requirements

- Python 3.14
- pip

## Setup on Windows

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `SECRET_KEY` and `RIOT_API_KEY` in `.env`. Keep `.env` private; it is excluded from Git.

Tracked Riot IDs are stored in the local, Git-ignored `.env` file as a JSON array in `TRACKED_ACCOUNTS`. For example:

```dotenv
TRACKED_ACCOUNTS='[{"game_name":"PlayerName","tag_line":"NA1"}]'
```

Add one object per account. Riot IDs stay local and are not committed; `.env.example` contains an empty list as a template.

For development tools, install Ruff:

```powershell
python -m pip install -r requirements-dev.txt
```

## Run

```powershell
python run.py
```

Open the local URL printed by Flask. Debug mode is enabled by the local `.env` setting and should be disabled outside development.

## Code quality

Ruff settings are in `pyproject.toml`. Run linting and formatting checks with:

```powershell
python -m ruff check .
python -m ruff format --check .
```

To apply automatic formatting, run `python -m ruff format .`.

## Structure

```text
app/
  config.py
  controllers/       Flask routes and request handling
  models/            Application data models
  static/            CSS, JavaScript, and images
  templates/         Jinja HTML views
run.py               Application entry point
requirements.txt     Python dependencies
requirements-dev.txt Development dependencies, including Ruff
pyproject.toml       Ruff lint and format configuration
.env                 Local secrets and settings (not committed)
.env.example         Environment variable template
```
