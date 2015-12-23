import uuid
import src.models.folders.constants as FolderConstants
from src.common.database import Database
import src.models.folders.errors as FolderErrors
from src.models.tasks.task import Task

__author__ = 'team_project_2015'


class Folder(object):
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
        Database.insert(FolderConstants.COLLECTION, self.json())

    @classmethod
    def get_folders_by_user_id(cls, user_id):
        folders = Database.find(FolderConstants.COLLECTION, {"user_id": user_id})
        if folders is not None:
            return [cls(**folder) for folder in folders]
        else:
            raise FolderErrors.FolderNotExistError("No Folders exist")

    @classmethod
    def get_folder_by_id(cls, folder_id):
        folder = Database.find_one(FolderConstants.COLLECTION, {"_id": folder_id})
        if folder is not None:
            return cls(**folder)
        else:
            raise FolderErrors.FolderNotExistError("Folder does not exist")

    def add_task(self, title, description, due_date):
        task = Task(title=title, description=description, due_date=due_date, folder_id=self._id, user_id=self.user_id)
        task.save_to_mongo()
