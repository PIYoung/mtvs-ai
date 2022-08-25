import config

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/chat")
    def chat():
        return {"result": "Hello World!"}

    return app
