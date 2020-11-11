from jsonpath_ng import parse
from . import util


def get_all_states(definition):
    machine_states = []
    expression = "$..['States']"
    matched_node = util.get_matching_nodes(expression, definition)
    for node in matched_node:
        machine_states.extend(node.value.keys())
    return machine_states


def get_all_reachable_states(definition):
    reachable_states = []
    jsonpath_expr = parse("$..['StartAt','Next','Default']")
    found_states = [match.value for match in jsonpath_expr.find(definition)]
    for i, match in enumerate(found_states):
        if type(match) == str:
            if i == found_states.index(match):
                reachable_states.append(match)
    return reachable_states


def get_unreachable_states(machine_states, reachable_states):
    unreachable_states = [
            {
                "Error code": "MISSING_STATE_INCOMING",
                "Message": "State {} is not reachable".format(state)
            }
            for state in machine_states if state not in reachable_states
            ]
    return unreachable_states


def get_undefined_states(machine_states, reachable_states):
    undefined_states = [
            {
                "Error code": "MISSING_STATE_DEFINITION",
                "Message": "Missing target {} not defined".format(state)
            }
            for state in reachable_states if state not in machine_states
        ]
    return undefined_states


def get_duplicate_states(all_states):
    duplicate_states = []
    set_Of_states = set()
    for state in all_states:
        if state in set_Of_states:
            duplicate_states.append({"Error code": "DUPLICATE_STATE_DEFINITION", "Message": "State {} is defined more than once".format(state)})
        else:
            set_Of_states.add(state)
    return duplicate_states


def validate_terminal_node_existance(definition):
    error_terminal_node = []
    jsonpath_expr = parse("$..['States']")
    for match in jsonpath_expr.find(definition):
        for state_name, state_def in match.value.items():
            if state_def['Type'] in ['Succeed', 'Fail']:
                continue
            elif state_def.get("End", False) is True:
                continue
            else:
                error_terminal_node.append(
                        {
                            'Error code': 'NO_END_STATE',
                            "Message": "Definition {} must contain one Succeed|Fail|End state".format(state_name)
                        }
                )


def validate_parallel_node_links(definition):
    error_links = []
    jsonpath_expr = parse("$..['Branches']")
    for match in jsonpath_expr.find(definition):
        braches = match.value
        for branch in braches:
            links = {k: v.get("Next") for k, v in branch.get("States").items()}
            valid_next_target = set(links.keys())
            for sname, next_target in links.items():
                if next_target and (next_target not in valid_next_target):
                    error_links.append(
                            {
                                'Error code': 'INVALID_DEF',
                                "Message": "Incorrect next step in {} must be from these {}".format(sname, valid_next_target)
                            }
                        )
    return error_links


def validate_state(definition):
    machine_states = get_all_states(definition)
    error_invalid_links = validate_parallel_node_links(definition)
    duplicate_states = get_duplicate_states(machine_states)
    reachable_states = get_all_reachable_states(definition)
    unreachable_states = get_unreachable_states(
        machine_states,
        reachable_states
        )
    undefined_states = get_undefined_states(machine_states, reachable_states)
    error_terminal_node = validate_terminal_node_existance(definition)
    error_state = util.get_combined_errors(
        unreachable_states,
        undefined_states,
        duplicate_states,
        error_terminal_node,
        error_invalid_links
        )
    return error_state
