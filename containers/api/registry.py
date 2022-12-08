from typing import Dict

REGISTRY: Dict[str, str] = {
    "NR3C4": "26/27a2e03d24c047a3a28636f0e83b2cd5/artifacts/model/Random_Forest_Ensemble.pkl"
}

def get_model_path(protein) -> str:
    return REGISTRY[protein]