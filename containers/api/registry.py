from typing import Dict

REGISTRY: Dict[str, str] = {
    "NR3C4": {
        "model": "26/27a2e03d24c047a3a28636f0e83b2cd5/artifacts/model/Random_Forest_Ensemble.pkl",
        "scaler": "path/to/scaler"
    }
}

def get_model_path(protein) -> str:
    return REGISTRY[protein]['model']

def get_scaler_path(protein) -> str:
    return REGISTRY[protein]['scaler']