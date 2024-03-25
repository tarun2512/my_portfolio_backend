from typing import Dict, List, Optional

from scripts.constants import UserCollectionKeys
from scripts.constants.app_constants import Collections, Database
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_utility import MongoCollectionBaseClass


class VisitorsSchema(MongoBaseSchema):
    visitor_name: Optional[str]
    visitor_ip: Optional[str]
    last_viewed_date: Optional[str]


class Visitors(MongoCollectionBaseClass):
    def __init__(self, mongo_client, project_id=None):
        super().__init__(mongo_client, database=Database.login, collection=Collections.visitors)
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

    def save_user(self, visitor_name, data):
        query = {"visitor_name": visitor_name}
        if user := self.update_one(query=query, data=data, upsert=True):
            return dict(user)
        else:
            return user
