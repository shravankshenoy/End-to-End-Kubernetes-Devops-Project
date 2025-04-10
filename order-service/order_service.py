from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import os

app = Flask(__name__)

db_user = os.getenv('DB_USER', 'user')
db_pass = os.getenv('DB_PASSWORD', 'password')
db_host = os.getenv('DB_HOST', 'postgres')
db_name = os.getenv('DB_NAME', 'appdb')
DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(String, primary_key=True)
    item = Column(String)
    quantity = Column(Integer)
    user_id = Column(String)

@app.route('/orders', methods=['GET'])
def homepage():
    return jsonify({'message': 'Welcome to order service'})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(id=data['id'], item=data['item'], quantity=data['quantity'], user_id=data['user_id'])
    session.merge(order)
    session.commit()
    return jsonify({'message': 'Order created'}), 201

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = session.get(Order, order_id)
    if order:
        return jsonify({'id': order.id, 'item': order.item, 'quantity': order.quantity, 'user_id': order.user_id})
    return jsonify({'error': 'Order not found'}), 404

if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5002)