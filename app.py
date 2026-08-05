from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]

questions = [
    {
        "q": "Q1. What does a STOP sign mean?\nA. Slow down\nB. Stop completely\nC. Speed up\nD. Turn left",
        "a": "B"
    },
    {
        "q": "Q2. Before changing lanes you should:\nA. Honk\nB. Accelerate\nC. Check mirrors and blind spot\nD. Brake hard",
        "a": "C"
    }
]

user_progress = {}

@app.route("/")
def home():
    return "ShokoDrivingInstructor Bot is running!"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

def send_message(to, text):
    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }

    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    try:
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"].strip().upper()

        if text == "START":
            user_progress[sender] = 0
            send_message(sender, "Welcome to Shoko Driving Instructor Provisional Test.\n\nReply with A, B, C or D.\n\n" + questions[0]["q"])
            return "OK", 200

        if sender in user_progress:
            i = user_progress[sender]

            if text == questions[i]["a"]:
                send_message(sender, "✅ Correct!")
            else:
                send_message(sender, f"❌ Wrong. Correct answer: {questions[i]['a']}")

            i += 1

            if i < len(questions):
                user_progress[sender] = i
                send_message(sender, questions[i]["q"])
            else:
                send_message(sender, "🎉 Test Finished!")
                del user_progress[sender]

    except Exception as e:
        print(e)

    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run()
