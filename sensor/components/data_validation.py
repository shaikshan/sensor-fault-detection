from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from sensor.exception import SensorException, error_message_detail
from sensor.logger import logging
import os,sys
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import pandas as pd
from sensor.constants.training_pipeline import *
from sensor.util.main_utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e,sys)

    def is_numeric_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns
            
            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)

            logging.info(f"Missing numerical columns:[{missing_numerical_columns}]")
            return numerical_column_present

        except Exception as e:
            raise SensorException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
    
    def detect_data_drift(self,file_path)->bool:
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
    def get_data_drift_report(self,base_df,current_df,threshold=0.5)->bool:
        try:
            report = {}
            status = True
            True_count = 0
            False_count = 0
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                if is_found is True:
                    True_count += 1
                else:
                    False_count +=1
                if True_count >= len(base_df.columns)//2:
                    status = False
                report.update({column:{
                "p_value":float(is_same_dist.pvalue),
                "drift_status":is_found
                }})
            logging.info(f"True count of data_drift found:{True_count}")
            logging.info(f"False count of data_drift found:{False_count}")
            logging.info(f"Difference of True and count and no: of columns:{True_count-len(base_df.columns)}")
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            logging.info(f"Drift report is generated and exporting to:{drift_report_file_path}")
            
            #Creating directory
            dir_name = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_validation(self):
        try:
            erro_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Reading train and test data into DataFrame
            train_dataframe = DataValidation.read_data(file_path=train_file_path)
            test_dataframe = DataValidation.read_data(file_path=test_file_path)

            #Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{erro_message} Train dataframe does not contain all columns \n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{erro_message} Test dataframe does not contain all columns \n"

            #Validate numerical columns
            status = self.is_numeric_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain numerical columns"
            status = self.is_numeric_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain numerical columns"
            
            if len(erro_message)>0:
                raise Exception(erro_message)
                
            #Lets check data drift
            status = self.get_data_drift_report(base_df=train_dataframe,current_df=test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path= self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact 
        except Exception as e:
            raise SensorException(e,sys)

        
    

    