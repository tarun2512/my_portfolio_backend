from typing import Dict, List, Optional

from scripts.constants import UserCollectionKeys
from scripts.constants.app_constants import Collections, Database
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_utility import MongoCollectionBaseClass


class UserSchema(MongoBaseSchema):
    user_name: Optional[str]
    password: Optional[str]


class User(MongoCollectionBaseClass):
    def __init__(self, mongo_client, project_id=None):
        super().__init__(mongo_client, database=Database.login, collection=Collections.user)
        self.project_id = project_id

    @property
    def key_username(self):
        return UserCollectionKeys.KEY_USERNAME

    def get_all_users(self, filter_dict=None, sort=None, skip=0, limit=None, **query):
        if users := self.find(
            filter_dict=filter_dict, sort=sort, skip=skip, limit=limit, query=query
        ):
            return list(users)
        return []

    def find_user(self, user_name):
        if user := self.find_one(query={"user_name": user_name}):
            return dict(user)
        else:
            return user
