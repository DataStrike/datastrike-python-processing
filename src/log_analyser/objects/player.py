# from src.log_analyser.character import Character
from objects.object import Object
from objects.character import Character


class Player(Object):

    def __init__(self, **kwargs) -> None:
        data_schema = {"name": str,
                       "characters": dict}

        super().__init__(data_schema, **kwargs)

    def add_event(self, event):
        pass

    def add_character(self, data):
        self.characters[data["name"]] = Character.from_json(data)
