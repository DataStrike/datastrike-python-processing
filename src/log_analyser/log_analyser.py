import os
from datetime import datetime, timedelta
from log_analyser.objects.map import Map


class LogAnalyser:
    
    def __init__(self, path, name, team_id) -> None:
        
        self.path_csv = "{}/{}".format(path, name)
        self.name = name
        self.team_id = team_id
        
        self.date = self.name2datetime()
        
        self.map = None
        
        self.actions = {"match_start": self.process_map_start}
        
    def run(self):
        
        with open(self.path_csv, encoding='utf-8') as my_file:
            file = my_file.read()
            lines = file.split("\n")
            for line in lines:
                line_split = line.split(",")

                if len(line_split) > 1:
                    type = line_split[1]
                    if type in self.actions:
                        self.actions[type](line_split)

        self.map.aggregate_stats()


    def name2datetime(self):
        
        date_string = self.name.split(".")[0].split("Log-")[1]
        date_object = datetime.strptime(date_string, '%Y-%m-%d-%H-%M-%S')
        
        return date_object

    def process_map_start(self, data):

        print("New map : {}".format(data[3]))
        self.map = Map.from_json({"rounds": [],
                       "date": self.date,
                       "map_name": data[3],
                       "map_type": data[4],
                       "team1_name": data[5],
                       "team2_name": data[6],
                       "team1_score": 0,
                       "team2_score": 0,
                       "team_id": self.team_id,
                       "events": [],
                       "stats_graph": {},
                       })

        self.actions = {"match_start": self.process_map_start,
                        "round_start": self.map.add_round,
                        "round_end": self.map.end_round,
                        "hero_spawn": self.process_hero_spawn,
                        "hero_swap": self.process_hero_swap,
                        "kill": self.map.add_kill,
                        "ultimate_charged": self.map.add_ultimate_charged,
                        "ultimate_start": self.map.add_ultimate_start,
                        "ultimate_end": self.map.add_ultimate_end,
                        "objective_captured": self.map.add_objective_captured,
                        "player_stat": self.map.add_player_stat,
                        "point_progress": self.map.add_objective_progress,
                        "payload_progress": self.map.add_objective_progress,
                        }

    def process_hero_spawn(self, data):

        player_data = {"time": data[2], "team_name": data[3], "player_name": data[4], "character_name": data[5]}
        self.map.add_player(player_data)

    def process_hero_swap(self, data):

        hero_data = {"time": data[2], "team_name": data[3], "player_name": data[4], "character_name": data[5], "character_swap": data[6]}
        self.map.add_hero_swap(hero_data)

    def convert_timefile_to_datetime(self, time_string):

        # Utilisation de strptime pour convertir la chaîne en datetime
        time_delta = datetime.strptime(time_string, "[%H:%M:%S]")

        # Conversion en timedelta (représentation de la durée)
        duration = timedelta(hours=time_delta.hour, minutes=time_delta.minute, seconds=time_delta.second)
        return duration


# for file in os.listdir("../logs"):
#     if file.endswith(".txt"):
#         print(file)
#         la = LogAnalyser('../logs/{}'.format(file), file)
#         la.run()

# la = LogAnalyser('../logs/Log-2023-12-22-21-12-32.txt', "Log-2023-12-22-21-12-32.txt")
# la.run()