import os
import numpy as np

from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import r2_score
from minio import Minio
from loguru import logger

from mlops_base.utils import load_from_s3, read_array
from mlops_base.model import RandomForest


ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

FEATURES_PATH = os.environ.get("FEATURES_PATH")
TARGET_PATH = os.environ.get("TARGET_PATH")

N_SPLITS = 5
RANDOM_STATE = 42
MODE = 'regression'
TEST_SIZE = 0.2

client = Minio(
    endpoint=S3_ENDPOINT_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

logger.info(f"Loading features {FEATURES_PATH} from {BUCKET_NAME} bucket")
features_path = load_from_s3(client, BUCKET_NAME, FEATURES_PATH)

logger.info(f"Loading target {TARGET_PATH} from {BUCKET_NAME} bucket")
target_path = load_from_s3(client, BUCKET_NAME, TARGET_PATH)

logger.info(f"Loading features from {FEATURES_PATH}")
features = read_array(FEATURES_PATH)

logger.info(f"Loading target from {TARGET_PATH}")
target = read_array(TARGET_PATH)

def trainable(params):
    features_train, features_test, target_train, target_test = train_test_split(
        features, target, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    kfd = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

    models = []
    for fold, (train_index, test_index) in enumerate(kfd.split(features)):
        logger.info(f"Starting training on fold {fold}")

        model = RandomForest(mode=MODE, params=params)
        model.fit(X=features_train[train_index], y=target_train[train_index])

        fold_preds = model.predict(features_train[test_index])
        score = r2_score(y_true=target_train[test_index], y_pred=fold_preds)
        logger.info(f"R2 score for fold {fold}: {score}")

        models.append(model)

    test_preds = np.column_stack([model.predict(features_test) for model in models])
    mean_test_preds = np.mean(test_preds, axis=1)




