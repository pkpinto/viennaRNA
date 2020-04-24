# coding: utf-8


def str_base_pairs(structure):
    """
    Returns the base pairs of a given structure.
    """
    from collections import deque

    open_brackets = deque()
    pairings = set()

    for i, s in enumerate(structure):
        if s == '(':
            open_brackets.append(i)
        elif s == ')':
            pairings.add((open_brackets.pop(), i))

    return pairings


_possible_pairs_of = {'a': {'u'}, 'c': {'g'}, 'g': {'c', 'u'},
                      'u': {'a', 'g'}, 'A': {'U'}, 'C': {'G'},
                      'G': {'C', 'U'}, 'U': {'A', 'G'}}


def seq_str_compatible(sequence, structure):
    """
    Determines if a sequence and structure pais is compatible.
    """
    for pair in str_base_pairs(structure):
        if sequence[pair[0]] not in _possible_pairs_of[sequence[pair[1]]]:
            return False
    return True
