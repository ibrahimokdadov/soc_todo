from flask import Blueprint, session, render_template, request

from src.models.folders.folder import Folder
from src.models.users.user import User

__author__ = 'team_project_2015'

folder_blueprints = Blueprint('folders', __name__)


@folder_blueprints.route('/user/folders')
def list_folders():
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in")
    else:
        if session['email'] is None:
            return render_template("login.html", message="You must be logged in")
        else:
            user = User.get_user_by_email(session['email'])
            folders = Folder.get_folders_by_user_id(user._id)
            # TODO: If folders is none display no folder exist message else return
            return render_template("list_folders.html", folders=folders)


@folder_blueprints.route('/user/folder/add', methods=['POST', 'GET'])
def add_folder():
    if request.method == 'GET':
        return render_template("add_folder.html")
    else:
        user = User.get_user_by_email(session['email'])
        title = request.form['title']
        description = request.form['description']

        folder = Folder(title=title, description=description, user_id=user._id)
        folder.save_to_mongo()

