from typing import Dict

REGISTRY: Dict[str, str] = {
    "NR3C4": {
        "model": '37/1904276dabdc4c95b192b3ed7e171f81/artifacts/model/Random_Forest_Ensemble.pkl',
        "scaler": "NR3C4_standard_value_Test_Scaler_184c8d04783246a7962fa7140fbf2ae9/scaler/scaler.pkl"
    }
}

def get_model_path(protein) -> str:
    return REGISTRY[protein]['model']

def get_scaler_path(protein) -> str:
    return REGISTRY[protein]['scaler']