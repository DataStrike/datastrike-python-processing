# from src.log_analyser.character import Character
from log_analyser.objects.object import Object
from log_analyser.objects.character import Character


class Player(Object):

    def __init__(self, **kwargs) -> None:
        data_schema = {"name": str,
                       "characters": dict,
                       "role": str}

        super().__init__(data_schema, **kwargs)

    def add_event(self, event):
        pass

    def add_character(self, data):
        self.characters[data["name"]] = Character.from_json(data)

    def find_role(self):

        roles_time = {"Tank": 0, "DPS": 0, "Support": 0}
        for character in self.characters:
            character_role = self.characters[character].role
            if character_role:
                for play_time in self.characters[character].played_time:
                    if "end" in play_time and "start" in play_time:
                        roles_time[character_role] += float(play_time["end"]) - float(play_time["start"])

        self.role = max(roles_time, key=roles_time.get)