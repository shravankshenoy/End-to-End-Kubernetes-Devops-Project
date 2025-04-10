from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
import redis
import json
import os

app = Flask(__name__)

# Redis setup
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
CACHE_TTL = 60

# PostgreSQL setup
db_user = os.getenv('DB_USER', 'user')
db_pass = os.getenv('DB_PASSWORD', 'password')
db_host = os.getenv('DB_HOST', 'postgres')
db_name = os.getenv('DB_NAME', 'appdb')
DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(id=data['id'], name=data['name'], email=data['email'])
    session.merge(user)
    session.commit()
    redis_client.setex(user.id, CACHE_TTL, json.dumps(data))
    return jsonify({'message': 'User created'}), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    cached = redis_client.get(user_id)
    if cached:
        return jsonify(json.loads(cached))
    user = session.get(User, user_id)
    if user:
        user_data = {'id': user.id, 'name': user.name, 'email': user.email}
        redis_client.setex(user.id, CACHE_TTL, json.dumps(user_data))
        return jsonify(user_data)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    # Base.metadata.create_all(engine)

    app.run(host='0.0.0.0', port=5001)