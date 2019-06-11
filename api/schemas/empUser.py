
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
    "required": ["email", "password", "name", "lname", "birthdate", "empType","createdAt", "status"],
    "additionalProperties": False
}


def validate_empUser(data):
    try:
        validate(data, empUser_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}