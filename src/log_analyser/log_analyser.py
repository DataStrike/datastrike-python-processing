import pandas as pd


class LogAnalyser:
    
    def __init__(self, path_csv) -> None:
        
        self.path_csv = path_csv
        

        
    def run(self):
        
        with open(self.path_csv, encoding='utf-8') as my_file:
            line = my_file.read()
            line_split = line.split(",")
            print(line_split)

            timestamp = line_split[0]
            type = line_split[1]


    def process_kill(self):
        pass
    
    
    def process_ultimate_charged(self):
        pass
    
    def process_round_start(self):
        pass
    
    def process_round_stop(self):
        pass
    
    def process_match_start(self):
        pass

la = LogAnalyser('src/logs/Log-2023-12-22-21-12-32.txt')
la.run()