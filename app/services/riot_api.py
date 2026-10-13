import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from app.models import Player

_ROUTING_REGIONS = {"americas", "asia", "europe", "sea"}


class RiotAPIError(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code


def get_account_by_riot_id(
    game_name: str,
    tag_line: str,
    api_key: str,
    region: str,
) -> Player:
    if region not in _ROUTING_REGIONS:
        raise RiotAPIError(500, "RIOT_REGION must be a valid Riot routing region.")

    url = (
        f"https://{region}.api.riotgames.com/riot/account/v1/accounts/"
        f"by-riot-id/{quote(game_name, safe='')}/{quote(tag_line, safe='')}"
    )
    request = Request(url, headers={"X-Riot-Token": api_key})

    try:
        with urlopen(request, timeout=10) as response:
            account = json.loads(response.read())
    except HTTPError as error:
        if error.code == 404:
            raise RiotAPIError(404, "Riot account not found.") from error
        if error.code in {401, 403}:
            raise RiotAPIError(
                502,
                "Riot API rejected the key; check RIOT_API_KEY.",
            ) from error
        if error.code == 429:
            raise RiotAPIError(503, "Riot API rate limit exceeded.") from error
        raise RiotAPIError(502, "Riot API returned an error.") from error
    except (TimeoutError, URLError) as error:
        raise RiotAPIError(502, "Could not connect to Riot API.") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RiotAPIError(502, "Riot API returned an invalid response.") from error

    if not isinstance(account, dict) or not all(
        isinstance(account.get(field), str)
        for field in ("gameName", "tagLine", "puuid")
    ):
        raise RiotAPIError(502, "Riot API returned an invalid account.")

    return Player(
        game_name=account["gameName"],
        tag_line=account["tagLine"],
        puuid=account["puuid"],
        region=region,
    )
