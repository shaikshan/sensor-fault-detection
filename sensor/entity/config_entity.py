from datetime import datetime
from sensor.constants import training_pipeline
from sensor.constants.training_pipeline import *
from sensor.exception import SensorException
import os,sys
class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        try:
            timestamp = timestamp.strftime('%m_%d_%Y-%H_%M_%S')
            self.pipeline_name:str = training_pipeline.PIPELINE_NAME 
            self.artifact_dir_path = os.path.join(training_pipeline.ARTIFACT_DIR,timestamp)
            self.timestamp = timestamp
        except Exception as e:
            raise SensorException(e,sys)
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_ingestion_dir = os.path.join(
                training_pipeline_config.artifact_dir_path,training_pipeline.DATA_INGESTION_DIR_NAME
            )
            self.feature_store_file_path = os.path.join(
                self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                training_pipeline.FILE_NAME
            )
            self.training_file_path = os.path.join(
                self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.TRAIN_FILE_NAME
                )
            self.testing_file_path = os.path.join(
                self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.TEST_FILE_NAME
            )
            self.train_test_split_ratio:float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME 
        except Exception as e:
            raise SensorException(e,sys)

