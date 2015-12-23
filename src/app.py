from flask import Flask, render_template, session

from src.common.database import Database
from src.models.folders.views import folder_blueprints
from src.models.tasks.views import task_blueprint

__author__ = 'team_project_2015'

app = Flask(__name__)
app.secret_key = 'team-project-2015'

app.register_blueprint(folder_blueprints)
app.register_blueprint(task_blueprint)


@app.before_first_request
def initialize_db():
    Database.initialize()


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/logout')
def logout():
    session['email'] = None
    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=4555, debug=True)
