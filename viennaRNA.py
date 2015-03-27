#!/usr/bin/env python
# coding: utf-8

import ctypes
import ctypes.util
import os

# free memory allocated in c
free_c_pointer = ctypes.CDLL(ctypes.util.find_library('c')).free
free_c_pointer.argtypes = [ctypes.c_void_p, ]


# compiled library file path
vienna_clib = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'viennarna.so')


# char* seq_fold(const char*, float*)
__seq_fold = ctypes.CDLL(vienna_clib).seq_fold
__seq_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
# if restype is c_char_p python will convert it to a str
# and no free'ing is possible
__seq_fold.restype = ctypes.c_void_p


def seq_fold(sequence):
    """
    Wrapper to seq_fold
    """
    mfe = ctypes.c_float()
    c_structure = __seq_fold(sequence, ctypes.byref(mfe))

    structure = ctypes.cast(c_structure, ctypes.c_char_p).value
    free_c_pointer(c_structure)
    return (structure, mfe.value)


# char* seq_pf_fold(const char*, float*)
__seq_pf_fold = ctypes.CDLL(vienna_clib).seq_pf_fold
__seq_pf_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
# if restype is c_char_p python will convert it to a str
# and no free'ing is possible
__seq_pf_fold.restype = ctypes.c_void_p


def seq_pf_fold(sequence):
    """
    Wrapper to seq_pf_fold
    """
    gfe = ctypes.c_float()
    c_structure = __seq_pf_fold(sequence, ctypes.byref(gfe))

    structure = ctypes.cast(c_structure, ctypes.c_char_p).value
    free_c_pointer(c_structure)
    return (structure, gfe.value)


class __SOLUTION(ctypes.Structure):
    """
    Implementation of the SOLUTION struct.

    typedef struct {
        float energy;
        char *structure;
    } SOLUTION;
    """
    _fields_ = [('energy', ctypes.c_float), ('c_structure', ctypes.c_void_p)]

# SOLUTION* seq_subopt(const char*, float)
__seq_subopt = ctypes.CDLL(vienna_clib).seq_subopt
__seq_subopt.argtypes = [ctypes.c_char_p, ctypes.c_float]
__seq_subopt.restype = ctypes.POINTER(__SOLUTION)


def seq_subopt(sequence, delta):
    """
    Wrapper to seq_subopt
    """
    sol = __seq_subopt(sequence, ctypes.c_float(delta))

    sol_tuples = set()
    for s in sol:
        if s.c_structure is None:
            break
        sol_tuples.add((ctypes.cast(s.c_structure, ctypes.c_char_p).value,
                       s.energy))
        free_c_pointer(s.c_structure)
    free_c_pointer(sol)

    return sol_tuples


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


__possible_pairs_of = {'a': {'u'}, 'c': {'g'}, 'g': {'c', 'u'},
                       'u': {'a', 'g'}, 'A': {'U'}, 'C': {'G'},
                       'G': {'C', 'U'}, 'U': {'A', 'G'}}


def seq_str_compatible(sequence, structure):
    """
    Determines if a sequence and structure pais is compatible.
    """
    for pair in str_base_pairs(structure):
        if sequence[pair[0]] not in __possible_pairs_of[sequence[pair[1]]]:
            return False
    return True


# float seq_eval(const char*, const char*)
__seq_eval = ctypes.CDLL(vienna_clib).seq_eval
__seq_eval.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
__seq_eval.restype = ctypes.c_float


def seq_eval(sequence, structure):
    """
    Wrapper to seq_eval
    """
    return __seq_eval(sequence, structure)


# float get_T(void)
__get_T = ctypes.CDLL(vienna_clib).get_T
__get_T.restype = ctypes.c_float


def get_T():
    """
    Wrapper to get_T
    """
    return __get_T()


# void set_T(float)
__set_T = ctypes.CDLL(vienna_clib).set_T
__set_T.argtypes = [ctypes.c_float, ]


def set_T(temperature):
    """
    Wrapper to set_T
    """
    __set_T(temperature)


# float str_inverse(char*, const char*, int)
__str_inverse = ctypes.CDLL(vienna_clib).str_inverse
__str_inverse.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                          ctypes.c_uint, ctypes.c_int]
__str_inverse.restype = ctypes.c_float


def str_inverse(seed, structure, rng_seed=None, give_up=False):
    """
    Wrapper to str_inverse
    """
    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = long(time.time() * 256)  # use fractional seconds

    sequence = ctypes.create_string_buffer(seed)
    dist = __str_inverse(sequence, structure, rng_seed, 1 if give_up else 0)

    return (sequence.value, dist)


# float str_pf_inverse(char*, const char*, int, float)
__str_pf_inverse = ctypes.CDLL(vienna_clib).str_pf_inverse
__str_pf_inverse.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                             ctypes.c_long, ctypes.c_uint,
                             ctypes.c_float]
__str_pf_inverse.restype = ctypes.c_float


def str_pf_inverse(seed, structure, rng_seed=None, give_up=False,
                   delta_target=0.0):
    """
    Wrapper to str_pf_inverse
    """
    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = long(time.time() * 256)  # use fractional seconds

    sequence = ctypes.create_string_buffer(seed)
    dist = __str_pf_inverse(sequence, structure, rng_seed,
                            1 if give_up else 0, delta_target)

    return (sequence.value, dist)


if __name__ == '__main__':

    # Optimal fold
    sequence = 'CGCAGGGAUACCCGCGCC'
    structure, mfe = seq_fold(sequence)
    print('%s %s %f' % (sequence, structure, mfe))

    structure, gfe = seq_pf_fold(sequence)
    print('%s %s %f' % (sequence, structure, gfe))

    print('')

    # Find suboptimal structures
    sol_tuples = seq_subopt(sequence, 4.0)
    for s in sol_tuples:
        print('%s %s %f' % ((sequence,) + s))

    print('')

    # Evaluate fe of a structure (given a sequence)...
    print('%f' % get_T())
    test_str = '(((.((.....)))))..'
    print('%s %s %f' % (sequence, test_str, seq_eval(sequence, test_str)))
    # ... and how it changes with temperature
    set_T(15.0)
    print('%f' % get_T())
    print('%s %s %f' % (sequence, test_str, seq_eval(sequence, test_str)))
    set_T(37.0)

    print('')

    # Check compatiblity of sequence and structure
    seed_seq = 'AAUAGGGAUACCCGCGCC'
    print('%s %f' % (seq_str_compatible(sequence, test_str),
                     seq_eval(sequence, test_str)))
    print('%s %f' % (seq_str_compatible(seed_seq, test_str),
                     seq_eval(seed_seq, test_str)))

    print('')

    # Take a not so different sequence with a different optimal structure
    structure, mfe = seq_fold(seed_seq)
    print('%s %s %f' % (seed_seq, structure, mfe))

    # See that is not even stable on the test fold
    print('%s %s %f' % (seed_seq, test_str, seq_eval(seed_seq, test_str)))

    # Mutate it until you get the test fold...
    seq, dist = str_inverse(seed_seq, test_str, 12345)
    # ... and confirm it's its ground state
    structure, mfe = seq_fold(seq)
    print('%s %s %f' % (seq, structure, mfe))
