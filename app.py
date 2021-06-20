
from flask import Flask, request

from main import execute

app = Flask("alocse")

@app.route("/teste", methods=["GET"])
def get():
    return {"ok": "mundo1"}

@app.route("/home")
def home():
    return "Flask API get endpoint running"

app.run()
