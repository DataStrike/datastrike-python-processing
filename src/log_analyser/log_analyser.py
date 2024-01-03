from datetime import datetime
from objects.match import Match


class LogAnalyser:
    
    def __init__(self, path_csv, name) -> None:
        
        self.path_csv = path_csv
        self.name  = "Log-2023-12-22-21-12-32.txt"
        
        self.date = self.name2datetime()
        
        self.match = None
        
        self.actions = {"match_start": self.process_match_start,
                        "round_start": self.process_round_start,
                        "hero_spawn": self.process_hero_spawn,
                        "hero_swap": self.process_hero_swap
                        }
        
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

        self.match.export_json()


    def name2datetime(self):
        
        date_string = self.name.split(".")[0].split("Log-")[1]
        date_object = datetime.strptime(date_string, '%Y-%m-%d-%H-%M-%S')
        
        return date_object
        

    def process_kill(self):
        pass
    
    
    def process_ultimate_charged(self):
        pass
    
    def process_round_start(self, data):
        
        self.match.add_round()
        # self.match.export_json()
    def process_round_stop(self):
        pass
    
    def process_match_start(self, data):

        self.match = Match.from_json({"rounds": [], 
                       "date": self.date,
                       "map_name": data[3],
                       "map_type": data[4],
                       "team1_name": data[5],
                       "team2_name": data[6]
                       })

    def process_hero_spawn(self, data):

        player_data = {"team_name": data[3], "player_name": data[4], "character_name": data[5]}
        self.match.add_player(player_data)

    def process_hero_swap(self, data):

        hero_data = {"team_name": data[3], "player_name": data[4], "character_name": data[6]}
        self.match.add_player(hero_data)


la = LogAnalyser('../logs/Log-2023-12-22-21-12-32.txt', "Log-2023-12-22-21-12-32.txt")
la.run()