
import string, random, datetime
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

empUser_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "lname": {
            "type": "string",
        },
        "birthdate": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        },
        "empType":{
            "type":"string",
        },
        "createdAt":{
            "type":"string"
        },
        "status": {
            "type": "string",
        }
    },
    "required": ["email", "name", "lname", "birthdate", "empType","createdAt", "status"],
    "additionalProperties": False
}


def validate_empUser(data):
    try:
        validate(data, empUser_schema)
    except ValidationError as e:
        return {'ok': False, 'message': 'All fields are required'}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

def validate_datetime(date_text):
    try:
        return True
    except ValueError:
        return False


def generate_random():
    number = random.randrange (1,999)
    letters = string.ascii_lowercase
    generated = ''.join(random.choice(letters) for i in range(stringLength))
    generated += str(number)
    return generated


    