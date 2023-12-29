from object import Object


class Character(Object):
    
    def __init__(self, **kwargs):
        
        data_schema = {"name": str, 
                       "age": int}
        
        super().__init__(data_schema, **kwargs)
    
    def __print__(self):
        print(vars(self))
    
character = Character.from_json({"name": "ok", "age": 3})

character.__print__()

print(character.export_json())