import json
from jsonschema import validate, ValidationError

schema_detail = {
    "type" : "object",
    "properties" : {
        "detail" : {"type" : "string"}
    },
    "required" : ["detail"],
    "additionalProperties": False
}

#json = '{"user":{"type_code":"c","status":"cf"}}'
schema_valid_client = {
    "type" : "object",
    "properties" : {
        "user" : {
            "type" : "object",
            "properties" : {
                "type_code" : "c",
                "status" : ["rg", "cf", "bn"]
            },
            "required" : ["type_code", "status"],
            "additionalProperties": False
        }
    },
    "required" : ["user"],
    "additionalProperties": False
}

#{"user":{"type_code":"m","status":"cf","master":{"id":6,"status":"uv"}}}
schema_valid_master = {
    "type" : "object",
    "properties" : {
        "user" : {
            "type" : "object",
            "properties" : {
                "type_code" : "m",
                "status" : ["rg", "cf", "bn"],
                "master" : {
                    "type" : "object",
                    "properties" : {
                        "id" : {"type" : "integer", "minimum" : 0},
                        "status" : ["vr", "uv", "bn"]
                    },
                    "required" : ["id", "status"],
                    "additionalProperties" : False
                }
            },
            "required" : ["type_code", "status", "master"],
            "additionalProperties": False
        }
    },
    "required" : ["user"],
    "additionalProperties": False
}

def validate_error(self, json_str, error_message):
    is_validate = validate(json_str, self.schema_detail)
    if is_validate:
        json_loaded = json.loads(json_str)
        return json_loaded['detail'] == error_message

def validate_users_get_valid_client(self, json_str):
    return validate(json_str, self.schema_valid_client)

def validate_users_get_valid_master(self, json_str):
    return validate(json_str, self.schema_valid_master)

def validate(self, json_str, json_schema):
    json_loaded = json.loads(json_str)
    try:
        validate(json_loaded, json_schema)
        return True
    except ValidationError:
        return False