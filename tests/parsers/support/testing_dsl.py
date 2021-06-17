from parsers.parser_constants import ExpressionValueTypes
from parsers.result_objects import ParseFailure


def flatten(result):
    if type(result) is ParseFailure:
        print("ParseFailure " + str(result.message))
        return result
    if result.value is not None:
        return result.value, result.result_type

    return result.match, result.result_type


def is_assignment(result, left, right):
    if flatten(result.left) != (left, ExpressionValueTypes.VARIABLE):
        print("expected left = " + left + ", found " + result.left.match)
        return False

    if result.right.result_type == ExpressionValueTypes.OPERATION:
        if right != result.rest:
            print("expected right = " + right + ", found " + result.rest)
            return False

    elif flatten(result.right) != (right, ExpressionValueTypes.INT):
        print("expected right = " + right + ", found " + result.right.match)
        return False

    return True


def that(result):
    return ResultTester(result)


class ResultTester:

    def __init__(self, result):
        self.result = result

    def is_assignment(self, left, right):
        return is_assignment(self.result, left, right)
