from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = "orders"   # 👈 IMPORTANT
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

@app.route("/orders", methods=["POST"])
def add_order():
    data = request.json
    new_order = Order(
        user_id=data["user_id"],
        product_id=data["product_id"],
        quantity=data["quantity"],
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed", "order_id": new_order.id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
