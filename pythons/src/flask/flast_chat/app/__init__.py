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

    @app.route("/set-user")
    def set_user():
        data = models.UserInfo(name="홍길동")
        db.session.add(data)
        db.session.commit()
        return "ok"

    @app.route("/get-user")
    def get_user():
        data = models.UserInfo.query.get(1)
        return str(data.name)

    @app.route("/chat")
    def chat():
        return {"result": "Hello World!"}

    return app
