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
        
        teams = []
        teams.append(Team.from_json({"name":self.team1_name, "players": []}))
        teams.append(Team.from_json({"name":self.team2_name, "players": []}))
        self.rounds.append(Round.from_json({"teams": teams}))
        
        self.actual_round += 1
        
    def add_player(self, data):
        
        for team in self.rounds[self.actual_round].teams:
            
            for player in team.players:
                
                if player.name == data["name"]:
                    return -1
        
        self.rounds[self.actual_round].teams[data["team_number"]].add_player(data)
        
                    
            
        