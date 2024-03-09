from log_analyser.objects.object import Object
import json
import os


class Character(Object):
    def __init__(self, **kwargs):

        data_schema = {"name": str,
                       "stats": dict,
                       "played_time": list,
                       "kills": list,
                       "deaths": list,
                       "ultimate_charged": list,
                       "ultimate_use": list,
                       "role": str}

        super().__init__(data_schema, **kwargs)
        self.role = self.find_role()

    def find_role(self):

        roles_file = 'log_analyser/roles/roles.json'
        lang_folder = 'log_analyser/roles/lg'

        roles_data = self.load_roles(roles_file)

        role = self.find_character_role(self.name, roles_data, lang_folder)
        return role
    def add_played_time(self, data):
        self.played_time.append(data)

    def add_start_time(self, data):

        if len(self.played_time) > 0:
            if "end" not in self.played_time[-1] and self.played_time[-1]["start"] == data["start"]:
                pass
            else:
                self.played_time.append(data)

    def add_end_time(self, data):
        if len(self.played_time) == 0:
            return -1
        self.played_time[-1]["end"] = data["end"]

    def add_kill(self, data):
        self.kills.append(data)

    def add_death(self, data):
        self.deaths.append(data)

    def add_offensive_assist(self, data):
        self.offensive_assists.append(data)

    def add_defensive_assist(self, data):
        self.defensive_assists.append(data)

    def add_ultimate_charged(self, data):
        self.ultimate_charged.append(data)

    def add_ultimate_start(self, data):
        self.ultimate_use.append(data)

    def add_ultimate_end(self, data):

        if len(self.ultimate_use) == 0:
            return -1
        self.ultimate_use[-1]["end"] = data["end"]

    def add_character_stats(self, data):
        self.stats = data

    def load_roles(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            roles_data = json.load(file)
        return roles_data

    def find_character_role(self, character_name, roles_data, lang_folder):
        for role in roles_data:
            if character_name in roles_data[role]:
                return role
        else:
            for lang_file in os.listdir(lang_folder):
                lang_file_path = os.path.join(lang_folder, lang_file)
                if os.path.isfile(lang_file_path) and lang_file.endswith('.json'):
                    with open(lang_file_path, 'r', encoding='utf-8') as file:
                        lang_data = json.load(file)
                    if character_name in lang_data:
                        name = lang_data[character_name]
                        for role in roles_data:
                            if name in roles_data[role]:
                                return role
        return None
