import os
import uuid
import requests

from fastapi import FastAPI
from pydantic import BaseModel

from registry import get_model_path
from fastapi.responses import RedirectResponse

from mlbase.utils import ClientS3

SCORE_EVENT_LISTENER_URL = os.environ.get("SCORE_EVENT_LISTENER_URL")
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")

RESULTS_BUCKET = "score"

class ScoreCase(BaseModel):
    smiles: str
    protein: str


app = FastAPI()

score_id = uuid.uuid4().hex

@app.get("/")
async def index():
    return RedirectResponse("/docs")

@app.post(f"/runs/{score_id}")
async def score(score_case: ScoreCase, score_id: str=score_id):
    model_path = get_model_path(score_case.protein)
    response = requests.post(
        SCORE_EVENT_LISTENER_URL,
        json={
            "smiles": score_case.smiles,
            "scoreId": score_id,
            "modelPath": model_path
        })
    return response.json()


@app.get("/runs/")
async def get_results(score_id: str):
    s3_client = ClientS3(
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    return s3_client.get_object(
        bucket=RESULTS_BUCKET,
        path=os.path.join(score_id, 'response.json')
    )
