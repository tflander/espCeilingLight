import collections
import ply.yacc as yacc  # this will wrap the generated parser code from test_ply_chem_example.py


def atom_count(s):
    """calculates the total number of atoms in the chemical equation
    >>> atom_count("H2SO4")
    7
    >>>
    """
    count = 0
    for atom in yacc.parse(s):
        count += atom.count
    return count


def element_counts(s):
    """calculates counts for each element in the chemical equation
    >>> element_counts("CH3COOH")["C"]
    2
    >>> element_counts("CH3COOH")["H"]
    4
    >>>
    """

    counts = collections.defaultdict(int)
    for atom in yacc.parse(s):
        counts[atom.symbol] += atom.count
    return counts


def assert_raises(exc, f, *args):
    try:
        f(*args)
    except exc:
        pass
    else:
        raise AssertionError("Expected %r" % (exc,))


def test_element_counts():
    pass
    # assert element_counts("CH3COOH") == {"C": 2, "H": 4, "O": 2}
    # assert element_counts("Ne") == {"Ne": 1}
    # assert element_counts("") == {}
    # assert element_counts("NaCl") == {"Na": 1, "Cl": 1}
    # assert_raises(TypeError, element_counts, "Blah")
    # assert_raises(TypeError, element_counts, "10")
    # assert_raises(TypeError, element_counts, "1C")


def test_atom_count():
    pass
    # assert atom_count("He") == 1
    # assert atom_count("H2") == 2
    # assert atom_count("H2SO4") == 7
    # assert atom_count("CH3COOH") == 8
    # assert atom_count("NaCl") == 2
    # assert atom_count("C60H60") == 120
    # assert_raises(TypeError, atom_count, "SeZYou")
    # assert_raises(TypeError, element_counts, "10")
    # assert_raises(TypeError, element_counts, "1C")

