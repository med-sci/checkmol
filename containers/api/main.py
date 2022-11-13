import uuid
from typing import Literal, List

from fastapi import FastAPI
from pydantic import BaseModel

from registry import get_model_path


class ScoreCase(BaseModel):
    smiles: str
    protein: str


app = FastAPI()

score_id = uuid.uuid4().hex

@app.post(f"/items/{score_id}")
async def score( score_case: ScoreCase, score_id: str=score_id,):
    model_path = get_model_path(score_case.protein)
    return {
        "score_id": score_id,
        "model_path": model_path,
         **score_case.dict()
    }