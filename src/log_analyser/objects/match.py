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
                       "team2_name": str,
                       "score_team1": int,
                       "score_team2": int,
                       }

        super().__init__(data_schema, **kwargs)

        self.actual_round = -1

    def add_round(self, data):

        teams = {}
        teams[self.team1_name] = Team.from_json({"name": self.team1_name, "players": {}})
        teams[self.team2_name] = Team.from_json({"name": self.team2_name, "players": {}})
        self.rounds.append(Round.from_json({"teams": teams, "start_time": data[2], "objective_captured": [], "objective_progress": []}))

        self.actual_round += 1

        print("###### NEW ROUND {} #######".format(self.actual_round))

    def add_player(self, data):

        if data["player_name"] in self.rounds[self.actual_round].teams[data["team_name"]].players:
            self.add_character(data)
            return -1
        else:
            self.rounds[self.actual_round].teams[data["team_name"]].add_player(
                {"name": data["player_name"], "characters": {}})
            # print("add player", data["player_name"])
            self.add_character(data)
            return 0

    def add_character(self, data):

        if data["character_name"] in self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters:
            return -2
        else:
            self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].add_character({"name": data["character_name"], "stats": {}, "played_time": [], "kills": [], "deaths": [], "ultimate_charged": [], "ultimate_use": []})

        if len(self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_name"]].played_time) > 0:
            self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_name"]].played_time[-1]["end"] = data["time"]

        self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_name"]].add_played_time({"start": data["time"]})

    def add_kill(self, data):

        killer_data = {"time": data[2], "player_victim": data[7], "character_victim": data[8]}
        victim_data = {"time": data[2], "player_killer": data[4], "character_killer": data[5]}

        self.create_if_player_and_caracter_not_exist(data[3], data[4], data[5])
        self.create_if_player_and_caracter_not_exist(data[6], data[7], data[8])

        if not data[5] in self.rounds[self.actual_round].teams[data[3]].players[data[4]].characters:
            self.add_character({"time": data[2], "team_name": data[3], "player_name": data[4], "character_name": data[5]})

        if not data[6] in self.rounds[self.actual_round].teams[data[6]].players[data[7]].characters:
            self.add_character({"time": data[2], "team_name": data[6], "player_name": data[7], "character_name": data[8]})

        self.rounds[self.actual_round].teams[data[3]].players[data[4]].characters[data[5]].add_kill(killer_data)
        self.rounds[self.actual_round].teams[data[6]].players[data[7]].characters[data[8]].add_death(victim_data)

    def add_player_stat(self, data):

        # self.create_if_player_and_caracter_not_exist(data[4], data[5], data[6])

        player_data = {"eliminations": data[6], "final_blows": data[7], "deaths": data[8], "damage": data[9],
                       "barrier_damage": data[10], "hero_damage": data[11], "healing": data[12], "healing_receive": data[13],
                       "self_healing": data[14], "damage_taken": data[15], "damage_blocked": data[16], "defensive_assist": data[17],
                       "offensive_assists": data[18], "ultimated_earn": data[19], "ultimates_used": data[20], "solo_kills": data[23],
                       "critical_hits_accuracy": data[28], "weapon_accuracy": data[37], "hero_time_played": data[38]}

        if player_data["hero_time_played"] != "0" and data[6] in self.rounds[self.actual_round].teams[data[4]].players[data[5]].characters:
            self.rounds[self.actual_round].teams[data[4]].players[data[5]].characters[data[6]].add_character_stats(player_data)

    def add_hero_swap(self, data):

        self.add_player(data)
        if data["character_swap"] in self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters:
            self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_swap"]].add_played_time({"end": data["time"]})


    def create_if_player_and_caracter_not_exist(self, team, player_name, character_name):

        if not player_name in self.rounds[self.actual_round].teams[team].players:
            self.add_player({"team_name": team, "player_name": player_name, "character_name": character_name, "time": self.rounds[self.actual_round].start_time})

        if not character_name in self.rounds[self.actual_round].teams[team].players[player_name].characters:
            self.add_character({"team_name": team, "player_name": player_name, "character_name": character_name, "time": self.rounds[self.actual_round].start_time})

    def add_ultimate_start(self, data):

        self.create_if_player_and_caracter_not_exist(data[3], data[4], data[5])

        ultimate_start_data = {"start": data[2]}
        self.rounds[self.actual_round].teams[data[3]].players[data[4]].characters[data[5]].add_ultimate_start(ultimate_start_data)

    def add_ultimate_end(self, data):

        self.create_if_player_and_caracter_not_exist(data[3], data[4], data[5])

        ultimate_end_data = {"end": data[2]}
        self.rounds[self.actual_round].teams[data[3]].players[data[4]].characters[data[5]].add_ultimate_end(ultimate_end_data)

    def add_ultimate_charged(self, data):

        self.create_if_player_and_caracter_not_exist(data[3], data[4], data[5])

        ultimate_charged_data = data[2]
        self.rounds[self.actual_round].teams[data[3]].players[data[4]].characters[data[5]].add_ultimate_charged(ultimate_charged_data)

    def add_objective_captured(self, data):

        objective_capture_data = {"time": data[2], "team_name": data[4], "control_team1_progress": data[6],
                                  "control_team2_progress": data[7]}

        self.rounds[self.actual_round].add_objective_captured(objective_capture_data)


    def add_objective_progress(self, data):

        objectif_progress_data = {"time": data[2], "team_name": data[4], "progress": data[6]}
        self.rounds[self.actual_round].add_objective_progress(objectif_progress_data)
        pass

    def end_round(self, data):

        end_round_data = {"time": data[2], "score_team1": data[5], "score_team2": data[6]}

        for team in self.rounds[self.actual_round].teams:
            for player in self.rounds[self.actual_round].teams[team].players:
                for character in self.rounds[self.actual_round].teams[team].players[player].characters:
                    if not "end" in self.rounds[self.actual_round].teams[team].players[player].characters[character].played_time[-1]:
                        self.rounds[self.actual_round].teams[team].players[player].characters[character].played_time[-1]["end"] = end_round_data["time"]


        self.score_team1 = end_round_data["score_team1"]
        self.score_team2 = end_round_data["score_team2"]
        print("###### END ROUND {} #######\n".format(self.actual_round))

    def end_match(self, data):

        end_match_data = {"time": data[2], "score_team1": data[4], "score_team2": data[5]}

        self.score_team1 = end_match_data["score_team1"]
        self.score_team2 = end_match_data["score_team2"]
