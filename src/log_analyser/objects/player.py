# from src.log_analyser.character import Character


class Player():
    
    def __init__(self, name, team) -> None:
        
        self.name = name
        self.team = team
        
        self.character = []
        
        self.ultimate = 0
            
    def add_event(self, event):
        pass
    
    def add_character(self, character):
        self.character.append(character)