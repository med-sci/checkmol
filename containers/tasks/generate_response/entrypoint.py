import os
import json
from mlbase.utils import read_array, ClientS3
from loguru import logger

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")

STATUS = os.environ.get("STATUS")
RESULTS_PATH = os.environ.get("RESULTS_PATH")
SMILES_PATH = os.environ.get("SMILES_PATH")
RESULT_BUCKET_NAME = os.environ.get("RESULT_BUCKET_NAME")
SCORE_ID = os.environ.get("SCORE_ID")

TMP_RESULTS_PATH = "/tmp/results.pkl"
TMP_SMILES_PATH = "/tmp/smiles.pkl"
TMP_RESPONSE_PATH = "/tmp/response.json"


s3_client = ClientS3(
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

logger.info(f"STATUS: {STATUS}")
response = {"Error": None}


if STATUS == "Succeeded":
    logger.info(f"loading {SMILES_PATH} to {TMP_SMILES_PATH}")
    s3_client.load_from_s3(
        bucket=RESULT_BUCKET_NAME,
        remote_path=SMILES_PATH,
        local_path=TMP_SMILES_PATH
    )
    logger.info(f"loading {RESULTS_PATH} to {TMP_RESULTS_PATH}")
    s3_client.load_from_s3(
        bucket=RESULT_BUCKET_NAME,
        remote_path=RESULTS_PATH,
        local_path=TMP_RESULTS_PATH
    )
    predictions = read_array(TMP_RESULTS_PATH)
    smiles = read_array(TMP_SMILES_PATH)
    response.update({key: value for key, value in zip(smiles, predictions)})
elif STATUS == "Failed":
    response["Error"] = "PipelineFailure"
else:
    response["Error"] = "UnknownError"


logger.info(f"Response: {response}")
with open (TMP_RESPONSE_PATH, "wt") as file:
    json.dump(response, file)


ClientS3.upload_to_s3(
    RESULT_BUCKET_NAME,
    os.path.join(SCORE_ID, "response.json"),
    TMP_RESPONSE_PATH
)

