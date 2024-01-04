from objects.object import Object
from objects.team import Team


class Round(Object):
    
    def __init__(self, **kwargs):
        
        data_schema = {"teams": dict,
                       "start_time": str,
                       "objective_captured": list,
                       "objective_progress": list
                       }
        
        super().__init__(data_schema, **kwargs)

    def add_objective_captured(self, data):
        self.objective_captured.append(data)

    def add_objective_progress(self, data):
        self.objective_progress.append(data)