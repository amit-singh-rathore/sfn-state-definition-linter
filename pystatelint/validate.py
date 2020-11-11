"""   
This project is inspired from the below projects.
https://github.com/awslabs/statelint
https://github.com/airware/asl-validator

"""

from cfripper.pystatelint import schema
from cfripper.pystatelint import state
from cfripper.pystatelint import path
from cfripper.pystatelint import custom
from cfripper.pystatelint import error_retry
from cfripper.pystatelint import util

def validate(sfdefinition):
    schema_errors = schema.validate_schema(sfdefinition)
    state_errors = state.validate_state(sfdefinition)
    path_errors = path.validate_path(sfdefinition)
    erro_retry_errors = error_retry.validate_error_retry(sfdefinition)
    custom_errors = custom.validate_custom(sfdefinition)
    errors = util.get_combined_errors(schema_errors, state_errors, path_errors, erro_retry_errors, custom_errors)
    return errors

