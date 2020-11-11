from . import util
import sys
import os


def validate_callback(definition):
    missing_callback = []
    return missing_callback


def validate_resource_arn(definition):
    incorrect_arn = []
    # expression = "$..['Resource']"
    # matched_node = util.get_matching_nodes(expression, definition)
    # for node in matched_node:
    #     resource_arn = node.value
    #     if resource_arn.startswith("arn:aws:"):
    #         target_account = resource_arn.split(":")[4]
    #         if target_account not in []:
    #             incorrect_arn.append(
    #                 {
    #                     "Error code": "INVALID_RESOURCE_ARN",
    #                     "Message": "{} should be at valid ARN in task {}".format(resource_arn, node.full_path)
    #                 }
    #             )
    return incorrect_arn


def validate_custom(definition):
    error_arn = validate_resource_arn(definition)
    error_callback = validate_callback(definition)
    return util.get_combined_errors(error_arn, error_callback)
