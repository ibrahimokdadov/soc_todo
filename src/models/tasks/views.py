import datetime
from flask import Blueprint, session, render_template, request, make_response

from src.models.folders.folder import Folder
from src.models.tasks.task import Task
from src.models.users.user import User

__author__ = 'team_project_2015'

task_blueprints = Blueprint('tasks', __name__)


@task_blueprints.route('/user/folder/tasks/<string:folder_id>')
def view_tasks(folder_id):
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in")
    else:
        if (session.get('productivity') is not None) and (session['productivity'] == 1):
            tasks = Task.get_future_three_tasks(folder_id)
            #TODO: display passed undone tasks
            if tasks is not None:
                return render_template("list_tasks.html", folder_id=folder_id, tasks=tasks)
            else:
                return render_template("list_tasks.html")
        else:
            tasks = Task.get_tasks_by_folder_id(folder_id)
            if tasks is not None:
                return render_template("list_tasks.html", folder_id=folder_id, tasks=tasks)
            else:
                return render_template("list_tasks.html")


@task_blueprints.route('/user/folder/task/add/<string:folder_id>', methods=['POST', 'GET'])
def add_task(folder_id):
    if request.method == 'GET':
        return render_template("add_task.html", folder_id=folder_id)
    else:
        folder = Folder.get_folder_by_id(folder_id)
        if folder is not None:
            task_title = request.form['title']
            task_description = request.form['description']
            task_due_date = request.form['due_date']
            task_due_date = datetime.datetime.strptime(task_due_date, '%d/%m/%Y %H:%M')
            task_due_date.isoformat()
            folder.add_task(title=task_title, description=task_description, due_date=task_due_date)
            return make_response(view_tasks(folder_id))

#test method
@task_blueprints.route('/user/productivity/one')
def productivity_one():
    if session.get('email') is None:
        return render_template('login.html', message="You must be logged in")
    else:
        user = User.get_user_by_email(session['email'])
        folders = Folder.get_folders_by_user_id(user._id)
        tasks_list=[]
        if folders is not None:
            for folder in folders:
                tasks_list.append({folder: Task.get_future_three_tasks(folder._id)})
            for list in tasks_list:
                for folder in list:
                    tasks = list[folder]
                    for task in tasks:
                        print("folder {} has task {}, due date {}".format(folder.title, task.title, task.due_date))
