from flask import Flask, render_template

from src.common.database import Database

__author__ = 'team_project_2015'

app = Flask(__name__)
app.secret_key = 'team-project-2015'

from src.models.folders.views import folder_blueprints
app.register_blueprint(folder_blueprints)


@app.before_first_request
def initialize_db():
    Database.initialize()


@app.route('/')
def index():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(port=4555, debug=True)
