from sensor.exception import SensorException
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import ClassificationMetricArtifact,ModelTrainerArtifact,DataTransformationArtifact
from sensor.logger import logging
import os,sys
from sensor.util.main_utils import *
from xgboost import XGBClassifier
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def perform_hyper_parameter_tuning(self,):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def train_model(self,x_train,y_train):
        try:
            xg_cls = XGBClassifier()
            xg_cls.fit(x_train,y_train)
            return xg_cls
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_model_trainer(self,)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            #Loading train and test array from train and test file path
            train_arr = load_numpy_array_data(file_path=train_file_path)
            test_arr = load_numpy_array_data(file_path=test_file_path)

            #splitting training and testing data into x_train,y_train,x_test,y_test
            x_train,y_train,x_test,y_test = (
                                            train_arr[:,:-1],
                                            train_arr[:,-1],
                                            test_arr[:,:-1],
                                            test_arr[:,-1]
                                            )
            
            model= self.train_model(x_train=x_train,y_train=y_train)
            y_train_pred = model.predict(X=x_train)
            classification_train_metric =  get_classification_score(y_pred=y_train_pred,y_true=y_train)

            if classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise Exception("Trained model is not good to provide expected accuracy")

            y_test_pred = model.predict(X=x_test)
            classification_test_metric = get_classification_score(y_pred=y_test_pred,y_true=y_test)

            #Overfitting and Underfitting
            diff = abs(classification_train_metric.f1_score-classification_test_metric.f1_score)

            if diff>self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good try to do more experimentation")
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            #Creating a directory for saving best model
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok = True)
            sensor_model = SensorModel(preprocessor=preprocessor,model=model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=sensor_model)

            #model trainer artifact

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric)

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e,sys)