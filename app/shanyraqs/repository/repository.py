from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyraqRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyraq(self, input: dict):
        payload = {
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"],
            "user_id": ObjectId(input["user_id"]),
            "created_at": datetime.utcnow(),
        }

        self.database["shanyraq"].insert_one(payload)

    def get_shanyraq_by_user_id(self, user_id: str) -> List[dict]:
        shanyraqs = self.database["shanyraq"].find(
            {
                "user_id": ObjectId(user_id),
            }
        )
        result = []

        for shanyraq in shanyraqs:
            result.append(shanyraq)

        return result

    def update_shanyraq_by_id(self, id: str, data: dict):
        self.database["shanyraq"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$set": {
                    "type": data["type"],
                    "price": data["price"],
                    "address": data["address"],
                    "area": data["area"],
                    "rooms_count": data["rooms_count"],
                    "description": data["description"],
                }
            },
        )

    def delete_shanyraq_by_id(self, id: str):
        self.database["shanyraq"].delete_one(
            filter={"_id": ObjectId(id)},
        )
