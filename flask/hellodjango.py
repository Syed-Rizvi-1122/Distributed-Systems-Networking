from flask import Flask
 
app = Flask(__name__)
 
@app.route("/django")
def hello_world():
    return "<p>Hello, Django!</p>"