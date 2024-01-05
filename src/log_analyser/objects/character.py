from objects.object import Object


class Character(Object):
    def __init__(self, **kwargs):
        
        data_schema = {"name": str,
                       "stats": dict,
                       "played_time": list,
                       "kills": list,
                       "deaths": list,
                       "ultimate_charged": list,
                       "ultimate_use": list}
        
        super().__init__(data_schema, **kwargs)


    def add_played_time(self, data):
        self.played_time.append(data)

    def add_kill(self, data):
        self.kills.append(data)

    def add_death(self, data):
        self.deads.append(data)

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