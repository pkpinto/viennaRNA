#!/usr/bin/env python
# coding: utf-8

import ctypes
import os

# char* seq_fold(char*, float*)
seq_fold = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.dylib')).seq_fold
seq_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
seq_fold.restype = ctypes.c_char_p

# char* seq_pf_fold(char*, float*)
seq_pf_fold = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.dylib')).seq_pf_fold
seq_pf_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
seq_pf_fold.restype = ctypes.c_char_p

if __name__ == '__main__':

    sequence='CGCAGGGAUACCCGCGCC'
    mfe, gfe = ctypes.c_float(), ctypes.c_float()
    structure = seq_fold(sequence, ctypes.byref(mfe))
    print('%s\n%s' % (sequence, structure))
    structure = seq_pf_fold(sequence, ctypes.byref(gfe))
    print('%s\n%f, %f' % (structure, mfe.value, gfe.value))
