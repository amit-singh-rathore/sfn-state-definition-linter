from jsonpath_ng import parse
from . import util

def validate_states_all(definition):
    error_states_all = []
    jsonpath_expr = parse("$..['Retry', 'Catch']")
    for match in jsonpath_expr.find(definition):
        error_equals = match.value
        idx_for_sall = len(error_equals)-1
        for idx, ee in enumerate(error_equals):
            ee_list = ee.get("ErrorEquals", [])
            if "States.ALL" in ee_list and idx != idx_for_sall:
                error_states_all.append(
                        {
                            'Error code': 'INVALID_DEF',
                            "Message": "State.ALL should be at last in {}".format(match.full_path)
                        }
                    )
            if not ee_list:
                error_states_all.append(
                        {
                            'Error code': 'INVALID_DEF',
                            "Message": "ErrorEquals field can't be empty in {}".format(match.full_path)
                        }
                    )
    return error_states_all


def validate_error_retry(definition):
    error_states_all = validate_states_all(definition)
    error = util.get_combined_errors(error_states_all, [])
    return error
