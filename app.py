from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Shoko Provisional Test Bot is running!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "Webhook verified!"
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
