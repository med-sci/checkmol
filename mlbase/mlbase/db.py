import pymongo
from pymongo.database import Database
from typing import Dict


class DBInterface:
    def __init__(self, host, port, db_name, user, password):
        self._client = pymongo.MongoClient(
            host=host,
            port=port,
            username=user,
            password=password
        )
        self._db_name = db_name

    @property
    def database(self) -> Database:
        return self._client[self._db_name]

    def add_record(self, collection: str, record: Dict):
        self.database[collection].insert_one(record)

    def update_record(self, collection, score_id, updates: Dict):
        self.database[collection].update_one(
            {"scoreId": score_id},
            {"$set": updates}
        )
    def get_record(self, collection: str, score_id: str):
        return self.database[collection].find_one({"scoreId": score_id})


class ScoreTask:
    COLLECTION_NAME = "score"
    def __init__(self, db: DBInterface):
        self._db = db

    def create_task(self, score_id, smiles, model_path):
        self._db.add_record(
            self.COLLECTION_NAME,
            {
                "score_id": score_id,
                "smiles": smiles,
                "model_path": model_path
            }
        )