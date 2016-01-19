from flask import Flask, render_template, url_for, session, request, make_response

from src.common.database import Database
from src.models.tasks.views import task_blueprints
from src.models.users.user import User
from src.models.folders.views import folder_blueprints, list_folders

__author__ = 'team_project_2015'

app = Flask(__name__)
app.secret_key = 'team-project-2015'

app.register_blueprint(folder_blueprints)
app.register_blueprint(task_blueprints)


@app.before_first_request
def initialize_db():
    Database.initialize()


@app.route('/')
def index():
    session['email']='ibrahim@ibrahim.com'
    return render_template("home.html")


@app.route('/register')
def register_template():
    return render_template("register.html")


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['username_email']
    password = request.form['password']
    name = request.form['username_name']
    if User.register(email, password, name) is True:
        return make_response(list_folders())
    else:
        return render_template("register.html", message="User with the same email exist. Try another email")


@app.route('/logout')
def logout():
    session['email'] = None
    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=4555, debug=True)
