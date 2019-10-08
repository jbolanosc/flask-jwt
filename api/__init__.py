import os
import datetime
import json
from flask import Flask
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



config_object = os.environ.get('CONFIGURE')

    
app = Flask(__name__)
app.config.from_object(config_object)
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)

mongo = PyMongo(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)


from .controllers.user import user
app.register_blueprint(user)
from .controllers.userManager import userManager
app.register_blueprint(userManager)
