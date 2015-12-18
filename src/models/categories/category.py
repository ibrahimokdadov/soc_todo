import uuid
import src.models.categories.constants as CategoryConstants
from src.common.database import Database

__author__ = 'team_project_2015'


class Category(object):
    def __init__(self, title, description, user_id, _id=None):
        self.title = title
        self.description = description
        self.user_id = user_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(CategoryConstants.COLLECTION, self.json())

    @classmethod
    def get_categories_by_user_id(cls, user_id):
        categories = Database.find(CategoryConstants, {"user_id": user_id})
        if categories is not None:
            return [cls(**category) for category in categories]
