import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from rdkit import Chem
from rdkit.Chem import Descriptors
from tqdm import tqdm


def get_dataframe(path: str):
    return pd.read_csv(path)


def drop_duplicates(dataframe: pd.DataFrame):
    return dataframe.drop_duplicates()


def drop_nan(dataframe: pd.DataFrame):
    return dataframe.dropna()


def get_target(dataframe: pd.DataFrame, target: str):
    return dataframe[target].to_numpy()


def calculate_features(dataframe: pd.DataFrame, smiles_col: str):
    smiles = dataframe[smiles_col].to_list()
    molecules = [Chem.MolFromSmiles(s) for s in smiles]
    return np.array([[descriptor_func(molecule) for _, descriptor_func
                      in Descriptors.descList]
                      for molecule in tqdm(molecules)])

def scale_features(features):
    scaler = MinMaxScaler()
    return scaler.fit_transform(features)

def log_10_target(target: np.ndarray):
    return np.log10(target)