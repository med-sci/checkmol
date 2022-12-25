from typing import Dict

REGISTRY: Dict[str, str] = {
    "NR3C4": {
        "model": '37/1904276dabdc4c95b192b3ed7e171f81/artifacts/model/Random_Forest_Ensemble.pkl',
        "scaler": "NR3C4_standard_value_Test_Scaler_184c8d04783246a7962fa7140fbf2ae9/scaler/scaler.pkl"
    },
    "VEGFR2": {
        "model": '43/dbb7def4733345bea746e86288c487d2/artifacts/model/Random_Forest_Ensemble.pkl',
        "scaler": "VEGFR2_standard_value_Train_for_prod_2aaf6ee232f94863b17c376e4dc187ad/scaler/scaler.pkl"
    },
    "EGFR": {
        "model": '42/527915b92b8540bb874dfab7297d1ee9/artifacts/model/Random_Forest_Ensemble.pkl',
        "scaler": "EGFR_standard_value_4h_5b586f44483143fbacb0bae736a7d32e/scaler/scaler.pkl"
    }
}

def get_model_path(protein) -> str:
    return REGISTRY[protein]['model']

def get_scaler_path(protein) -> str:
    return REGISTRY[protein]['scaler']