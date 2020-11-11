import os
import json
from jsonschema import Draft7Validator, RefResolver, ValidationError


def validate_schema(definition):
    schema_path = os.path.dirname(os.path.abspath(__file__))+'/schemas'
    with open(os.path.join(schema_path, 'state-machine.json')) as fp:
        schema = json.load(fp)
    schema_path_uri = 'file:///{0}/'.format(schema_path.replace("\\", '/'))
    custom_resolver = RefResolver(base_uri=schema_path_uri, referrer=schema)
    validator = Draft7Validator(schema, resolver=custom_resolver)
    error_schema = []
    try:
        validator.validate(definition)
    except ValidationError as err:
        pointer = " --> ".join(err.relative_path)
        error_schema = [
                {
                    'Error code': 'INVALID_SCHEMA',
                    "Message": "{} at {}".format(err.message, pointer)
                }
            ]
    except Exception as err:
        error_schema = [
                {
                    'Error code': 'INVALID_SCHEMA',
                    "Message": "Could not validate {}".format(err)
                }
            ]
    return error_schema
