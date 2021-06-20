
import Flask

app = Flask("alocse")


@app.route("/home")
def home():
    return "Flask API get endpoint running"

app.run()
