from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd
import numpy as np
import yaml
import os,sys
import dill

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise SensorException(e,sys)

def write_yaml_file(file_path:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)

    except Exception as e:
        raise SensorException(e,sys)

def save_numpy_array_data(file_path:str,array:np.array):
    """

    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise SensorException(e,sys)
    
def load_numpy_array_data(file_path:str,)->np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e,sys)

def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("Entered the save object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited the save object method of MainUtils class")
    except Exception as e:
        raise SensorException(e,sys)

def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e,sys)