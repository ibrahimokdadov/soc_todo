import uuid

import datetime

from src.common.database import Database
import src.models.tasks.constants as TaskConstants


class Task(object):
    def __init__(self, title, description, due_date, folder_id, user_id, is_done=False, _id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.folder_id = folder_id
        self.user_id = user_id
        self.is_done = is_done
        self._id = uuid.uuid4().hex if _id is None else _id

    def mark_as_done(self):
        self.is_done = True

    def save_to_mongo(self):
        Database.insert(collection=TaskConstants.COLLECTION,
                        data=self.json())

    def json(self):
        data = {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'folder_id': self.folder_id,
            'user_id': self.user_id,
            'is_done': self.is_done,
            '_id': self._id
        }
        return data

    @classmethod
    def get_task_by_id(cls, task_id):
        task_data = Database.find_limit(collection=TaskConstants.COLLECTION, query={'_id': task_id})
        return cls(**task_data)

    @classmethod
    def get_tasks_by_folder_id(cls, folder_id):
        tasks = Database.find(collection=TaskConstants.COLLECTION, query={'folder_id': folder_id})
        if tasks is not None:
            return [cls(**task) for task in tasks]

    @staticmethod
    def get_tasks_count(folder_id):
        tasks = Database.find_count(TaskConstants.COLLECTION, {"folder_id": folder_id})
        return tasks

    @classmethod
    def get_future_three_tasks(cls, folder_id):
        # tasks = Database.find_limit(TaskConstants.COLLECTION, {"folder_id": folder_id, "due_date": {
        #     "$lt": datetime.datetime.today().strftime("%d/%M/%Y %H:%M")}})
        #date= "new ISODate('{}')".format(datetime.datetime.utcnow().isoformat())
        tasks = Database.find_limit(TaskConstants.COLLECTION, {"folder_id": folder_id, "due_date": {
            "$gt": datetime.datetime.utcnow()}})
        if tasks is not None:
            return [cls(**task) for task in tasks]

    @classmethod
    def get_previous_tasks(cls, folder_id):
        #option to return just count
        tasks = Database.find(TaskConstants.COLLECTION, {"folder_id": folder_id, "due_date": {
            "$lt": datetime.datetime.utcnow()}})
        if tasks is not None:
            return [cls(**task) for task in tasks]
