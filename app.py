import flask
app = flask.Flask(__name__)

@app.route("/home")
def home():
    return "teste api alocse"

if __name__ == "__main__":
    app.run()

    
