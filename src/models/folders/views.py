import collections
from flask import Blueprint, session, render_template, request, make_response

from src.models.folders.folder import Folder
from src.models.tasks.task import Task
from src.models.users.user import User

__author__ = 'team_project_2015'

folder_blueprints = Blueprint('folders', __name__)


@folder_blueprints.route('/user/folders')
def list_folders(message=None):
    # TODO: list ascending
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in")
    else:
        if (session.get('productivity') is not None) and (session['productivity'] == 1):
            user = User.get_user_by_email(session['email'])
            folders = Folder.get_folders_by_user_id(user._id)
            tasks_list = {}
            # TODO: display passed undone tasks
            if folders is not None:
                for folder in folders:
                    tasks_list[folder] = len(Task.get_future_three_tasks(folder._id))
                return render_template("folders/list_folders.html", folders=tasks_list)
        elif (session.get('productivity') is not None) and (session['productivity'] == 2):
            user = User.get_user_by_email(session['email'])
            tasks = Task.get_three_tasks(user._id)
            return render_template("tasks/list_level_two_tasks.html", tasks=tasks)
        else:
            user = User.get_user_by_email(session['email'])
            folders = Folder.get_folders_by_user_id(user._id)
            folder_tasks_count = {}
            for folder in folders:
                tasks = Task.get_tasks_count(folder._id)
                folder_tasks_count[folder] = tasks
            if message is None:
                return render_template("folders/list_folders.html", folders=folder_tasks_count)
            else:
                return render_template("folders/list_folders.html", folders=folder_tasks_count, message=message)


@folder_blueprints.route('/user/folder/add', methods=['POST', 'GET'])
def add_folder():
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in")
    else:
        if request.method == 'GET':
            return render_template("folders/add_folder.html")
        else:
            user = User.get_user_by_email(session['email'])
            if user is not None:
                title = request.form['title']
                folder = Folder.get_folder_by_title(title, user._id)
                if folder is None:
                    description = request.form['description']
                    folder = Folder(title=title, description=description, user_id=user._id)
                    folder.save_to_mongo()
                    return make_response(list_folders())
                else:
                    return render_template("folders/add_folder.html",
                                           message="Folder with the same name exist. Choose another name")
            else:
                return render_template("login.html", message="You must be logged in to add folders")


@folder_blueprints.route('/user/folder/delete/<string:folder_id>')
def delete_item(folder_id):
    if session.get('email') is not None:
        folder = Folder.get_folder_by_id(folder_id)
        if folder is not None:
            user = User.get_user_by_email(session['email'])
            if folder.user_id == user._id:
                folder.remove_item()
                return make_response(list_folders())
        return make_response(list_folders("Folder could not be located"))
    else:
        return render_template("login.html", message="You must be logged-in to remove items.")


@folder_blueprints.route('/user/folder/update/title', methods=['GET', 'POST'])
def update_title():
    # TODO: fix the update not to make response because it is not used.
    folder_id = request.form['pk']
    value = request.form['value']
    folder = Folder.get_folder_by_id(folder_id)
    folder.update_folder("title", value)
    return make_response(list_folders(message="Folder title updated successfully"))


@folder_blueprints.route('/user/folder/update/description', methods=['GET', 'POST'])
def update_description():
    folder_id = request.form['pk']
    value = request.form['value']
    folder = Folder.get_folder_by_id(folder_id)
    folder.update_folder("description", value)
    return make_response(list_folders(message="Folder description updated successfully"))


@folder_blueprints.route('/user/productivity/level1')
def productivity_level_one():
    session['productivity'] = 1
    return make_response(list_folders())


@folder_blueprints.route('/user/productivity/level1/off')
def productivity_level_one_off():
    session['productivity'] = None
    return make_response(list_folders())


@folder_blueprints.route('/user/productivity/level2')
def productivity_level_two():
    session['productivity'] = 2
    return make_response(list_folders())


@folder_blueprints.route('/user/productivity/level2/off')
def productivity_level_two_off():
    session['productivity'] = None
    return make_response(list_folders())
