#!/usr/bin/env python
# coding: utf-8

import ctypes
import os

# char* seq_fold(char*, float*)
__seq_fold = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.dylib')).seq_fold
__seq_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
__seq_fold.restype = ctypes.c_char_p

def seq_fold(sequence):
    mfe = ctypes.c_float()
    structure = __seq_fold(sequence, ctypes.byref(mfe))
    return (structure, mfe)

# char* seq_pf_fold(char*, float*)
__seq_pf_fold = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.dylib')).seq_pf_fold
__seq_pf_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
__seq_pf_fold.restype = ctypes.c_char_p

def seq_pf_fold(sequence):
    gfe = ctypes.c_float()
    structure = __seq_pf_fold(sequence, ctypes.byref(gfe))
    return (structure, gfe)

# typedef struct {
#     float energy;
#     char *structure;
# } SOLUTION;
class __SOLUTION(ctypes.Structure):
    _fields_ = [('energy', ctypes.c_float), ('structure', ctypes.c_char_p)]

# SOLUTION* seq_subopt(char*, float)
__seq_subopt = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.dylib')).seq_subopt
__seq_subopt.argtypes = [ctypes.c_char_p, ctypes.c_float]
__seq_subopt.restype = ctypes.POINTER(__SOLUTION)

def seq_subopt(sequence, delta):
    sol = __seq_subopt(sequence, ctypes.c_float(delta))
    sol_tuples = set()
    for s in sol:
        if s.structure == None: break
        sol_tuples.add((s.structure, s.energy))
    return sol_tuples

if __name__ == '__main__':

    sequence = 'CGCAGGGAUACCCGCGCC'
    structure, mfe = seq_fold(sequence)
    print('%s\n%s' % (sequence, structure))
    structure, gfe = seq_pf_fold(sequence)
    print('%s\n%f, %f' % (structure, mfe.value, gfe.value))
    sol_tuples = seq_subopt(sequence, 4.0)
    for s in sol_tuples:
        print('%f, %s' % (s[1], s[0]))
