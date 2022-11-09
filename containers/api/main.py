from typing import Literal, List

from fastapi import FastAPI
from pydantic import BaseModel


class ScoreCase(BaseModel):
    target: str
    mode: Literal['regression'] = 'regression'
    smiles: List[str]
    model: str


app = FastAPI()

@app.post("/items/{score_id}")
async def score(score_id: int, score_case: ScoreCase):
    return {"score_id": score_id, **score_case.dict()}