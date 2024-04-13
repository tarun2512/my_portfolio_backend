from typing import Dict, List, Optional

from scripts.constants import UserCollectionKeys
from scripts.constants.app_constants import Collections, Database
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_utility import MongoCollectionBaseClass


class MyResumeSchema(MongoBaseSchema):
    last_updated_at: Optional[int]
    pdf_data: Optional[str]
    last_fetched_date: Optional[str]
    last_fetched_by: Optional[str]
    resume_name: Optional[str]


class MyResume(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(mongo_client, database=Database.login, collection=Collections.myresume)

    @property
    def key_username(self):
        return UserCollectionKeys.KEY_USERNAME

    def get_all_users(self, filter_dict=None, sort=None, skip=0, limit=None, **query):
        if users := self.find(
                filter_dict=filter_dict, sort=sort, skip=skip, limit=limit, query=query
        ):
            return list(users)
        return []

    def save_resume(self, resume_name, data):
        query = {"resume_name": resume_name}
        self.update_one(query=query, data=data, upsert=True)

    def get_resume(self):
        if records := self.find({}, sort={"last_updated_at": -1}):
            return records[0]
        return {}

    def update_resume(self, resume_data):
        query = {"resume_name": resume_data.get("resume_name")}
        self.update_one(query=query, data=resume_data)


