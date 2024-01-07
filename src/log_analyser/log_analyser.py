import os
from datetime import datetime, timedelta
from log_analyser.objects.match import Match


class LogAnalyser:
    
    def __init__(self, path_csv, name) -> None:
        
        self.path_csv = path_csv
        self.name = name
        
        self.date = self.name2datetime()
        
        self.match = None
        
        self.actions = {"match_start": self.process_match_start}
        
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

        # with open("../logs_process/{}.json".format(self.name.split(".")[0]), "w") as file:
        #     file.write(self.match.export_json())


    def name2datetime(self):
        
        date_string = self.name.split(".")[0].split("Log-")[1]
        date_object = datetime.strptime(date_string, '%Y-%m-%d-%H-%M-%S')
        
        return date_object

    def process_match_start(self, data):

        self.match = Match.from_json({"rounds": [], 
                       "date": self.date,
                       "map_name": data[3],
                       "map_type": data[4],
                       "team1_name": data[5],
                       "team2_name": data[6],
                       "score_team1": 0,
                       "score_team2": 0,
                       })

        self.actions = {"match_start": self.process_match_start,
                        "round_start": self.match.add_round,
                        "round_end": self.match.end_round,
                        "hero_spawn": self.process_hero_spawn,
                        "hero_swap": self.process_hero_swap,
                        "kill": self.match.add_kill,
                        "ultimate_charged": self.match.add_ultimate_charged,
                        "ultimate_start": self.match.add_ultimate_start,
                        "ultimate_end": self.match.add_ultimate_end,
                        "objective_captured": self.match.add_objective_captured,
                        "player_stat": self.match.add_player_stat,
                        "point_progress": self.match.add_objective_progress,
                        "payload_progress": self.match.add_objective_progress,
                        }

    def process_hero_spawn(self, data):

        player_data = {"time": data[2], "team_name": data[3], "player_name": data[4], "character_name": data[5]}
        self.match.add_player(player_data)

    def process_hero_swap(self, data):

        hero_data = {"time": data[2], "team_name": data[3], "player_name": data[4], "character_name": data[5], "character_swap": data[6]}
        self.match.add_hero_swap(hero_data)

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