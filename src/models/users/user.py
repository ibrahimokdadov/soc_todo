import uuid

from flask import session

from src.common.database import Database
from src.models.folders.folder import Folder
from src.models.tasks.task import Task
import src.models.users.constants as UserConstants


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

    @classmethod
    def get_user_by_email(cls, email):
        user = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user is not None:
            return cls(**user)

    @classmethod
    def register(cls, email, password, name):
        user = cls.get_user_by_email(email)
        if user is None:
            new_user = cls(email, password, name)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @classmethod
    def login(cls, email, password):
        user = cls.get_user_by_email(email)
        if user is not None:
            if user.password == password:
                session['email'] = email
                return True
            return False
        else:
            return False

    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(UserConstants.COLLECTION, self.json())
