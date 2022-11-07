from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
from sensor.entity.config_entity import ModelPusherConfig
import os,sys
from sensor.util.main_utils import *
from sensor.constants.training_pipeline import *
import shutil

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_pusher(self,):
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path

            #Creating model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=model_file_path)
            logging.info(f"creating directory of model and copying... trained model")

            #saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=saved_model_path)
            logging.info(f"creating saved_model_dir and coping.... trained model..")
            
            #prepare artifact
            logging.info(f"Preparing model pusher artifact")
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path,
                                                        model_file_path=model_file_path)

            logging.info(f"Model Pusher Artifact:{model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)