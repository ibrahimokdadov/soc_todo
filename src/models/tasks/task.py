import uuid

import datetime

from src.common.database import Database
import src.models.tasks.constants as TaskConstants


class Task(object):
    def __init__(self, title, description, due_date, folder_id, user_id, is_done=False, _id=None, date_created=datetime.datetime.utcnow()):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.folder_id = folder_id
        self.user_id = user_id
        self.is_done = is_done
        self._id = uuid.uuid4().hex if _id is None else _id
        self.date_created=date_created

    @staticmethod
    def mark_as_done(task_id):
        result = Database.update_one(TaskConstants.COLLECTION, {"_id": task_id}, {"is_done": True})
        if result.matched_count == 1:
            return True

    @staticmethod
    def mark_as_undone(task_id):
        result = Database.update_one(TaskConstants.COLLECTION, {"_id": task_id}, {"is_done": False})
        if result.matched_count == 1:
            return True

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
            '_id': self._id,
            'date_created': self.date_created
        }
        return data

    @classmethod
    def get_task_by_id(cls, task_id):
        task_data = Database.find_one(collection=TaskConstants.COLLECTION, query={'_id': task_id})
        if task_data is not None:
            return cls(**task_data)

    @classmethod
    def get_tasks_by_folder_id(cls, folder_id):
        tasks = Database.find(collection=TaskConstants.COLLECTION, query={'folder_id': folder_id})
        if tasks is not None:
            return [cls(**task) for task in tasks]

    @staticmethod
    def get_tasks_count(folder_id):
        tasks = Database.find_count(TaskConstants.COLLECTION, {"folder_id": folder_id, "is_done": False})
        return tasks

    @classmethod
    def get_future_three_tasks(cls, folder_id):
        # tasks = Database.find_limit(TaskConstants.COLLECTION, {"folder_id": folder_id, "due_date": {
        #     "$lt": datetime.datetime.today().strftime("%d/%M/%Y %H:%M")}})
        # date= "new ISODate('{}')".format(datetime.datetime.utcnow().isoformat())
        tasks = Database.find_limit(TaskConstants.COLLECTION, {"folder_id": folder_id, "is_done": False, "due_date": {
            "$gt": datetime.datetime.utcnow()}})
        if tasks is not None:
            return [cls(**task) for task in tasks]

    @classmethod
    def get_previous_tasks(cls, folder_id):
        # option to return just count
        tasks = Database.find(TaskConstants.COLLECTION, {"folder_id": folder_id, "is_done": False, "due_date": {
            "$lt": datetime.datetime.utcnow()}})
        if tasks is not None:
            return [cls(**task) for task in tasks]

    @classmethod
    def get_previous_tasks_count(cls, folder_id):
        # option to return just count
        tasks = Database.find_count(TaskConstants.COLLECTION, {"folder_id": folder_id, "is_done": False, "due_date": {
            "$lt": datetime.datetime.utcnow()}})
        return tasks

    @classmethod
    def get_three_tasks(cls, user_id):
        tasks = Database.find_limit(TaskConstants.COLLECTION, {"user_id": user_id, "is_done": False, "due_date": {
            "$gt": datetime.datetime.utcnow()}})
        if tasks is not None:
            return [cls(**task) for task in tasks]

    def update_task(self, attribute_name, attribute_value):
        Database.update_one(TaskConstants.COLLECTION, {"_id": self._id}, {attribute_name: attribute_value})
