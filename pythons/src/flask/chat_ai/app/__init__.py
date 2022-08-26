from flask import Flask, request

from chat_bert import ai_chatbot


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "챗봇 서버입니다."

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        text_temp = data["text"]
        chat_result = ai_chatbot(text_temp)

        return {"result": chat_result}

    return app
