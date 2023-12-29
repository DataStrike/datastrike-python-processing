from object import Object


class Character(Object):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    
    def __print__(self):
        print(vars(self))
    
character = Character.from_json({"name": "ok", "test": "lol"})

character.__print__()