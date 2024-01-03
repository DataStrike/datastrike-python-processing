from objects.object import Object
from objects.round import Round
from objects.team import Team
from datetime import datetime


class Match(Object):

    def __init__(self, **kwargs):

        data_schema = {"rounds": list,
                       "date": datetime,
                       "map_name": str,
                       "map_type": str,
                       "team1_name": str,
                       "team2_name": str
                       }

        super().__init__(data_schema, **kwargs)

        self.actual_round = -1

    def add_round(self):

        teams = {}
        teams[self.team1_name] = Team.from_json({"name": self.team1_name, "players": {}})
        teams[self.team2_name] = Team.from_json({"name": self.team2_name, "players": {}})
        self.rounds.append(Round.from_json({"teams": teams}))

        self.actual_round += 1

    def add_player(self, data):

        if data["player_name"] in self.rounds[self.actual_round].teams[data["team_name"]].players:
            print("player already exist")
            self.add_character(data)
            return -1
        else:
            self.rounds[self.actual_round].teams[data["team_name"]].add_player(
                {"name": data["player_name"], "characters": {}})
            self.add_character(data)
            return 0


    def add_character(self, data):

        if data["character_name"] in self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters:
            print("character already exist")
            return -2
        else:
            self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].add_character({"name": data["character_name"]})
