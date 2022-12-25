import os
import tempfile
from loguru import logger
from mlbase.utils import ClientS3, read_array
from mlbase.db import DBInterface
from score.utils import load_model


ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

MODEL_BUCKET_NAME = os.environ.get("MODEL_BUCKET_NAME")
FEATURES_BUCKET_NAME = os.environ.get("FEATURES_BUCKET_NAME")
SCORE_ID = os.environ.get("SCORE_ID")

COLLECTION = "score"

db = DBInterface(
    db_name=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)

MODEL_PATH = db.get_record(COLLECTION, SCORE_ID)["modelPath"]
FEATURES_PATH = db.get_record(COLLECTION, SCORE_ID)["featuresPath"]

s3_client = ClientS3(
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_model_path = os.path.join(tmpdir, "model.pkl")
    tmp_features_path = os.path.join(tmpdir, "features.pkl")

    logger.info(f"Loading model from {MODEL_PATH} to {tmp_model_path} of {MODEL_BUCKET_NAME}")
    s3_client.load_from_s3(
        bucket=MODEL_BUCKET_NAME,
        remote_path=MODEL_PATH,
        local_path=tmp_model_path
    )
    logger.info(f"Loading features from {FEATURES_PATH} "
                f"to {tmp_features_path} of {FEATURES_BUCKET_NAME}")
    s3_client.load_from_s3(
        bucket=FEATURES_BUCKET_NAME,
        remote_path=FEATURES_PATH,
        local_path=tmp_features_path
    )
    logger.info(f"Loading features from {tmp_features_path}")
    features = read_array(tmp_features_path)

    logger.info("Instantiating model..")
    model = load_model(tmp_model_path)

    logger.info(f"Scoring on {tmp_model_path}")
    predictions = model.predict(features)

    smiles = db.get_record(COLLECTION, SCORE_ID)["smiles"]
    results = {smiles: value for smiles, value in zip(smiles, predictions)}
    db.update_record(COLLECTION, SCORE_ID, {"results": results})