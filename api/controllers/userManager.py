import os
from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required)
from api import app, mongo, flask_bcrypt, jwt, JSONEncoder
from ..schemas import validate_empUser, generate_random, validate_datetime


userManager = Blueprint('userManager', __name__, url_prefix='/userManager')


@userManager.route('/', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@jwt_required
def userManagement():
    if request.method == 'GET':
        try:
            users = []
            data = mongo.db.empUsers.find({}, {'name':1, 'lname':1, 'email':1, '_id':0})
            for user in data:
                users.append(user)
            return jsonify(users), 200
        except Exception as e:
            return jsonify({'ok': False, 'Message' : 'Server error' + e.message}), 500

    if request.method == 'POST':
        try:
            data = validate_empUser(request.get_json())
            
        
            if data['ok']:
                data = data['data']
                if validate_datetime(data['createdAt']) and validate_datetime(data['birthdate']):
                    return jsonify({'ok': False, 'msg': 'Invalid date format'}), 400
                else: 
                    user = mongo.db.empUsers.find_one({'email': data['email']}, {"_id": 0})
                    if user: 
                        return jsonify({'ok': False, 'msg': 'This email is already in use.'}), 409
                    else:
                        generated = generate_random()
                        data['password'] = generated
                        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
                        mongo.db.empUsers.insert_one(data)
                        return jsonify({'ok': True, 'msg': 'User created successfully!','generated': generated }), 200
            else:
                return jsonify({'ok': False, 'msg': 'Bad request parameters: {}' .format(data['message'])}), 400     
        except Exception as e:
            return jsonify({'ok': False, 'msg' : 'Server error' + str(e)}), 500  

    if request.method == 'PATCH':
        try:
            data = validate_empUser(request.get_json())

            if not data['ok']:
                return jsonify({'ok': False, 'msg': 'Bad request parameters: {}' .format(data['message'])}), 400  
            else:
                data = data['data']
                if not 'email' in data:
                     return jsonify({'ok': False, 'Message' : 'Please provide an email address'}), 400
                else:        
                    user = mongo.db.empUsers.find_one({'email': data['email']}, {"password": 0})
                    if not user:
                        return jsonify({'ok': False, 'Message' : 'not user found.'}), 404
                    else:
                        data['_id'] = user['_id']
                        user = data
                        mongo.db.empUsers.save(user)
                        return jsonify({'ok': True, 'msg': 'User updated successfully!'}), 200 

        except Exception as e:
            return jsonify({'ok': False, 'Message' : 'Failed to update user' + str(e)}), 500
    
    if request.method == 'DELETE': 
        try:
            data = request.get_json()
            if not data:
                return jsonify({'ok': False, 'Message' : 'please provide user data'}), 400
            else:
                if 'email' in data:
                    user = mongo.db.empUsers.find_one({'email': data['email']}, {'password':0, '_id':0})
                    if not user:
                        return jsonify({'ok': False, 'Message' : 'not user found.'}), 404
                    else:
                        mongo.db.empUsers.remove(user)
                        return jsonify({'ok': True, 'msg': 'User deleted successfully!'}), 200 
                else:        
                    return jsonify({'ok': False, 'Message' : 'Please provide an email address'}), 400

        except Exception as e:
            return jsonify({'ok': False, 'Message' : 'Failed to delete user' + str(e)}), 500 