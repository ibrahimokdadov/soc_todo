class TaskErrors(Exception):
    def __init__(self, message):
        self.message = message


class TaskNotExistError(TaskErrors):
    pass
