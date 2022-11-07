from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from sensor.constants.training_pipeline import *

class TargetValueMapping:
    def __init__(self):
        self.neg:int = 0
        self.pos:int = 1
    
    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_object = self.to_dict()
        return dict(zip(mapping_object.values(),mapping_object.keys()))


#Write a code for train a model and check the accuracy

class SensorModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise SensorException(e,sys)

    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise SensorException(e,sys)

class ModelResolver:

    def __init__(self,model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SensorException(e,sys)

    def get_best_model_path(self,):
        try:
            timestamps = list(map(int ,os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME)
            return latest_model_path
        except Exception as e:
            raise SensorException(e,sys)

    def is_model_exists(self,):
        try:
            if not os.path.exists(self.model_dir):
                return False
            
            timestamps = os.listdir(self.model_dir)
            if len(timestamps)==0:
                return False
            
            latest_model_file_path = self.get_best_model_path()
            if not os.path.exists(latest_model_file_path):
                return False
            
            return True
        except Exception as e:
            raise SensorException(e,sys)



