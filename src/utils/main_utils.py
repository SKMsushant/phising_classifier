import sys
from typing import Dict,Tuple
import os

import numpy as np
import pandas as pd
import pickle
import yaml
import boto3

from src.constant import *
from src.exception import CustomException
from src.logger import logging

class MainUtils:
    def __init__(self)->None:
        pass
    
    def read_yaml_file(self,filename:str)->dict:
        """
        Reads a YAML file and returns its contents as a dictionary.

        :param filename: str: Path to the YAML file.
        :return: Dict: Contents of the YAML file.
        """
        try:
            with open(filename, 'rb') as file:
                return yaml.safe_load(file)
            
        except Exception as e:
            raise CustomException(e, sys) from e
            
    def read_schema_config_file(self)->dict:
        """
        Reads the schema configuration file and returns its contents as a dictionary.

        :return: Dict: Contents of the schema configuration file.
        """
        try:
            schema_config = self.read_schema_config_file(os.path.join('config', 'training_schema.yaml'))
            return schema_config
        except Exception as e:
            raise CustomException(e, sys) from e
        
    @staticmethod
    def save_object(file_path:str, obj:object)->None:
        """
        Saves an object to a file using pickle.

        :param file_path: str: Path to the file where the object will be saved.
        :param object: object: The object to be saved.
        """
        try:
            #writing trained model in binary and dumping in pickle format
            with open(file_path, 'wb') as file_obj:
                obj=pickle.dump(object, file_obj)
            logging.info("exited the save_object method of MainUtils class")

            return obj

        except Exception as e:
            raise CustomException(e, sys) from e
    @staticmethod
    def load_object(file_path:str)->object:
        logging.info("entered the load_object method of MainUtils class")

        """
        Loads an object from a file using pickle.

        :param file_path: str: Path to the file from which the object will be loaded.
        :return: object: The loaded object.
        """
        try:
            with open(file_path, 'rb') as file_obj:
                obj=pickle.load(file_obj)
            
            logging.info("exited the load_object method of MainUtils class")

            return obj
        except Exception as e:
            raise CustomException(e, sys) from e
        
    @staticmethod
    def upload_file_to_s3_bucket(from_filename,to_filename, bucket_name)->None:
        """
        Uploads a file to an S3 bucket.

        :param file_name: str: Path to the file to be uploaded.
        :param bucket_name: str: Name of the S3 bucket.
        :param object_name: str: Name of the object in the S3 bucket.
        """
        try:
            s3_resource = boto3.resource('s3')
            s3_resource.meta.client.upload_file(from_filename, to_filename,bucket_name,)
            logging.info(f"File {from_filename} uploaded to S3 bucket {bucket_name} as {to_filename}.")
        except Exception as e:
            raise CustomException(e, sys) from e
        
    @staticmethod
    def download_model(bucket_name,bucket_file_name,dest_file_name)->None:
        """
        Downloads a file from an S3 bucket.

        :param bucket_name: str: Name of the S3 bucket.
        :param bucket_file_name: str: Name of the file in the S3 bucket.
        :param dest_file_name: str: Path to save the downloaded file.
        """
        try:
            s3_client = boto3.client('s3')
            s3_client.download_file(bucket_name, bucket_file_name, dest_file_name)
            logging.info(f"File {bucket_file_name} downloaded from S3 bucket {bucket_name} to {dest_file_name}.")
            return dest_file_name
        except Exception as e:
            raise CustomException(e, sys) from e
        
    @staticmethod
    def remove_unwanted_spaces(data:pd.DataFrame)->pd.DataFrame:
        """
        Removes unwanted spaces from the columns of a DataFrame.

        :param data: pd.DataFrame: Input DataFrame.
        :return: pd.DataFrame: DataFrame with unwanted spaces removed.
        On failure:Raise Exception
        """
        try:
            df_without_spaces=data.apply(
                lambda x:x.str.strip() if x.dtype=='object' else x
            )
            logging.info("Unwanted space Removed.exited the remove_unwanted_spaces method of MainUtils class")
            return df_without_spaces
        except Exception as e:
            raise CustomException(e, sys) from e
        
    @staticmethod
    def identify_feature_types(dataframe:pd.DataFrame):
        data_types=dataframe.dtypes

        categorical_features = []
        continuous_features = []
        discrete_features = []
        for column,dtype in dict(data_types).items():
            unique_values = dataframe[column].nunique()
            
            
            # Check if the column is categorical, continuous, or discrete based on the number of unique values and data type
            if dtype == 'object' or unique_values < 10:  # Consider features with less than 10 unique values as categorical
                categorical_features.append(column)
            elif dtype in [np.int64, np.float64]:  # Consider features with numeric data types as continuous or discrete
                if unique_values > 20:  # Consider features with more than 20 unique values as continuous
                    continuous_features.append(column)
                else:
                    discrete_features.append(column)
            else:
                # Handle other data types if needed
                pass

        return categorical_features, continuous_features, discrete_features