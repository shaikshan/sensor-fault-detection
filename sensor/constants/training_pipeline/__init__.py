import os

from sensor.constants.s3_bucket import TRAINING_BUCKET_NAME

SAVED_MODEL_DIR = "saved_models"

#defining common constant variable for training pipeline
TARGET_COLUMN = "class"
PIPELINE_NAME:str = "sensor"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "sensor.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"

# Data ingestion related constants start with DATA_INGESTION VAR NAME

DATA_INGESTION_COLLECTION_NAME: str = "car"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


"""
Data Validation related constants start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

"""
Data Transformation related constants start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"

"""
Model Training constants 
"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05

"""
Model Evaluation constants
"""

MODEL_EVALUATION_DIR_NAME:str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float = 0.02
MODEL_EVALUATION_REPORT_NAME = "report.yaml"

"""
MODEL PUSHER CONSTANTS
"""
MODEL_PUSHER_DIR_NAME = 'model_pusher'
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR