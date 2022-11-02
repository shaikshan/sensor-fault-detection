from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd
import numpy as np
import yaml
import os,sys

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