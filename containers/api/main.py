import os
import requests

from fastapi import FastAPI
from pydantic import BaseModel

from registry import get_model_path
from fastapi.responses import RedirectResponse

from mlbase.utils import ClientS3
from mlbase.db import DBInterface

SCORE_EVENT_LISTENER_URL = os.environ.get("SCORE_EVENT_LISTENER_URL")
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

RESULTS_BUCKET = "score"
COLLECTION = "score"

print(DB_NAME)
db = DBInterface(
    db_name=DB_NAME,
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_USER,
    password=DB_PASSWORD
)
class ScoreCase(BaseModel):
    smiles: str
    protein: str


app = FastAPI()

@app.get("/")
async def index():
    return RedirectResponse("/docs")

@app.post("/runs/{score_id}")
async def score(score_case: ScoreCase, score_id: int):
    model_path = get_model_path(score_case.protein)
    db.add_record(COLLECTION,
        {
            "smiles": score_case.smiles,
            "scoreId": score_id,
            "modelPath": model_path
        }
    )
    response = requests.post(
        SCORE_EVENT_LISTENER_URL,
        json={
            "scoreId": score_id,
        })
    return response.status_code


@app.get("/runs/")
async def get_results(score_id: str):
    return db.get_record(collection=COLLECTION, score_id=score_id)
