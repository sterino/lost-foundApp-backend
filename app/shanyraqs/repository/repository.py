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
            "media": [],
            "comment": [],
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

    def get_shanyraq_id(self, id: str):
        result = self.database["shanyraq"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
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

    def add_shanyraq_media(self, id: str, url: str):
        sh = self.database["shanyraq"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if sh is None:
            return None
        result = self.database["shanyraq"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "media": url,
                }
            },
        )
        return result

    def delete_shanyraq_media(self, id: str, url: str):
        sh = self.database["shanyraq"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if sh is None:
            return None
        result = self.database["shanyraq"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$pull": {
                    "media": url,
                }
            },
        )
        return result

    def create_shanyraq_comment(self, user_id: str, id: str, comment: str):
        sh = self.database["shanyraq"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if sh is None:
            return None
        payload = {
            "id": ObjectId(),
            "content": comment,
            "person_id": ObjectId(user_id),
            "created_at": datetime.utcnow(),
        }
        result = self.database["shanyraq"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "comment": payload,
                }
            },
        )
        return result

    def get_shanyraq_comments(self, id: str):
        sh = self.database["shanyraq"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if sh is None:
            return None
        if sh["comment"] is None:
            return None

        return sh["comment"]

    def delete_comment(self, id: str, comment_id: str, user_id: str):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        if shanyrak["comments"] is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$pull": {
                    "comments": {
                        "id": ObjectId(comment_id),
                        "author_id": ObjectId(user_id),
                    },
                }
            },
        )

        return result

    def update_comment(self, id: str, comment_id: str, user_id: str, content: str):
        sh = self.database["shanyraq"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if sh is None:
            return None

        if sh["comment"] is None:
            return None

        result = self.database["shanyraq"].update_one(
            filter={
                "_id": ObjectId(id),
                "comment.id": ObjectId(comment_id),
                "comment.author_id": ObjectId(user_id),
            },
            update={
                "$set": {
                    "comment.$.content": content,
                }
            },
        )

        return result
