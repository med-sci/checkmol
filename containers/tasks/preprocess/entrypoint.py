import os
import pandas as pd
import numpy as np
import uuid
import tempfile

from typing import Literal, List
from loguru import logger
from mlbase.utils import write_array, ClientS3, write_task_result
from mlbase.db import DBInterface
from preprocess.utils import (
    drop_duplicates,
    get_dataframe,
    drop_nan,
    calculate_features,
    get_target,
    log_10_target
)

TASK: Literal["Train", "Score"] = os.environ.get("TASK")

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")

RESULT_BUCKET_NAME = os.environ.get("RESULT_BUCKET_NAME")
FEATURES_PATH_RESULT_PATH = os.environ.get("FEATURES_PATH_RESULT_PATH")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

COLLECTION = "score"

db = DBInterface(
    db_name=DB_NAME,
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_USER,
    password=DB_PASSWORD
)

logger.info(f"Instantiating client..")
s3_client = ClientS3(
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

if TASK == "Train":
    TARGET_PATH_RESULT_PATH = os.environ.get("TARGET_PATH_RESULT_PATH")
    EXPERIMENT_NAME_RESULT_PATH = os.environ.get("EXPERIMENT_NAME_RESULT_PATH")

    DATA_BUCKET_NAME = os.environ.get("DATA_BUCKET_NAME")

    PROTEIN_NAME = os.environ.get("PROTEIN_NAME")

    DATA_PATH = os.environ.get("DATA_PATH")
    TRIM_DATA = os.environ.get("TRIM_DATA")
    TARGET_NAME = os.environ.get("TARGET_NAME")

    SMILES_COLUMN_NAME = os.environ.get("SMILES_COLUMN_NAME")
    LOG10_TARGET = os.environ.get("LOG10_TARGET")

    EXPERIMENT_CONDITION = os.environ.get("EXPERIMENT_CONDITION")
    EXPERIMENT_NAME = f"{PROTEIN_NAME}_{TARGET_NAME}_" \
        f"{EXPERIMENT_CONDITION}_{uuid.uuid4().hex}"

    TARGET_PATH = os.path.join(EXPERIMENT_NAME, "target/target.pkl")
    TMP_DATA_PATH = os.path.join('/tmp', DATA_PATH)
    TMP_TARGET_PATH = os.path.join('/tmp', TARGET_PATH)
    FEATURES_PATH = os.path.join(EXPERIMENT_NAME, "features/features.pkl")
    TMP_FEATURES_PATH = os.path.join('/tmp', FEATURES_PATH)

    logger.info(
        f"Loading data {DATA_PATH} from"
        f"{DATA_BUCKET_NAME} bucket to {TMP_DATA_PATH}"
    )
    s3_client.load_from_s3(
        bucket=DATA_BUCKET_NAME,
        remote_path=DATA_PATH,
        local_path=TMP_DATA_PATH
    )

    logger.info(f"Loading data from {TMP_DATA_PATH}")
    dataframe = get_dataframe(TMP_DATA_PATH)

    if TRIM_DATA == 'True':
        logger.info(f"Removing duplicates. Initial shape: {dataframe.shape}")
        dataframe = drop_duplicates(dataframe)
        logger.info(f"Final shape: {dataframe.shape}")

        logger.info(f"Removing NaN initial shape: {dataframe.shape}")
        dataframe = drop_nan(dataframe)
        logger.info(f"Final shape: {dataframe.shape}")


    logger.info(f"Loading {TARGET_NAME}")
    target = get_target(dataframe=dataframe, target=TARGET_NAME)


    if LOG10_TARGET == 'True':
        logger.info("Converting target values to log10")
        target = log_10_target(target)


    logger.info(f"Writing target {TARGET_NAME} to {TMP_TARGET_PATH}")
    write_array(array=target, path=TMP_TARGET_PATH)

    logger.info(
        f"Uploading {TARGET_NAME} from {TMP_TARGET_PATH} to"
        f" {TARGET_PATH} in {RESULT_BUCKET_NAME}")
    s3_client.upload_to_s3(
        bucket=RESULT_BUCKET_NAME,
        remote_path=TARGET_PATH,
        local_path=TMP_TARGET_PATH
    )
    logger.info("Calculating features")
    features = calculate_features(dataframe=dataframe, smiles_col=SMILES_COLUMN_NAME)

    logger.info(f"Writing features to {TMP_FEATURES_PATH}")
    write_array(array=features, path=TMP_FEATURES_PATH)

    logger.info(
        f"Uploading features from {TMP_FEATURES_PATH} to"
        f" {FEATURES_PATH} in {RESULT_BUCKET_NAME} bucket")
    s3_client.upload_to_s3(
        bucket=RESULT_BUCKET_NAME,
        remote_path=FEATURES_PATH,
        local_path=TMP_FEATURES_PATH
    )

    # emitting results
    logger.info(f"Writing {FEATURES_PATH} to {FEATURES_PATH_RESULT_PATH}")
    write_task_result(FEATURES_PATH, FEATURES_PATH_RESULT_PATH)

    logger.info(f"Writing {TARGET_PATH} to {TARGET_PATH_RESULT_PATH}")
    write_task_result(TARGET_PATH, TARGET_PATH_RESULT_PATH)

    logger.info(f"Writing {EXPERIMENT_NAME} to {EXPERIMENT_NAME_RESULT_PATH}")
    write_task_result(EXPERIMENT_NAME, EXPERIMENT_NAME_RESULT_PATH)

elif TASK == "Score":
    SCORE_ID = os.environ.get("SCORE_ID")

    SMILES_COLUMN_NAME = "smiles"
    FEATURES_PATH = os.path.join(SCORE_ID, "features/features.pkl")

    smiles = db.get_record(COLLECTION, SCORE_ID)["smiles"]
    dataframe = pd.DataFrame({SMILES_COLUMN_NAME: smiles})

    logger.info("Calculating features")
    features = calculate_features(dataframe=dataframe, smiles_col=SMILES_COLUMN_NAME)
    features = np.nan_to_num(features)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_features_path = os.path.join(tmpdir, FEATURES_PATH)

        logger.info(f"Writing features to {tmp_features_path}")
        write_array(array=features, path=tmp_features_path)

        logger.info(
            f"Uploading features from {tmp_features_path} to"
            f" {FEATURES_PATH} in {RESULT_BUCKET_NAME} bucket")
        s3_client.upload_to_s3(
            bucket=RESULT_BUCKET_NAME,
            remote_path=FEATURES_PATH,
            local_path=tmp_features_path
        )

    db.update_record(
        COLLECTION,
        SCORE_ID,
        {
            "featuresPath": FEATURES_PATH
        }
    )

