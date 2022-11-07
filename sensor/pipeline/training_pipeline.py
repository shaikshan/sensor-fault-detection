from sensor.constants import training_pipeline
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,\
DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
import os,sys
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact,\
ModelTrainerArtifact,ModelPusherArtifact,ModelEvaluationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher

class TrainPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("DataIngestion Started")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info(f"DataIngestion Completed and artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("DataValidation Started")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info(f"Data Validation is Completed and artifact:{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("DataTransformation Started")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
            logging.info(f"Data Transformation is completed and artifact:{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Model Training is Started")
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                        data_transformation_artifact=data_transformation_artifact)

            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training is completed and artifact:{model_trainer_config}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_evaluation(self,model_trainer_artifact:ModelTrainerArtifact,
                                data_validation_artifact:DataValidationArtifact)->ModelEvaluationArtifact:
        try:
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"{'<<*15'}Model Evaluation is Started{'>>*15'}")
            model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                    model_training_aritifact=model_trainer_artifact,data_validation_aritfact=data_validation_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info(f"{'<<*15'}Model Evaluation is Completed{'>>*15'}")
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"{'<<*15'}Model Pusher is started{'>>*15'}")
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config,model_evaluation_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info(f"{'<<*15'}Model Pusher is completed{'>>*15'}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_aritfact:ModelTrainerArtifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )
            model_evaluation_artifact:ModelEvaluationArtifact = self.start_model_evaluation(
                model_trainer_artifact=model_trainer_aritfact,data_validation_artifact=data_validation_artifact
            )
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model ")
            model_pusher_artifact:ModelPusherArtifact = self.start_model_pusher(
                model_evaluation_artifact=model_evaluation_artifact
            )

            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)