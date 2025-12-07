from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"   # 👈 IMPORTANT: match init.sql
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added", "user_id": new_user.id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
