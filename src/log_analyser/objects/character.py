from objects.object import Object


class Character(Object):
    
    def __init__(self, **kwargs):
        
        data_schema = {"name": str}
        
        super().__init__(data_schema, **kwargs)

        self.played_time = []
        self.stats = {}
        self.kills = []
        self.deads = []
        self.offensive_assists = []
        self.defensive_assists = []
        self.ultimate_charged = []
        self.ultimate_use = []

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
    def add_ultimate_stop(self, data):
        self.ultimate_end[-1]["end"] = data["date"]
    def add_character_stats(self, data):
        self.stats = data