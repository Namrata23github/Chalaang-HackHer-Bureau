from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
from db import mongo

user_bp = Blueprint('user', __name__)
@user_bp.route('/api/users/register', methods=['POST'])
def registerUser():
    # Extract data from the request body
    data = request.get_json()

    # Validate the data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required parameter'}), 400

    # Check if the username or email already exists
    existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create the new user
    user = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.utcnow()
    }
    result = mongo.db.users.insert_one(user)

    # Return the new user's id, username, email, and created_at
    return jsonify({
        'id': str(result.inserted_id),
        'username': username,
        'email': email,
        'created_at': user['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    }), 200


