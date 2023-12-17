from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo.database import Database


class AdsRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_ad(self, input: dict):
        payload = {
            "title": input["title"],
            "type": input["type"],            
            "description": input["description"],
            "user_id": ObjectId(input["user_id"]),
            "category": input["category"],
            "media": [],
            "comment": [],
            "created_at": datetime.utcnow(),
        }

        self.database["ads"].insert_one(payload)

    def get_ad_by_user_id(self, user_id: str) -> List[dict]:
        ads = self.database["ads"].find(
            {
                "user_id": ObjectId(user_id),
            }
        )
        result = []

        for ad in ads:
            result.append(ad)

        return result

    def get_ad_id(self, id: str):
        result = self.database["ads"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        return result

    def update_shanyraq_by_id(self, id: str, data: dict):
        self.database["ads"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$set": {
                    "title": input["title"],
                    "description": input["description"],
                    "category": input["category"],
                }
            },
        )

    def delete_ad_by_id(self, id: str):
        self.database["ads"].delete_one(
            filter={"_id": ObjectId(id)},
        )

    def add_ads_media(self, id: str, url: str):
        sh = self.database["ads"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if sh is None:
            return None
        result = self.database["ads"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "media": url,
                }
            },
        )
        return result

    def delete_ads_media(self, id: str, url: str):
        sh = self.database["ads"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if sh is None:
            return None
        result = self.database["ads"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$pull": {
                    "media": url,
                }
            },
        )
        return result

    def create_ads_comment(self, user_id: str, id: str, comment: str):
        sh = self.database["ads"].find_one(
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
        result = self.database["ads"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "comment": payload,
                }
            },
        )
        return result

    def get_ads_comments(self, id: str):
        sh = self.database["ads"].find_one(
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
        shanyrak = self.database["ads"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        if shanyrak["comments"] is None:
            return None

        result = self.database["ads"].update_one(
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
        sh = self.database["ads"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if sh is None:
            return None

        if sh["comment"] is None:
            return None

        result = self.database["ads"].update_one(
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
    
    def get_posts(
        self,
        limit,
        offset,
        type,
        category,

    ):
        query = {
            "$and": [
                ({"type": type}) if type != None else {},
                ({"category": category}) if category != None else {},
            ]
        }
        total_count = self.database["ads"].count_documents(query)

        cursor = (
            self.database["ads"]
            .find(query)
            .sort("created_at")
            .skip(offset)
            .limit(limit)
        )

        result = []
        for item in cursor:
            result.append(item)

        return {"total": total_count, "ads": result}
