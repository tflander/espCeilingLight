class CombineResult:

    def __init__(self, token, match, result_type):
        self.result_type = result_type
        self.token = token
        self.match = match
        self.value = None


class ParseResult(CombineResult):

    def __init__(self, token, match, result_type):
        CombineResult.__init__(self, token, match, result_type)
        self.rest = token[len(match):]


class CombineFailure:

    def __init__(self, errored_token):
        self.errored_token = errored_token


class ParseFailure(CombineFailure):

    def __init__(self, errored_token, text, line=None):
        CombineFailure.__init__(self, errored_token)
        pos = text.index(errored_token) + 1
        message_main = "Syntax Error"
        if line is not None:
            message_main += ", line " + str(line)
        if pos >= 1:
            self.message = [
                message_main,
                "  " + text,
                "  " + (" " * pos) + "^"
            ]


def show_message(failure):
    for line in failure.message:
        print(line)
