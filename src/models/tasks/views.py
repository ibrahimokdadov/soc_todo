import datetime
from flask import Blueprint, session, render_template, request, make_response, jsonify

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
            folder = Folder.get_folder_by_id(folder_id)
            if tasks is not None:
                return render_template("tasks/list_tasks.html", folder_id=folder_id, folder_name=folder.title, tasks=tasks)
            else:
                return render_template("tasks/list_tasks.html")
        else:
            tasks = Task.get_tasks_by_folder_id(folder_id)
            folder = Folder.get_folder_by_id(folder_id)
            if tasks is not None:
                return render_template("tasks/list_tasks.html", folder_id=folder_id, folder_name=folder.title, tasks=tasks)
            else:
                return render_template("tasks/list_tasks.html")


@task_blueprints.route('/user/folder/tasks/expired/<string:folder_id>')
def view_expired_tasks(folder_id):
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in")
    else:
        if (session.get('productivity') is not None) and (session['productivity'] == 1):
            tasks = Task.get_previous_tasks(folder_id)
            if tasks is not None:
                return render_template("tasks/list_tasks.html", folder_id=folder_id, tasks=tasks)
            else:
                return render_template("tasks/list_tasks.html")
        else:
            tasks = Task.get_previous_tasks(folder_id)
            if tasks is not None:
                return render_template("tasks/list_tasks.html", folder_id=folder_id, tasks=tasks)
            else:
                return render_template("tasks/list_tasks.html")


@task_blueprints.route('/user/folder/task/add/<string:folder_id>', methods=['POST', 'GET'])
def add_task(folder_id):
    if request.method == 'GET':
        return render_template("tasks/add_task.html", folder_id=folder_id)
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


@task_blueprints.route('/user/task/done/<int:set>')
def mark_done(set):
    if set is 0:
        task_id = request.args.get('task_id')
        task = Task.get_task_by_id(task_id)
        if task is not None:
            if task.mark_as_undone(task_id):
                return jsonify(result=task_id)
            else:
                return jsonify(result=False)
        else:
            return jsonify(result=None)
    elif set is 1:
        task_id = request.args.get('task_id')
        task = Task.get_task_by_id(task_id)
        if task is not None:
            if task.mark_as_done(task_id):
                return jsonify(result=task_id)
            else:
                return jsonify(result=False)
        else:
            return jsonify(result=None)
    else:
        return jsonify(result=None)


@task_blueprints.route('/user/folder/task/detail/<string:task_id>')
def task_detail(task_id):
    task = Task.get_task_by_id(task_id)
    if task is not None:
        return render_template("tasks/task_details.html", task=task)
    else:
        return render_template("tasks/task_details.html", task=task, message="Could not located task")


@task_blueprints.route('/user/folder/task/update/title', methods=['GET', 'POST'])
def update_title():
    task_id = request.form['pk']
    value = request.form['value']
    task = Task.get_task_by_id(task_id)
    task.update_task("title", value)
    return render_template("tasks/task_details.html", task=task)


@task_blueprints.route('/user/folder/task/update/description', methods=['GET', 'POST'])
def update_description():
    task_id = request.form['pk']
    value = request.form['value']
    task = Task.get_task_by_id(task_id)
    task.update_task("description", value)
    return render_template("tasks/task_details.html", task=task)

@task_blueprints.route('/user/folder/task/update/due_date', methods=['GET', 'POST'])
def update_due_date():
    task_id = request.form['pk']
    value = request.form['value']
    task_due_date= datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')
    task = Task.get_task_by_id(task_id)
    task.update_task("due_date", task_due_date)
    return render_template("tasks/task_details.html", task=task)


# test method
@task_blueprints.route('/user/productivity/one')
def productivity_one():
    if session.get('email') is None:
        return render_template('login.html', message="You must be logged in")
    else:
        user = User.get_user_by_email(session['email'])
        folders = Folder.get_folders_by_user_id(user._id)
        tasks_list = []
        if folders is not None:
            for folder in folders:
                tasks_list.append({folder: Task.get_future_three_tasks(folder._id)})
            for list in tasks_list:
                for folder in list:
                    tasks = list[folder]
                    for task in tasks:
                        print("folder {} has task {}, due date {}".format(folder.title, task.title, task.due_date))
