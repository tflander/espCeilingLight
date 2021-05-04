def test_variable_assignment():
    script_runner = ScriptRunner()
    script = [
        "let y = add(2, 1)",
        "show y"
    ]

    for line in script:
        parts = line.split()
        if parts[0] == 'let':
            print("variable assignment")

            script_runner.let('y', script_runner.add(3, 1))

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
        self.script_vars[k] = v

    def add(self, v1, v2):
        return v1 + v2

    def show(self, script_var):
        print(self.script_vars[script_var])

