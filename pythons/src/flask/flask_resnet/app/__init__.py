from flask import Flask, request
from PIL import Image

from app import ai_img


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        class_name = ai_img.ai_image("app/test.jpg")
        return {"result": class_name}

    @app.route("/face-class", methods=["POST"])
    def face_class():
        file = request.files["file"]
        class_name = ai_img.ai_image(file.stream)
        return {"result": class_name}


    return app
