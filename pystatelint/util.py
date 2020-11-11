from jsonpath_ng import parse


def get_combined_errors(*args):
    error = []
    for item in args:
        if item:
            error.extend(item)
    return error


def get_matching_nodes(parse_exp, definition):
    jsonpath_expr = parse(parse_exp)
    matched = [MatchNode(match) for match in jsonpath_expr.find(definition)]
    return matched


class MatchNode():
    def __init__(self, match):
        self.value = match.value
        self.context = match.context
        self.full_path = match.full_path
