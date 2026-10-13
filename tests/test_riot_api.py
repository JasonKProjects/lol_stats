import json
import unittest
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError

from app.services.riot_api import RiotAPIError, get_account_by_riot_id


class RiotAccountServiceTests(unittest.TestCase):
    @patch("app.services.riot_api.urlopen")
    def test_fetches_account_and_returns_player(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = (
            b'{"gameName":"Player Name","tagLine":"NA1","puuid":"puuid-value"}'
        )

        player = get_account_by_riot_id(
            "Player Name",
            "NA1",
            "test-api-key",
            "americas",
        )

        request = mock_urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://americas.api.riotgames.com/riot/account/v1/accounts/"
            "by-riot-id/Player%20Name/NA1",
        )
        self.assertEqual(request.get_header("X-riot-token"), "test-api-key")
        self.assertEqual(player.game_name, "Player Name")
        self.assertEqual(player.tag_line, "NA1")
        self.assertEqual(player.puuid, "puuid-value")
        self.assertEqual(player.region, "americas")

    def test_rejects_invalid_routing_region(self):
        with self.assertRaisesRegex(RiotAPIError, "RIOT_REGION"):
            get_account_by_riot_id("Player", "NA1", "test-api-key", "na")

    @patch(
        "app.services.riot_api.urlopen",
        side_effect=HTTPError(
            "https://americas.api.riotgames.com",
            404,
            "Not Found",
            {},
            BytesIO(b""),
        ),
    )
    def test_reports_account_not_found(self, _mock_urlopen):
        with self.assertRaises(RiotAPIError) as context:
            get_account_by_riot_id("Missing", "NA1", "test-api-key", "americas")

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(str(context.exception), "Riot account not found.")

    @patch("app.services.riot_api.urlopen")
    def test_rejects_invalid_riot_response(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(
            {"gameName": "Player"}
        ).encode()

        with self.assertRaisesRegex(RiotAPIError, "invalid account"):
            get_account_by_riot_id("Player", "NA1", "test-api-key", "americas")
