from dataclasses import dataclass


@dataclass
class Player:
    game_name: str
    tag_line: str
    puuid: str
    region: str
