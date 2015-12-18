import uuid

from src.models.tasks.task import Task


class User(object):
    def __init__(self, email, password, name, _id=None):
        self.email = email
        self.password = password
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id

    def add_new_task(self, title, description, due_date, folder):
        new_task = Task(title, description, due_date, folder, self._id)
        new_task.save_to_mongo()
