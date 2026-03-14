from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import *
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from src.utils.main_utils import *
from src.logger import get_logger
from src.exception import CustomException
from sklearn.tree import DecisionTreeClassifier
from src.entity.estimator import MyModel
import os 
import sys

logger = get_logger(__name__)

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):

        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config


    def get_model_object_and_report(self, train: np.array, test: np.array):
        


        x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
        y_train = y_train.astype(int)
        y_test = y_test.astype(int)
        print(np.isnan(y_train).any())
        logger.info("train-test split done.")
        
        logger.info("Model Initialized.")
        model = DecisionTreeClassifier(criterion=self.model_trainer_config._criterion, max_depth=self.model_trainer_config._max_depth)
        
        
        logger.info("Model training started")
        model.fit(x_train, y_train)
        logger.info("Model training done.")


        logger.info("Model Metrics Finding...")
        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        y_prob = model.predict_proba(x_test)[:, 1]
        auc_val = roc_auc_score(y_test, y_prob) if y_prob is not None else 0

        logger.info("Model Metrics Found.")

        model_result_artifact = ClassificationMetricArtifact(
            f1_score=f1,
            precision_score=precision,
            recall_score=recall,
            auc_roc=auc_val,
            accuracy=accuracy
        )
        logger.info("Model and Model Metric Sent.")

        return model, model_result_artifact

    def initiate_model_training(self):
        try:
            logger.info("=========== Model Trainer Component Started =================")
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            logger.info("train-test data loaded")

            trained_model, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            logger.info("Model object and artifact loaded.")

            logger.info("Preprocessor Object Loading..")
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            logger.info("Preprocessor Object Loaded.")

            logger.info("Model Object Creating")
            my_model = MyModel(preprocessing_object=preprocessing_obj, trained_model_object=trained_model)
            

            save_object(self.model_trainer_config.trained_model_file_path, my_model)

            model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            metric_artifact=metric_artifact,
            )
            print(metric_artifact)
            logger.info("Model Trainer Finished.")
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)