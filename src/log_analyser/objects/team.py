from objects.object import Object
from objects.player import Player

class Team(Object):
    
    def __init__(self, **kwargs):
        
        data_schema = {"name": str, 
                       "players": dict}
        
        super().__init__(data_schema, **kwargs)
    
    
    def add_player(self, data):
        
        self.players[data["name"]] = Player.from_json(data)