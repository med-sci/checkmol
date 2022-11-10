import os
import numpy as np
import uuid
import random

from mlflow import MlflowClient
from mlflow.entities import RunStatus
from mlflow.tracking.context.registry import resolve_tags

from os.path import dirname, abspath
from functools import partial
from typing import Dict, Any
from sklearn.model_selection import KFold, train_test_split
from loguru import logger

from ray import tune
from ray.tune.search.optuna import OptunaSearch

from mlbase.utils import read_array, ClientS3

from train.models import RandomForest, EnsembleModel
from train.utils import parse_space_from_file, get_metric


ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
MLFLOW_TRACKING_URI = os.environ.get('MLFLOW_TRACKING_URI')

FEATURES_PATH = os.environ.get("FEATURES_PATH")
TARGET_PATH = os.environ.get("TARGET_PATH")
TARGET_NAME = os.environ.get("TARGET_NAME")
EXPERIMENT_CONDITION = os.environ.get("EXPERIMENT_CONDITION")

TMP_TARGET_PATH = os.path.join('/tmp', TARGET_PATH)
TMP_FEATURES_PATH = os.path.join('/tmp', FEATURES_PATH)
EXPERIMENT_NAME = f"{TARGET_NAME}_{EXPERIMENT_CONDITION}_{uuid.uuid4().hex}"

NUM_RUNS = int(os.environ.get("NUM_RUNS"))
N_SPLITS = int(os.environ.get("NUM_SPLITS"))
RANDOM_STATE = int(os.environ.get("RANDOM_STATE"))
MODE = os.environ.get("MODE")
METRIC = os.environ.get("METRIC")
METRIC_MODE = os.environ.get("METRIC_MODE")
TEST_SIZE = float(os.environ.get("TEST_SIZE"))
SEARCH_SPACE_PATH = os.path.join(dirname(abspath(__file__)), "search_spaces/random_forest.json")
TMP_MODEL_PATH = "/tmp/model/"

METRIC_TO_OPTIMIZE = f'{METRIC}_cv_mean'
METRIC_FUNC = get_metric(METRIC)

TAGS = {
    "Num runs": NUM_RUNS,
    "Num splits": N_SPLITS,
    "Mode": MODE,
    "Metric mode": METRIC_MODE,
    "Test size": TEST_SIZE,
    "Target name": TARGET_NAME
}
TAGS.update(resolve_tags())

np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)


def trainable(params: Dict[str, Any], mlflow_client: MlflowClient, exp_id: str):
    run = mlflow_client.create_run(exp_id)

    for tag, value in TAGS.items():
        mlflow_client.set_tag(run.info.run_id, tag, value)

    for param, value in params.items():
        mlflow_client.log_param(run.info.run_id, param, value)

    metrics = None
    try:
        features_train, features_test, target_train, target_test = train_test_split(
            features, target, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        kfd = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

        models = []
        scores = []
        for fold, (train_index, test_index) in enumerate(kfd.split(features_train)):
            logger.info(f"Starting training on fold {fold}")

            model = RandomForest(mode=MODE, params=params)
            model.fit(X=features_train[train_index], y=target_train[train_index])

            fold_preds = model.predict(features_train[test_index])
            score = METRIC_FUNC(y_true=target_train[test_index], y_pred=fold_preds)
            logger.info(f"{METRIC} for fold {fold}: {score}")
            mlflow_client.log_metric(run.info.run_id, f"{METRIC}_fold_{fold}", score)

            models.append(model)
            scores.append(score)

        logger.info('Ensemble model instantiation..')
        ensemble = EnsembleModel(models=models)

        logger.info('Predicting with ensemble model..')
        mean_test_preds = ensemble.predict(features_test)

        r2_score_test = METRIC_FUNC(target_test, mean_test_preds)
        metrics = {
            f'{METRIC}_test': r2_score_test,
            METRIC_TO_OPTIMIZE: np.mean(scores)
        }
        for metric, value in metrics.items():
            mlflow_client.log_metric(run.info.run_id, metric, value)

        model_path = f'/{exp_id}/{run.info.run_id}/artifacts/model/'

        mlflow_client.log_artifact(
            run.info.run_id,
            ensemble.save_model(TMP_MODEL_PATH),
            model_path
        )
        mlflow_client.set_tag(run.info.run_id, "Model path", ensemble.model_path)

        mlflow_client.set_terminated(
            run.info.run_id, RunStatus.to_string(RunStatus.FINISHED)
        )
    except Exception as exc:
        logger.error(exc.with_traceback())
        mlflow_client.set_tag(run.info.run_id, "Error", exc.args)
        mlflow_client.set_terminated(
            run.info.run_id, RunStatus.to_string(RunStatus.FAILED))

    return metrics


s3_client = ClientS3(
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

mlflow_client = MlflowClient(
    tracking_uri=MLFLOW_TRACKING_URI,
    registry_uri=S3_ENDPOINT_URL
)

logger.info(
    f"Loading features {FEATURES_PATH} from"
    f" {BUCKET_NAME} bucket to {TMP_FEATURES_PATH}"
)
s3_client.load_from_s3(
    bucket=BUCKET_NAME,
    remote_path=FEATURES_PATH,
    local_path=TMP_FEATURES_PATH
)

logger.info(
    f"Loading target {TARGET_PATH} from"
    f" {BUCKET_NAME} bucket to {TMP_TARGET_PATH}"
)
s3_client.load_from_s3(
    bucket=BUCKET_NAME,
    remote_path=TARGET_PATH,
    local_path=TMP_TARGET_PATH
)

logger.info(f"Loading features from {TMP_FEATURES_PATH}")
features = read_array(TMP_FEATURES_PATH)

logger.info(f"Loading target from {TMP_TARGET_PATH}")
target = read_array(TMP_TARGET_PATH)

search_space = parse_space_from_file(SEARCH_SPACE_PATH)

search_algorithm = OptunaSearch(
    metric=METRIC_TO_OPTIMIZE,
    mode=METRIC_MODE
)

tune_config = tune.TuneConfig(
    mode=METRIC_MODE,
    metric=METRIC_TO_OPTIMIZE,
    num_samples=NUM_RUNS,
    search_alg=search_algorithm
)
exp_id = mlflow_client.create_experiment(EXPERIMENT_NAME)

tuner = tune.Tuner(
    partial(trainable, mlflow_client=mlflow_client, exp_id=exp_id),
    param_space=search_space,
    tune_config=tune_config,
)

tuner.fit()

