from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
import os,sys
import dill
from sensor.util.main_utils import save_numpy_array_data,save_object
from imblearn.combine import SMOTETomek
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from sensor.constants.training_pipeline import TARGET_COLUMN
import pandas as pd
import numpy as np
from sensor.ml.model.estimator import TargetValueMapping

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SensorException(e,sys)
    
    @staticmethod
    def load_dataframe(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
    
    @classmethod
    def get_data_transformer_object(cls,):
        try:
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant",fill_value=0)

            preprocessor = Pipeline(
                steps=[
                ("Imputer",simple_imputer),#Replace missing values with zero
                ("Robustscaler",robust_scaler)#keep every feature in same range and handle outlier
                ]
            )
            
            return preprocessor
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_data_transformation(self,)->DataTransformationArtifact:
        try:
            logging.info("Reading train and test data in DataFrame")
            train_df = DataTransformation.load_dataframe(file_path=
            self.data_validation_artifact.valid_train_file_path)

            test_df = DataTransformation.load_dataframe(file_path=
            self.data_validation_artifact.valid_test_file_path)

            preprocessor = self.get_data_transformer_object()
            
            #training dataframe
            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())

            #testing dataframe
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())

            #tranforming training and testing data
            preprocessor_object = preprocessor.fit(input_features_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_features_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_features_test_df)

            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final,target_feature_train_final = smt.fit_resample(
                transformed_input_train_feature,target_feature_train_df
            )
            input_feature_test_final,target_feature_test_final = smt.fit_resample(
                transformed_input_test_feature,target_feature_test_df
            )

            #Concatinating and converting training and testing into array.
            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]

            #save numpy array data
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,
            array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,
            array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,
            obj=preprocessor)

            #preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            logging.info(f"Data transformation artifact:{data_transformation_artifact}")
            
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)