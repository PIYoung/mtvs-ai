from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")
        

    @app.route("/chat")
    def chat():
        return {"result": "Hello World!"}

    return app


# terminal: set FLASK_APP={package name}, set FLASK_DEBUG={1 or 0}
