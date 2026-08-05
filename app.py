from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "ShokoDrivingInstructor-bot"

@app.route("/")
def home():
    return "Shoko Provisional Test Bot is running!"

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    return "EVENT_RECEIVED", 200
