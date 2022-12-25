import os
from mlbase.utils import read_array, ClientS3
from mlbase.db import DBInterface
from loguru import logger

STATUS = os.environ.get("STATUS")
SCORE_ID = os.environ.get("SCORE_ID")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

COLLECTION = "score"

db = DBInterface(
    db_name=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)

logger.info(f"STATUS: {STATUS}")

status = "Succeeded"
if STATUS != "Succeeded":
    status = "PipelineFailure"

db.update_record(COLLECTION, SCORE_ID, {"status": status})

