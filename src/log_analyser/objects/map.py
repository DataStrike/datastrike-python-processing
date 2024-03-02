from log_analyser.objects.object import Object
from log_analyser.objects.round import Round
from log_analyser.objects.team import Team
from datetime import datetime


class Map(Object):

    def __init__(self, **kwargs):

        data_schema = {"rounds": list,
                       "date": datetime,
                       "map_name": str,
                       "map_type": str,
                       "team1_name": str,
                       "team2_name": str,
                       "team1_score": int,
                       "team2_score": int,
                       "team_id": str,
                       "events": list,
                       "stats_graph": dict,
                       }

        super().__init__(data_schema, **kwargs)

        self.actual_round = -1

    def add_round(self, data):

        teams = {}
        teams[self.team1_name] = Team.from_json({"name": self.team1_name, "players": {}})
        teams[self.team2_name] = Team.from_json({"name": self.team2_name, "players": {}})
        self.rounds.append(Round.from_json({"teams": teams, "start_time": data[2], "end_time": "", "objective_captured": [], "objective_progress": []}))

        # self.events.append({"type": "round_start", "timestamp": data[2], "value": 1, "description": "Round {} start".format(len(self.rounds))})

        self.actual_round += 1

        print("###### NEW ROUND {} #######".format(self.actual_round))


    def add_player(self, data):

        if data["player_name"] in self.rounds[self.actual_round].teams[data["team_name"]].players:
            self.add_character(data)
            return -1
        else:
            self.rounds[self.actual_round].teams[data["team_name"]].add_player(
                {"name": data["player_name"], "characters": {}, "role": ""})
            # print("add player", data["player_name"])
            self.add_character(data)
            return 0

    def add_character(self, data):

        if data["character_name"] in self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters:
            return -2
        else:
            self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].add_character({"name": data["character_name"], "stats": {}, "played_time": [], "kills": [], "deaths": [], "ultimate_charged": [], "ultimate_use": [], "role": ""})

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

        team = self.find_team_for_player(data[4])

        self.events.append({"type": "kill", "timestamp": data[2], "player": data[4],
                            "description": "{} kill {}".format(data[4], data[7])})

        self.events.append({"type": "death", "timestamp": data[2], "player": data[7],
                            "description": "{} kill {}".format(data[4], data[7])})

        # if team == list(self.rounds[self.actual_round].teams.keys())[0]:
        #     self.events.append({"type": "kill_team1", "timestamp": data[2], "player": data[4], "description": "{} kill {}".format(data[4], data[7])})
        # else:
        #     self.events.append({"type": "kill_team2", "timestamp": data[2], "player": data[4],
        #                         "description": "{} kill {}".format(data[4], data[7])})
    def add_player_stat(self, data):

        # self.create_if_player_and_caracter_not_exist(data[4], data[5], data[6])

        player_data = {"eliminations": data[7], "final_blows": data[8], "deaths": data[9], "damage": data[10],
                       "barrier_damage": data[11], "hero_damage": data[12], "healing": data[13], "healing_receive": data[14],
                       "self_healing": data[15], "damage_taken": data[16], "damage_blocked": data[17], "defensive_assist": data[18],
                       "offensive_assists": data[19], "ultimates_earned": data[20], "ultimates_used": data[21], "solo_kills": data[24],
                       "critical_hits_accuracy": data[29], "weapon_accuracy": data[38], "hero_time_played": data[39]}

        if player_data["hero_time_played"] != "0":
            if not data[6] in self.rounds[self.actual_round].teams[data[4]].players[data[5]].characters:
                self.add_character({"time": data[2], "team_name": data[4], "player_name": data[5], "character_name": data[6]})
            self.rounds[self.actual_round].teams[data[4]].players[data[5]].characters[data[6]].add_character_stats(player_data)

    def add_hero_swap(self, data):

        self.add_player(data)

        character_swap_dict = data.copy()
        character_swap_dict["character_name"] = data["character_swap"]
        self.add_character(character_swap_dict)

        if data["character_swap"] in self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters:
            self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_swap"]].add_start_time({"start": data["time"]})
        if data["character_name"] in self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters:
            self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_name"]].add_end_time({"end": data["time"]})

        self.events.append({"type": "hero_swap", "timestamp": data["time"], "player": data["player_name"],
                            "description": "{} swap on {}".format(data["player_name"], data["character_swap"])})

        print("{}, {} swap on {}".format(data["player_name"], data["character_name"], data["character_swap"]))
        print("old {} time : {}".format(data["character_name"], self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_name"]].played_time))
        print("new {} time : {}".format(data["character_swap"], self.rounds[self.actual_round].teams[data["team_name"]].players[data["player_name"]].characters[data["character_swap"]].played_time))
        print("############")

    def add_hero_spawn(self, data):

        self.add_player(data)
        self.events.append({"type": "hero_spawn", "timestamp": data["time"], "player": data["player_name"],
                            "description": "{} spawn on {}".format(data["player_name"], data["character_name"])})
    def create_if_player_and_caracter_not_exist(self, team, player_name, character_name):

        if not player_name in self.rounds[self.actual_round].teams[team].players:
            self.add_player({"team_name": team, "player_name": player_name, "character_name": character_name, "time": self.rounds[self.actual_round].start_time})

        if not character_name in self.rounds[self.actual_round].teams[team].players[player_name].characters:
            self.add_character({"team_name": team, "player_name": player_name, "character_name": character_name, "time": self.rounds[self.actual_round].start_time})

    def add_ultimate_start(self, data):

        self.create_if_player_and_caracter_not_exist(data[3], data[4], data[5])

        ultimate_start_data = {"start": data[2]}
        self.rounds[self.actual_round].teams[data[3]].players[data[4]].characters[data[5]].add_ultimate_start(ultimate_start_data)

        self.events.append({"type": "ultimate", "timestamp": data[2], "player": data[4],
                            "description": "{} use {} ultimate".format(data[4], data[5])})

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

        end_round_data = {"time": data[2], "team1_score": data[5], "team2_score": data[6]}
        self.rounds[self.actual_round].end_time = data[2]
        for team in self.rounds[self.actual_round].teams:
            for player in self.rounds[self.actual_round].teams[team].players:

                for character in self.rounds[self.actual_round].teams[team].players[player].characters:
                    if not "end" in self.rounds[self.actual_round].teams[team].players[player].characters[character].played_time[-1]:
                        self.rounds[self.actual_round].teams[team].players[player].characters[character].played_time[-1]["end"] = end_round_data["time"]
                self.rounds[self.actual_round].teams[team].players[player].find_role()

        self.team1_score = end_round_data["team1_score"]
        self.team2_score = end_round_data["team2_score"]
        print(" score team 1 : ", self.team1_score)
        print(" score team 2 : ", self.team2_score)
        print("###### END ROUND {} #######\n".format(self.actual_round))


    def end_map(self, data):

        end_map_data = {"time": data[2], "team1_score": data[4], "team2_score": data[5]}

        self.team1_score = end_map_data["team1_score"]
        self.team2_score = end_map_data["team2_score"]


    def find_team_for_player(self, player_name):

        for team in self.rounds[self.actual_round].teams:
            if player_name in self.rounds[self.actual_round].teams[team].players:
                return team

        return None

    def aggregate_stats(self):
        players_data = {}

        for index, round_data in enumerate(self.rounds):
            print("### Round {} ###".format(index))
            for _, team in round_data.teams.items():
                for _, player in team.players.items():

                    aggregated_stats = {}

                    for character in player.characters.values():
                        if character.stats:
                            for key, value in character.stats.items():
                                try:
                                    numeric_value = float(value)
                                    aggregated_stats[key] = aggregated_stats.get(key, 0) + numeric_value
                                except ValueError:
                                    print("ValueError: ", value, player.name, character.name, key)
                                    aggregated_stats[key] = value

                    if any(isinstance(value, (int, float)) and value == value for value in aggregated_stats.values()):
                        player_name = player.name
                        players_data[player_name] = players_data.get(player_name, [])
                        players_data[player_name].append({"round": index, "stats": aggregated_stats})

        self.stats_graph = players_data