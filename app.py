from flask import Flask, request
from main import execute
app = Flask(__name__)

@app.route("/home")
def home():
    return "Bem vindo a calculadora TRI"


@app.route("/calculateTRI", methods=["POST"])
def calculate():
    body = request.get_json()
    
    try:  
        tri = execute(body) 
    except Exception as e: 
        return {"error": str(e)}
    
    return tri
    
if __name__ == "__main__":
    app.run()
