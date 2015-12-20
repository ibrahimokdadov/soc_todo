import uuid

from src.common.database import Database
from src.models.folders import constants


class Task(object):
    def __init__(self, title, description, due_date, folder_id, user_id, _id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.folder_id = folder_id
        self.user_id = user_id
        self.is_done = False
        self._id = uuid.uuid4().hex if _id is None else _id

    def mark_as_done(self):
        self.is_done = True

    def save_to_mongo(self):
        Database.insert(collection=constants.TASKS_COLLECTION,
                        data=self.json())

    def json(self):
        data = {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'folder': self.folder_id,
            'user_id': self.user_id,
            'is_done': self.is_done,
            '_id': self._id
        }
        return data

    @classmethod
    def get_task_by_id(cls, task_id):
        task_data = Database.find_one(collection=constants.TASKS_COLLECTION, query={'_id': task_id})
        return cls(**task_data)
