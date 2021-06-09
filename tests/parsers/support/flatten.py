def flatten(result):
    if result.value is not None:
        return result.value, result.result_type

    return result.match, result.result_type
