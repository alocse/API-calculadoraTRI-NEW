import Flask
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
    teste = execute(body)
    return teste

if __name__ == "__main__":
    app.run()
