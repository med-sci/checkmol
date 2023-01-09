import yaml

from yaml import SafeLoader
from sklearn.metrics import r2_score
from ray import tune

METRICS = {
    'r2_score': r2_score
}

def parse_space_from_file(path):
    with open(path, 'rt') as file:
        space_dict = yaml.load(file, SafeLoader)

    return {key: tune.choice(value) for key, value in space_dict.items()}



def get_metric(metric: str):
    return METRICS.get(metric)