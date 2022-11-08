import json
from sklearn.metrics import r2_score
from ray import tune

METRICS = {
    'r2_score': r2_score
}

def parse_space_from_file(path):
    with open(path, 'rb') as file:
        space_dict = json.load(file)

    return {key: tune.choice(value['choices']) for key,
            value in space_dict.items()}



def get_metric(metric: str):
    return METRICS.get(metric)