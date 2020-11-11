from jsonpath_ng import parse
from . import util


def validate_regular_path(definition):
    incorrect_paths = []
    jsonpath_expr = parse("$..['InputPath','OutputPath','ResultPath']")
    for match in jsonpath_expr.find(definition):
        if type(match.value) == str:
            path_to_check = match.value
            try:
                if path_to_check.startswith("$$"):
                    path_to_check = path_to_check.replace("$", "", 1)
                    parse(path_to_check)
                else:
                    parse(match.value)
            except Exception as err:
                incorrect_paths.append(
                    {
                        "Error code": "INCORRECT_PATH",
                        "Message": "{} is not a valid path".format(match.value)
                    }
                )
        else:
            incorrect_paths.append(
                {
                    "Error code": "INCORRECT_PATH",
                    "Message": "{} is Invalid path, must be string".format(match.value)
                }
            )
    return incorrect_paths if incorrect_paths else None


def check_invalid(value):
    try:
        if value.startswith("$$"):
            path_to_check = value.replace("$", "", 1)
            parse(path_to_check)
        else:
            parse(value)
    except Exception as err:
        return True
    return False


def get_all_path_params(dictionary):
    for key, value in dictionary.items():
        if type(value) == dict and not(key.endswith(".$")):
            yield from get_all_path_params(value)
        else:
            yield (key, value)


def validate_parameters_path(definition):
    jsonpath_expr = parse("$..['Parameters']")
    error_params = []
    for match in jsonpath_expr.find(definition):
        for key, value in get_all_path_params(match.value):
            if key.endswith(".$"):
                if type(value) == str:
                    if check_invalid(value):
                        error_params.append(
                                {
                                    "Error code": "INCORRECT_PATH_PARAM",
                                    "Message": "{} is Invalid path".format(value)
                                }
                            )
                else:
                    error_params.append(
                        {
                            "Error code": "INCORRECT_PATH_PARAM",
                            "Message": " {} is not a valid path, it must be a string".format(value)
                        }
                    )
    return error_params


def validate_path(definition):
    error_regular_path = validate_regular_path(definition)
    error_param_path = validate_parameters_path(definition)
    return util.get_combined_errors(error_regular_path, error_param_path)
