#!/usr/bin/env python
# coding: utf-8

import ctypes
import ctypes.util
import os

# free memory allocated in c
free_c_pointer = ctypes.CDLL(ctypes.util.find_library('c')).free
free_c_pointer.argtypes = [ctypes.c_void_p,]

# char* seq_fold(const char*, float*)
__seq_fold = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).seq_fold
__seq_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
# if restype is c_char_p python will convert it to a str and no free'ing is possible
__seq_fold.restype = ctypes.c_void_p

def seq_fold(sequence):

    mfe = ctypes.c_float()
    c_structure = __seq_fold(sequence, ctypes.byref(mfe))

    structure = ctypes.cast(c_structure, ctypes.c_char_p).value
    free_c_pointer(c_structure)
    return (structure, mfe.value)

# char* seq_pf_fold(const char*, float*)
__seq_pf_fold = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).seq_pf_fold
__seq_pf_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
# if restype is c_char_p python will convert it to a str and no free'ing is possible
__seq_pf_fold.restype = ctypes.c_void_p

def seq_pf_fold(sequence):

    gfe = ctypes.c_float()
    c_structure = __seq_pf_fold(sequence, ctypes.byref(gfe))

    structure = ctypes.cast(c_structure, ctypes.c_char_p).value
    free_c_pointer(c_structure)
    return (structure, gfe.value)

# typedef struct {
#     float energy;
#     char *structure;
# } SOLUTION;
class __SOLUTION(ctypes.Structure):
    _fields_ = [('energy', ctypes.c_float), ('c_structure', ctypes.c_void_p)]

# SOLUTION* seq_subopt(const char*, float)
__seq_subopt = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).seq_subopt
__seq_subopt.argtypes = [ctypes.c_char_p, ctypes.c_float]
__seq_subopt.restype = ctypes.POINTER(__SOLUTION)

def seq_subopt(sequence, delta):

    sol = __seq_subopt(sequence, ctypes.c_float(delta))

    sol_tuples = set()
    for s in sol:
        if s.c_structure == None: break
        sol_tuples.add((ctypes.cast(s.c_structure, ctypes.c_char_p).value, s.energy))
        free_c_pointer(s.c_structure)
    free_c_pointer(sol)

    return sol_tuples

# float seq_eval(const char*, const char*)
__seq_eval = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).seq_eval
__seq_eval.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
__seq_eval.restype = ctypes.c_float

def seq_eval(sequence, structure):
    return __seq_eval(sequence, structure)

# float get_T(void)
__get_T = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).get_T
__get_T.restype = ctypes.c_float
def get_T(): return __get_T()

# void set_T(float)
__set_T = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).set_T
__set_T.argtypes = [ctypes.c_float,]
def set_T(temperature): __set_T(temperature)

# float str_inverse(char*, const char*, int)
__str_inverse = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).str_inverse
__str_inverse.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_int]
__str_inverse.restype = ctypes.c_float

def str_inverse(seed, structure, rng_seed=None, give_up=False):

    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = long(time.time() * 256) # use fractional seconds

    sequence = ctypes.create_string_buffer(seed)
    dist = __str_inverse(sequence, structure, rng_seed, 1 if give_up else 0)

    return (sequence.value, dist)

# float str_pf_inverse(char*, const char*, int, float)
__str_pf_inverse = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')).str_pf_inverse
__str_pf_inverse.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint, ctypes.c_float]
__str_pf_inverse.restype = ctypes.c_float

def str_pf_inverse(seed, structure, rng_seed=None, give_up=False, delta_target=0.0):

    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = long(time.time() * 256) # use fractional seconds

    sequence = ctypes.create_string_buffer(seed)
    dist = __str_pf_inverse(sequence, structure, rng_seed, 1 if give_up else 0, delta_target)

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

    # Take a not so different sequence with a different optimal structure
    seed_seq = 'AAUAGGGAUACCCGCGCC'
    structure, mfe = seq_fold(seed_seq)
    print('%s %s %f' % (seed_seq, structure, mfe))

    # See that is not even stable on the test fold
    print('%s %s %f' % (seed_seq, test_str, seq_eval(seed_seq, test_str)))

    # Mutate it until you get the test fold...
    seq, dist = str_inverse(seed_seq, test_str, 12345)
    # ... and confirm it's its ground state
    structure, mfe = seq_fold(seq)
    print('%s %s %f' % (seq, structure, mfe))
