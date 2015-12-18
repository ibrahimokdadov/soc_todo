import uuid

from src.common.database import Database


class Task(object):
    def __init__(self, title, description, due_date, category, _id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.is_done = False
        self._id = uuid.uuid4().hex if _id is None else _id

    def mark_as_done(self):
        self.is_done = True

    def save_to_mongo(self):
        Database.insert(collection='tasks',
                        data=self.json())

    def json(self):
        data = {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'category': self.category,
            'is_done': self.is_done,
            '_id': self._id
        }
        return data

    @classmethod
    def from_mongo(cls, task_id):
        task_data = Database.find_one(collection='tasks', query={'_id': task_id})
        return cls(**task_data)
