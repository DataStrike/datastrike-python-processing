import json
from datetime import datetime, timedelta

class Object:
    def __init__(self, class_model, **kwargs):   
        
        self.from_json_ok = True
        self.class_name = self.__class__.__name__
        self.class_model = class_model
    
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

        for key, value in class_model.items():
            if not hasattr(self, key):
                print("key {} not find in object".format(key, value()))
                setattr(self, key, value())

    def export_json_recursive(self, data):
        if issubclass(type(data), Object):

            dict_class = data.__dict__.copy()
            dict_class_final = dict_class.copy()

            for key, value in dict_class.items():
                if not key in data.class_model and key != "class_name":
                    dict_class_final.pop(key)

            return data.export_json_recursive(dict_class_final)
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

        dict_class_final = dict_class.copy()

        for key, value in dict_class.items():
            if not key in self.class_model and key != "class_name":
                dict_class_final.pop(key)
            else:
                dict_class_final[key] = self.export_json_recursive(value)
        # return json.dumps(dict_class_final, indent=4, sort_keys=True, default=str)
        return json.dumps(dict_class_final, skipkeys=False, ensure_ascii=True, check_circular=True)
    def convert_timefile_to_datetime(self, time_string):


        # Utilisation de strptime pour convertir la chaîne en datetime
        time_delta = datetime.strptime(time_string, "[%H:%M:%S]")

        # Conversion en timedelta (représentation de la durée)
        duration = timedelta(hours=time_delta.hour, minutes=time_delta.minute, seconds=time_delta.second)
        return duration

    @classmethod
    def from_json(self, data):
        object = self(**data)
        if object.from_json_ok:
            return object
        else:
            return None

