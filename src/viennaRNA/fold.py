import ctypes
import ctypes.util
import os


# free memory allocated in c
_free_c_pointer = ctypes.CDLL(ctypes.util.find_library('c')).free
_free_c_pointer.argtypes = [ctypes.c_void_p,]

# compiled library file path
_vienna_clib = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')


# float get_temperature(void)
_get_temperature = ctypes.CDLL(_vienna_clib).get_temperature
_get_temperature.restype = ctypes.c_float

# void set_temperature(float)
_set_temperature = ctypes.CDLL(_vienna_clib).set_temperature
_set_temperature.argtypes = [ctypes.c_float,]


# float* sequence_fold(const char*, char*)
_sequence_fold = ctypes.CDLL(_vienna_clib).sequence_fold
_sequence_fold.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_sequence_fold.restype = ctypes.c_float

def sequence_fold(sequence, T=37.0):
    _set_temperature(T)

    structure = ctypes.c_char_p(''.encode('ascii'))
    mfe = _sequence_fold(sequence.encode('ascii'), structure)

    return (structure.value.decode('utf-8'), mfe)


# char* pf_sequence_fold(const char*, float*)
_pf_sequence_fold = ctypes.CDLL(_vienna_clib).pf_fold
_pf_sequence_fold.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_pf_sequence_fold.restype = ctypes.c_float

def pf_sequence_fold(sequence, T=37.0):
    _set_temperature(T)

    structure = ctypes.c_char_p(''.encode('ascii'))
    gfe = _pf_sequence_fold(sequence.encode('ascii'), structure)

    return (structure.value.decode('utf-8'), gfe)


class _SOLUTION(ctypes.Structure):
    '''
    Implementation of the SOLUTION struct.
    Deprecated (RNALib 2.4.14) but it's the return value of subopt (which is NOT deprecated)

    typedef struct {
        float energy;
        char* structure;
    } SOLUTION;
    '''
    _fields_ = [('energy', ctypes.c_float), ('c_structure', ctypes.c_void_p)]

# SOLUTION* subopt_structures(const char*, float)
_subopt_structures = ctypes.CDLL(_vienna_clib).subopt_structures
_subopt_structures.argtypes = [ctypes.c_char_p, ctypes.c_float]
_subopt_structures.restype = ctypes.POINTER(_SOLUTION)

def subopt_structures(sequence, delta, sort=False, T=37.0):
    _set_temperature(T)

    sol = _subopt_structures(sequence.encode('ascii'), ctypes.c_float(delta))

    sol_tuples = list()
    for s in sol:
        if s.c_structure is None:
            break
        sol_tuples.append((ctypes.cast(s.c_structure, ctypes.c_char_p).value.decode('utf-8'), s.energy))
        _free_c_pointer(s.c_structure)
    _free_c_pointer(sol)

    if sort:
        return sorted(sol_tuples, key=lambda s: s[1])
    else:
        return sol_tuples


# float eval_structure(const char*, const char*)
_eval_structure = ctypes.CDLL(_vienna_clib).eval_structure
_eval_structure.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_eval_structure.restype = ctypes.c_float

def eval_structure(sequence, structure, T=37.0):
    _set_temperature(T)

    return _eval_structure(sequence.encode('ascii'), structure.encode('ascii'))


# float str_inverse(char*, const char*, int)
_sequence_design = ctypes.CDLL(_vienna_clib).sequence_design
_sequence_design.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_int]
_sequence_design.restype = ctypes.c_float

def sequence_design(seed, structure, rng_seed=None, give_up=False, T=37.0):
    _set_temperature(T)

    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = int(time.time() * 256)  # use fractional seconds

    sequence = ctypes.create_string_buffer(str(seed).encode('ascii'))
    dist = _sequence_design(sequence, structure.encode('ascii'), rng_seed, 1 if give_up else 0)

    return (sequence.value.decode('utf-8'), dist)


# float str_pf_inverse(char*, const char*, int, float)
_pf_sequence_design = ctypes.CDLL(_vienna_clib).pf_sequence_design
_pf_sequence_design.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint, ctypes.c_float]
_pf_sequence_design.restype = ctypes.c_float

def pf_sequence_design(seed, structure, rng_seed=None, give_up=False, delta_target=0.0, T=37.0):
    _set_temperature(T)

    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = int(time.time() * 256)  # use fractional seconds

    sequence = ctypes.create_string_buffer(str(seed).encode('ascii'))
    dist = _pf_sequence_design(sequence, structure.encode('ascii'), rng_seed, 1 if give_up else 0, delta_target)

    return (sequence.value.decode('utf-8'), dist)
