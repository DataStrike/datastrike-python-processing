import json


class Object:
    def __init__(self, class_model, **kwargs):   
        
        self.from_json_ok = True
    
        for key, value in kwargs.items():
            if key in class_model:
                print(type(value), class_model[key])
                if type(value) == class_model[key]:
                    setattr(self, key, value)
                else:
                    print("type of key {} is invalid".format(class_model, key))
                    self.from_json_ok = False
            else:
                print("key {} not find in dataschema".format(key))
                self.from_json_ok = False
                
    def export_json(self):
        
        dict_class = self.__dict__
        dict_class.pop("from_json_ok")
        return json.dumps(dict_class)
    
    @classmethod
    def from_json(self, data):
        object = self(**data)
        if object.from_json_ok:
            return object
        else:
            return None