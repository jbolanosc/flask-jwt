import os
from flask import request, jsonify, Blueprint
from flask_jwt_extended import (create_access_token, create_refresh_token,get_raw_jwt,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required)
from api import app, mongo, flask_bcrypt, jwt

from ..schemas import validate_empUser
from ..util import send_password_reset_email


user = Blueprint('user', __name__, url_prefix='/user')

blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
}), 401


@user.route('/login', methods=['POST', 'GET'])
def login():
    data = request.get_json()

    if not data['email']:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not data['password']:
        return jsonify({"msg": "Missing password parameter"}), 400

    try:    

        user = mongo.db.empUsers.find_one({'email': data['email']}, {"_id": 0})



        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            ret = {
                'access_token': create_access_token(identity=data['email'], fresh=True),
                'refresh_token': create_refresh_token(identity=data['email'])
            }
            return jsonify(ret), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    
    except Exception as e:
        return jsonify({'ok': False, 'Message' : 'Failed to login' + e.message}), 500




@user.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    ret = {'access_token': new_token}
    return jsonify(ret), 200



@user.route('/protected-fresh', methods=['GET'])
@jwt_required
def protected_fresh():
    username = get_jwt_identity()
    return jsonify(fresh_logged_in_as=username), 200



@user.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    try:   
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return jsonify({"msg": "Successfully logged out"}), 200
    except Exception as e:
        return jsonify({'ok': False, 'Message' : 'Failed to logout' + e.message}), 500


 