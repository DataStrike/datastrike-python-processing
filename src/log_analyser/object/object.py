import json


class Object:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def export_json(self):
        
        return json.dumps(self.__dict__)
    
    @classmethod
    def from_json(self, data):
        return self(**data)