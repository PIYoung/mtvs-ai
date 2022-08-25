from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello World!"

    @app.route("/chat")
    def chat():
        return {"result": "Hello World!"}

    return app


# terminal: set FLASK_APP=package name, set FLASK_DEBUG=1 or 0
