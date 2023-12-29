from objects.object import Object
from objects.team import Team

class Round(Object):
    
    def __init__(self, **kwargs):
        
        data_schema = {"teams": list
                       }
        
        super().__init__(data_schema, **kwargs)
    
    