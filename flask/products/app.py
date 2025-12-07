from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = "products"   # 👈 IMPORTANT
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    new_product = Product(name=data["name"], price=data["price"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added", "product_id": new_product.id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
