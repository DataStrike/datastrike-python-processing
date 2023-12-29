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
                        "hero_spawn": self.process_hero_spawn}
        
    def run(self):
        
        with open(self.path_csv, encoding='utf-8') as my_file:
            line = my_file.read()
            line_split = line.split(",")
            # print(line_split)

            timestamp = line_split[0]
            type = line_split[1]
            
            if type in self.actions:
                self.actions[type](line_split)


    def name2datetime(self):
        
        date_string = self.name.split(".")[0].split("Log-")[1]
        date_object = datetime.strptime(date_string, '%Y-%m-%d-%H-%M-%S')
        
        return date_object
        

    def process_kill(self):
        pass
    
    
    def process_ultimate_charged(self):
        pass
    
    def process_round_start(self):
        
        self.match.add_round()
    
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
        pass
        
        

la = LogAnalyser('src/logs/Log-2023-12-22-21-12-32.txt', "Log-2023-12-22-21-12-32.txt")
la.run()