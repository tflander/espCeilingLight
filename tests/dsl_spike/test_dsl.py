
def test_eval():
    x = 1
    script = [
        "print(x)",
        "print(add(x, 1))"
    ]

    for line in script:
        eval(line)


script_vars = {}


def test_variable_assignment():
    global script_vars
    script = [
        "let y = add(x, 1)",
        "show y"
    ]

    for line in script:
        parts = line.split()
        if parts[0] == 'let':
            print("variable assignment")
            script_vars['y'] = eval('add(3, 1)')
            print(script_vars)
            continue
        if parts[0] == 'show':
            show(parts[1])
            continue
        eval(line)


def add(v1, v2):
    return v1 + v2


def show(script_var):
    global script_vars
    print(script_vars[script_var])