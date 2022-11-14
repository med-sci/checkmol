import os
import uuid
import requests

from fastapi import FastAPI
from pydantic import BaseModel

from registry import get_model_path
from fastapi.responses import RedirectResponse

SCORE_EVENT_LISTENER_URL = os.environ.get("SCORE_EVENT_LISTENER_URL")
class ScoreCase(BaseModel):
    smiles: str
    protein: str


app = FastAPI()

score_id = uuid.uuid4().hex

@app.get("/")
async def index():
    return RedirectResponse("/docs")

@app.post(f"/runs/{score_id}")
async def score(score_case: ScoreCase, score_id: str=score_id,):
    model_path = get_model_path(score_case.protein)
    response = requests.post(
        SCORE_EVENT_LISTENER_URL,
        json={
            "smiles": score_case.smiles,
            "scoreId": score_id,
            "modelPath": model_path
        })
    return response