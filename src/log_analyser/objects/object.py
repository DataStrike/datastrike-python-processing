import json
from datetime import datetime

class Object:
    def __init__(self, class_model, **kwargs):   
        
        self.from_json_ok = True
        self.class_name = self.__class__.__name__
    
        for key, value in kwargs.items():
            if key in class_model:
                if type(value) == class_model[key]:
                    setattr(self, key, value)
                else:
                    print("type of key {} is invalid".format(class_model, key))
                    self.from_json_ok = False
            else:
                print("key {} not find in dataschema".format(key))
                self.from_json_ok = False

    def export_json_recursive(self, data):
        if issubclass(type(data), Object):
            dict_class = data.__dict__.copy()
            dict_class.pop("from_json_ok")
            return data.export_json_recursive(dict_class)
        elif isinstance(data, datetime):
            return data.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(data, list):
            return [self.export_json_recursive(item) for item in data]
        elif isinstance(data, dict):
            return {key: self.export_json_recursive(value) for key, value in data.items()}
        else:
            return data

    def export_json(self):
        
        dict_class = self.__dict__.copy()
        dict_class.pop("from_json_ok")
        for key, value in dict_class.items():
            dict_class[key] = self.export_json_recursive(value)

        return json.dumps(dict_class)



    @classmethod
    def from_json(self, data):
        object = self(**data)
        if object.from_json_ok:
            return object
        else:
            return None

