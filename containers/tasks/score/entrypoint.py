import os

from loguru import logger
from mlbase.utils import ClientS3, write_array, read_array

from score.utils import load_model


ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")

MODEL_BUCKET_NAME = os.environ.get("MODEL_BUCKET_NAME")
FEATURES_BUCKET_NAME = os.environ.get("FEATURES_BUCKET_NAME")
MODEL_PATH = os.environ.get("MODEL_PATH")
TMP_MODEL_PATH = "/tmp/model.pkl"

FEATURES_PATH = os.environ.get("FEATURES_PATH")
TMP_FEATURES_PATH = os.path.join('/tmp', FEATURES_PATH)

s3_client = ClientS3(
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
logger.info(f"Loading model from {MODEL_PATH} to {TMP_MODEL_PATH} of {MODEL_BUCKET_NAME}")
s3_client.load_from_s3(
    bucket=MODEL_BUCKET_NAME,
    remote_path=MODEL_PATH,
    local_path=TMP_MODEL_PATH
)
logger.info(f"Loading features from {FEATURES_PATH} "
            f"to {TMP_FEATURES_PATH} of {FEATURES_BUCKET_NAME}")
s3_client.load_from_s3(
    bucket=FEATURES_BUCKET_NAME,
    remote_path=FEATURES_PATH,
    local_path=TMP_FEATURES_PATH
)
logger.info(f"Loading features from {TMP_FEATURES_PATH}")
features = read_array(TMP_FEATURES_PATH)

logger.info("Instantiating model..")
model = load_model(TMP_MODEL_PATH)

logger.info(f"Scoring on {TMP_FEATURES_PATH}")
predictions = model.predict(features)

logger.info(f"RESULT: {predictions}")
