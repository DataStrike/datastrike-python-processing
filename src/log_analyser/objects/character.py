from objects.object import Object


class Character(Object):
    
    def __init__(self, **kwargs):
        
        data_schema = {"name": str, 
                       "damage": int}
        
        super().__init__(data_schema, **kwargs)
    
    
# character = Character.from_json({"name": "ok", "age": 3})
# character.__print__()
# print(character.export_json())