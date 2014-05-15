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

if __name__ == '__main__':

    sequence = 'CGCAGGGAUACCCGCGCC'
    structure, mfe = seq_fold(sequence)
    print('%s\n%s' % (sequence, structure))
    structure, gfe = seq_pf_fold(sequence)
    print('%s\n%f, %f' % (structure, mfe.value, gfe.value))
