import pandas as pd
import numpy as np
from minio import Minio
import os

from rdkit import Chem
from rdkit.Chem import Descriptors
from tqdm import tqdm


def load_from_s3(
    client: Minio,
    bucket_name: str,
    file_path: str
):
    temp_path = os.path.join('/tmp/', file_path)
    client.fget_object(
        bucket_name=bucket_name,
        object_name=file_path,
        file_path=temp_path
    )
    return temp_path


def upload_to_s3(
    client: Minio,
    bucket_name: str,
    file_path: str,
    bucket_path: str
):
    client.fput_object(
        bucket_name=bucket_name,
        object_name=bucket_path,
        file_path=file_path
    )


def get_dataframe(path: str):
    return pd.read_csv(path)


def drop_duplicates(dataframe: pd.DataFrame):
    return dataframe.drop_duplicates(inplace=True)


def drop_nan(dataframe: pd.DataFrame):
    return dataframe.dropna(inplace=True)


def get_target(dataframe: pd.DataFrame, target: str):
    return dataframe[target].to_numpy()


def write_target(target_array: np.ndarray, path: str):
    with open(path, 'wb') as file:
        np.save(file, target_array)


def calculate_features(dataframe: pd.DataFrame, smiles_col: str):
    smiles = dataframe[smiles_col].to_list()
    molecules = [Chem.MolFromSmiles(s) for s in smiles]
    return np.array([[descriptor_func(molecule) for _, descriptor_func
                      in Descriptors.descList]
                      for molecule in tqdm(molecules)])


def write_features(features: np.ndarray, path: str):
    with open(path, 'wb') as file:
        np.save(file, features)


def log_10_target(target: np.ndarray):
    return np.log10(target)