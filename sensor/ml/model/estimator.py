from sensor.exception import SensorException
from sensor.logger import logging

class TargetValueMapping:
    def __init__(self,):
        self.neg:int = 0
        self.pos:int = 1
    
    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_object = self.to_dict()
        return dict(zip(mapping_object.values(),mapping_object.keys()))
