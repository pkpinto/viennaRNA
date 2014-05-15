#!/usr/bin/env python
# coding: utf-8

import ctypes
import os

# typedef struct
# {
#     char *sequence;
#     char *structure;
#     float mfe;
#     float gfe;
# } seqdata;
class seqdata(ctypes.Structure):
    _fields_ = [('sequence', ctypes.c_char_p), ('structure', ctypes.c_char_p),
                ('mfe',ctypes.c_float), ('gfe',ctypes.c_float)]

# void sequencefold(seqdata *s)
seqfold = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.dylib')).sequencefold
seqfold.argtypes = [ctypes.POINTER(seqdata)]
seqfold.restype = None

# void sequencepf(seqdata *s)
seqpf = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.dylib')).sequencepf
seqpf.argtypes = [ctypes.POINTER(seqdata)]
seqpf.restype = None

if __name__ == '__main__':

    sd = seqdata(sequence='CGCAGGGAUACCCGCGCC')
    seqfold(ctypes.byref(sd))
    seqpf(ctypes.byref(sd))
    print('%s\n%s\n%f\n%f\n' % (sd.sequence, sd.structure, sd.mfe, sd.gfe))
