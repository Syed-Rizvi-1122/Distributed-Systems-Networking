from flask import Flask
 
app = Flask(__name__)
 
@app.route("/kivy")
def hello_world():
    return "<p>Hello, Kivy!</p>"