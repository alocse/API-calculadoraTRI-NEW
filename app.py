from flask import Flask, request
from main import execute
app = Flask(__name__)

@app.route("/home")
def home():
    return "Flask API get endpoint running"


@app.route("/teste", methods=["GET"])
def get():
    return {"ok": "mundo1"}


@app.route("/calculateTRI", methods=["POST"])
def calculate():
    body = request.get_json()
    return body

if __name__ == "__main__":
    app.run()
