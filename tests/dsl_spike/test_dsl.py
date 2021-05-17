# https://tomassetti.me/parsing-in-python/
   # TODO: maybe Pyleri & PEG parsers

import re


def test_simple_variable_assignments():
    script_runner = ScriptRunner()
    script = [
        "let y = add(2, 1)",
        "let x = 3 + 1",
        "show y"
    ]

    script_runner.run(script)
    assert script_runner.script_vars == {'y': 3, 'x': 4}


# TODO:  Investigate lexical analyzers / parse generators
def skip_test_variable_reference_in_assignment():
    script_runner = ScriptRunner()
    script = [
        "let y = 3",
        "let x = y + 1",
        "let z = x+1"
    ]

    script_runner.run(script)
    assert script_runner.script_vars == {'y': 3, 'x': 4, 'z': 5}


class ScriptRunner:

    def __init__(self):
        self.script_vars = {}

    def run(self, script):
        for line in script:
            parts = line.split()
            if parts[0] == 'let':
                let_pattern = r"^let\s+(.*)=(.*)$"
                p = re.compile(let_pattern)
                m = p.match(line)
                if m is None:
                    print('invalid syntax', line, 'for', let_pattern)
                script_var = m.group(1).strip()
                rhs = m.group(2).strip()

                self.let(script_var, rhs)
                continue
            if parts[0] == 'show':
                self.show(parts[1])
                continue
            print('syntax error', line)

    def let(self, k, v):
        # TODO: resolve script variables in v
        print(v)
        self.script_vars[k] = eval(v)

    def show(self, script_var):
        print(self.script_vars[script_var])


def add(v1, v2):
    return v1 + v2
