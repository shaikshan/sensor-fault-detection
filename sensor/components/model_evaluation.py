from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import ModelEvaluationArtifact,DataValidationArtifact,ModelTrainerArtifact
from sensor.util.main_utils import *
import os,sys
import pandas as pd
from sensor.constants.training_pipeline import *
from sensor.ml.model.estimator import TargetValueMapping,ModelResolver,SensorModel
from sensor.ml.metric.classification_metric import get_classification_score

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                model_training_aritifact:ModelTrainerArtifact,
                data_validation_aritfact:DataValidationArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.model_training_artifact = model_training_aritifact
            self.data_validation_aritfact = data_validation_aritfact
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_evaluation(self,)->ModelEvaluationArtifact:
        try:
            valid_train_file_path = self.data_validation_aritfact.valid_train_file_path
            valid_test_file_path = self.data_validation_aritfact.valid_test_file_path

            #valid train and test file dataframe
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)
            logging.info(f"Loading Train and test dataset into dataframe.")

            df = pd.concat([train_df,test_df])
            logging.info(f"Concatinating Train and Test dataframe into df.")
            
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(),inplace=True)
            logging.info(f"Replacing target column values into 0 and 1")

            df.drop(TARGET_COLUMN,axis=1,inplace=True)
            logging.info(f"Droping target column from df.")

            trained_model_file_path = self.model_training_artifact.trained_model_file_path
            model_resolver = ModelResolver()
            is_model_accepted = True

            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    trained_model_path=trained_model_file_path,
                    trained_model_metric_artifact=self.model_training_artifact.test_metric_artifact,
                    best_mode_metric_artifact=None
                    )
                logging.info(f"Model evaluation artifact:{model_evaluation_artifact}")
                return model_evaluation_artifact

            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=trained_model_file_path)

            y_trained_pred = train_model.predict(df)
            y_latest_pred = latest_model.predict(df)

            trained_metric = get_classification_score(y_true=y_true,y_pred=y_trained_pred)
            latest_metric = get_classification_score(y_pred=y_latest_pred,y_true=y_true)

            improved_accuracy = trained_metric.f1_score-latest_metric.f1_score
            if self.model_evaluation_config.change_threshold < improved_accuracy:
                is_model_accepted=True
            else:
                is_model_accepted = False

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path=latest_model_path,
                trained_model_path=trained_model_file_path,
                trained_model_metric_artifact=trained_metric,
                best_mode_metric_artifact=latest_metric
            )
            logging.info(f"Model evaluation artifact:{model_evaluation_artifact}")


            #save model_evaluation_artifact as report
            model_eval_report = model_evaluation_artifact.__dict__
            write_yaml_file(file_path=self.model_evaluation_config.report_file_path, content = model_eval_report)
            logging.info(f"Generating model evaluation report from:{model_eval_report}")

            return model_evaluation_artifact

        except Exception as e:
            raise SensorException(e,sys)