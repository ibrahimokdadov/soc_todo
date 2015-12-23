from flask import Blueprint, session, render_template

from src.models.tasks.task import Task
from src.models.users.user import User

task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/tasks')
def list_tasks():
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in")
    else:
        user = User.get_user_by_email(session['email'])
        tasks = Task.get_tasks_by_user_id(user._id)
        return render_template("list_tasks.html", tasks=tasks)


@task_blueprint.route('/task/<string:task_id>')
def task_page(task_id):
    task = Task.get_task_by_id(task_id)
    return render_template("task.html", task=task)
