# https://tomassetti.me/parsing-in-python/
import re


def test_variable_assignment():
    script_runner = ScriptRunner()
    script = [
        "let y = add(2, 1)",
        "show y"
    ]

    for line in script:
        parts = line.split()
        if parts[0] == 'let':
            print("variable assignment", parts)

            let_pattern = r"^let\s+(.*)=(.*)$"
            p = re.compile(let_pattern)
            m = p.match(line)
            print(m)
            if m is None:
                print('invalid syntax', line, 'for', let_pattern)
            script_var = m.group(1).strip()
            rhs = m.group(2).strip()

            script_runner.let(script_var, rhs)
            print(script_runner.script_vars)
            continue
        if parts[0] == 'show':
            script_runner.show(parts[1])
            continue
        print('syntax error', line)


class ScriptRunner:

    def __init__(self):
        self.script_vars = {}

    def let(self, k, v):
        self.script_vars[k] = eval(v)

    def show(self, script_var):
        print(self.script_vars[script_var])


def add(v1, v2):
    return v1 + v2
