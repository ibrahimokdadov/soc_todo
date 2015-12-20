import uuid

from src.models.folders.folder import Folder
from src.models.tasks.task import Task


class User(object):
    def __init__(self, email, password, name, _id=None):
        self.email = email
        self.password = password
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id

    def add_new_task(self, title, description, due_date, folder_id):
        new_task = Task(title, description, due_date, folder_id, self._id)
        new_task.save_to_mongo()
        # possible alternative:
        # folder = Folder.get_folder_by_id(folder_id)
        # if folder is not None:
        #     folder.add_task(title=title, description=description, due_date=due_date)

    def add_new_folder(self, title, description):
        new_folder = Folder(title=title, description=description, user_id=self._id)
        new_folder.save_to_mongo()
