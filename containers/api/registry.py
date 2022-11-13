from typing import Dict

REGISTRY: Dict[str, str] = {
    "NR3C4": "76/effe61bfaa14418cb3f606c2a7edf0d4/artifacts/model/Random_Forest_Ensemble.pkl"
}

def get_model_path(protein) -> str:
    return REGISTRY[protein]