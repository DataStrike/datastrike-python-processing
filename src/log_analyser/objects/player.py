# from src.log_analyser.character import Character
from objects.object import Object
from objects.character import Character


class Player(Object):
    
    def __init__(self, name, team) -> None:
        
        data_schema = {"name": str, 
                       "characters": list}
        
        super().__init__(data_schema, **kwargs)
        
            
    def add_event(self, event):
        pass
    
    def add_character(self, character):
        self.character.append(character)