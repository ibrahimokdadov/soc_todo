__author__ = 'team_project_2015'


class FolderErrors(Exception):
    def __init__(self, message):
        self.message = message


class FolderNotExistError(FolderErrors):
    pass

