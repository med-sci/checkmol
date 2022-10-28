import os
from loguru import logger
from minio import Minio
from base.utils import (
    drop_duplicates,
    get_dataframe,
    drop_nan,
    calculate_features,
    get_target,
    write_features,
    write_target,
    log_10_target,
    load_from_s3,
    upload_to_s3
)

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

DATA_PATH = os.environ.get("DATA_PATH")
TRIM_DATA = os.environ.get("TRIM_DATA")
TARGET_PATH = os.environ.get("TARGET_PATH")
TARGET_NAME = os.environ.get("TARGET_NAME")
FEATURES_PATH = os.environ.get("FEATURES_PATH")
SMILES_COLUMN_NAME = os.environ.get("SMILES_COLUMN_NAME")
LOG10_TARGET = os.environ.get("LOG10_TARGET")

TMP_TARGET_PATH = os.path.join('/tmp', TARGET_PATH)
TMP_FEATURES_PATH = os.path.join('/tmp', FEATURES_PATH)


client = Minio(
    endpoint=S3_ENDPOINT_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

logger.info(f"Loading data {DATA_PATH} from {BUCKET_NAME}")
csv_path = load_from_s3(
    client=client,
    bucket_name=BUCKET_NAME,
    file_path=DATA_PATH
)

logger.info(f"Loading data from {csv_path}")
dataframe = get_dataframe(csv_path)


if TRIM_DATA:
    logger.info("Removing duplicates")
    dataframe = drop_duplicates(dataframe)

    logger.info("Removing NaN")
    dataframe = drop_nan(dataframe)


logger.info(f"Loading {TARGET_NAME}")
target = get_target(dataframe=dataframe, target=TARGET_NAME)


if LOG10_TARGET:
    logger.info("Converting target values to log10")
    target = log_10_target(target)


logger.info(f"Writing target {TARGET_NAME} to {TMP_TARGET_PATH}")
write_target(target_array=target, path=TMP_TARGET_PATH)

logger.info(
    f"Uploading {TARGET_NAME} from {TMP_TARGET_PATH} to"
     " {TARGET_PATH} in {BUCKET_NAME}")
upload_to_s3(
    client=client,
    bucket_name=BUCKET_NAME,
    bucket_path=TARGET_PATH,
    file_path=TMP_TARGET_PATH
)

logger.info("Calculating descriptors")
features = calculate_features(dataframe=dataframe, smiles_col=SMILES_COLUMN_NAME)

logger.info(f"Writing features to {FEATURES_PATH}")
write_features(features=features, path=FEATURES_PATH)

logger.info(
    f"Uploading features from {TMP_FEATURES_PATH} to"
     " {FEATURES_PATH} in {BUCKET_NAME}")
upload_to_s3(
    client=client,
    bucket_name=BUCKET_NAME,
    bucket_path=FEATURES_PATH,
    file_path=TMP_FEATURES_PATH
)

