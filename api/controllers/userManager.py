import os
from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required)
from api import app, mongo, flask_bcrypt, jwt, JSONEncoder
from ..schemas import validate_empUser


userManager = Blueprint('userManager', __name__, url_prefix='/userManager')


@userManager.route('/', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@jwt_required
def userManagement():
    if request.method == 'GET':
        users = []
        data = mongo.db.empUsers.find({}, {'name':1, 'lname':1, '_id':0})
        for user in data:
                print(user)
                users.append(user)
        print(users[0])
        return jsonify(users), 200

@userManager.route('/createUser', methods=['POST'])
@jwt_required
def register():
    data = validate_empUser(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(
            data['password'])
        mongo.db.empUsers.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400