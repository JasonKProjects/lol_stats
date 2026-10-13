import unittest
from unittest.mock import patch

from app import create_app
from app.models import Player


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret"
    RIOT_API_KEY = "test-api-key"
    RIOT_REGION = "americas"
    TRACKED_ACCOUNTS = []


class RiotAccountControllerTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    @patch("app.controllers.main_controller.get_account_by_riot_id")
    def test_returns_account_as_json(self, mock_lookup):
        mock_lookup.return_value = Player(
            game_name="Player",
            tag_line="NA1",
            puuid="puuid-value",
            region="americas",
        )

        response = self.client.get("/api/accounts/Player/NA1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "game_name": "Player",
                "tag_line": "NA1",
                "puuid": "puuid-value",
                "region": "americas",
            },
        )
        mock_lookup.assert_called_once_with(
            "Player",
            "NA1",
            "test-api-key",
            "americas",
        )

    def test_returns_clear_error_when_api_key_is_missing(self):
        self.app.config["RIOT_API_KEY"] = ""

        response = self.client.get("/api/accounts/Player/NA1")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json,
            {"error": "RIOT_API_KEY is not configured."},
        )

    @patch("app.controllers.main_controller.get_account_by_riot_id")
    def test_translates_riot_api_errors_to_json(self, mock_lookup):
        from app.services.riot_api import RiotAPIError

        mock_lookup.side_effect = RiotAPIError(404, "Riot account not found.")

        response = self.client.get("/api/accounts/Missing/NA1")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Riot account not found."})
