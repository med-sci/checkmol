import os
import requests

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from registry import get_model_path, get_scaler_path
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from rdkit import Chem
from mlbase.db import DBInterface


SCORE_EVENT_LISTENER_URL = os.environ.get("SCORE_EVENT_LISTENER_URL")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

COLLECTION = "score"

db = DBInterface(
    db_name=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)
class ScoreCase(BaseModel):
    Constant: str
    Mode: str
    Protein: str
    Task: str
    id: str
    smiles: List

class ValidateRequest(BaseModel):
    smiles: list


app = FastAPI()

origins = [
    'http://lupuslucis.fvds.ru',
    'http://lupuslucis.fvds.ru:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return RedirectResponse("/docs")

@app.post("/runs/{score_id}")
async def score(score_case: ScoreCase, score_id: str):
    if validate_smiles(smiles=score_case.smiles):

        model_path = get_model_path(score_case.Protein)
        scaler_path = get_scaler_path(score_case.Protein)

        db.add_record(COLLECTION,
            {
                "smiles": score_case.smiles,
                "scoreId": score_id,
                "modelPath": model_path,
                "Constant": score_case.Constant,
                "Protein": score_case.Protein,
                "Task": score_case.Task,
                "scalerPath": scaler_path
            }
        )
        response = requests.post(
            SCORE_EVENT_LISTENER_URL,
            json={
                "scoreId": score_id,
            })
        if response.status_code == 200:
            return {"status": "Ok"}
        return {"status": "Error"}
    return {"status": "ValidationError"}


@app.get("/runs/{score_id}")
async def get_results(score_id: str):
    record = db.get_record(collection=COLLECTION, score_id=score_id)
    record.pop("_id")
    return record


def validate_smiles(smiles):
    mols = [Chem.MolFromSmiles(s) for s in smiles]
    if None in mols:
        return False
    return True
