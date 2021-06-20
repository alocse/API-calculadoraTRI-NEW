import flask
import request
app = flask.Flask(__name__)

@app.route("/home")
def home():
    return "Flask API get endpoint running"


@app.route("/teste", methods=["GET"])
def get():
    return {"ok": "mundo1"}


@app.route("/calculateTRI", methods=["POST"])
def calculate():
    
    body = request.get_json()
    #print(body)
    
    return body

if __name__ == "__main__":
    app.run()
