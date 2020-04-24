import ctypes
import ctypes.util
import os

# free memory allocated in c
_free_c_pointer = ctypes.CDLL(ctypes.util.find_library('c')).free
_free_c_pointer.argtypes = [ctypes.c_void_p, ]


# compiled library file path
_vienna_clib = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viennarna.so')


# float get_T(void)
_get_T = ctypes.CDLL(_vienna_clib).get_T
_get_T.restype = ctypes.c_float


# void set_T(float)
_set_T = ctypes.CDLL(_vienna_clib).set_T
_set_T.argtypes = [ctypes.c_float, ]


# char* seq_fold(const char*, float*)
_seq_fold = ctypes.CDLL(_vienna_clib).seq_fold
_seq_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
# if restype is c_char_p python will convert it to a str
# and no free'ing is possible
_seq_fold.restype = ctypes.c_void_p


def seq_fold(sequence, T=37.0):
    """
    Wrapper to seq_fold
    """
    default_T = _get_T()
    if T != default_T:
        _set_T(T)

    mfe = ctypes.c_float()
    c_structure = _seq_fold(sequence.encode('ascii'), ctypes.byref(mfe))
    structure = ctypes.cast(c_structure, ctypes.c_char_p).value
    _free_c_pointer(c_structure)

    if T != default_T:
        _set_T(default_T)
    return (structure.decode('utf-8'), mfe.value)


# char* seq_pf_fold(const char*, float*)
_seq_pf_fold = ctypes.CDLL(_vienna_clib).seq_pf_fold
_seq_pf_fold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
# if restype is c_char_p python will convert it to a str
# and no free'ing is possible
_seq_pf_fold.restype = ctypes.c_void_p


def seq_pf_fold(sequence, T=37.0):
    """
    Wrapper to seq_pf_fold
    """
    default_T = _get_T()
    if T != default_T:
        _set_T(T)

    gfe = ctypes.c_float()
    c_structure = _seq_pf_fold(sequence.encode('ascii'), ctypes.byref(gfe))
    structure = ctypes.cast(c_structure, ctypes.c_char_p).value
    _free_c_pointer(c_structure)

    if T != default_T:
        _set_T(default_T)
    return (structure.decode('utf-8'), gfe.value)


class _SOLUTION(ctypes.Structure):
    """
    Implementation of the SOLUTION struct.

    typedef struct {
        float energy;
        char *structure;
    } SOLUTION;
    """
    _fields_ = [('energy', ctypes.c_float), ('c_structure', ctypes.c_void_p)]

# SOLUTION* seq_subopt(const char*, float)
_seq_subopt = ctypes.CDLL(_vienna_clib).seq_subopt
_seq_subopt.argtypes = [ctypes.c_char_p, ctypes.c_float]
_seq_subopt.restype = ctypes.POINTER(_SOLUTION)


def seq_subopt(sequence, delta, sort=False, T=37.0):
    """
    Wrapper to seq_subopt
    """
    default_T = _get_T()
    if T != default_T:
        _set_T(T)

    sol = _seq_subopt(sequence.encode('ascii'), ctypes.c_float(delta))

    sol_tuples = set()
    for s in sol:
        if s.c_structure is None:
            break
        sol_tuples.add((ctypes.cast(s.c_structure, ctypes.c_char_p).value.decode('utf-8'), s.energy))
        _free_c_pointer(s.c_structure)
    _free_c_pointer(sol)

    if T != default_T:
        _set_T(default_T)

    if sort:
        return sorted(sol_tuples, key=lambda s: s[1])
    else:
        return sol_tuples


# float seq_eval(const char*, const char*)
_seq_eval = ctypes.CDLL(_vienna_clib).seq_eval
_seq_eval.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_seq_eval.restype = ctypes.c_float


def seq_eval(sequence, structure, T=37.0):
    """
    Wrapper to seq_eval
    """
    default_T = _get_T()
    if T != default_T:
        _set_T(T)

    energy = _seq_eval(sequence.encode('ascii'), structure.encode('ascii'))

    if T != default_T:
        _set_T(default_T)
    return energy


# float str_inverse(char*, const char*, int)
_str_inverse = ctypes.CDLL(_vienna_clib).str_inverse
_str_inverse.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                         ctypes.c_uint, ctypes.c_int]
_str_inverse.restype = ctypes.c_float


def str_inverse(seed, structure, rng_seed=None, give_up=False, T=37.0):
    """
    Wrapper to str_inverse
    """
    default_T = _get_T()
    if T != default_T:
        _set_T(T)

    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = long(time.time() * 256)  # use fractional seconds

    sequence = ctypes.create_string_buffer(str(seed).encode('ascii'))
    dist = _str_inverse(sequence, structure.encode('ascii'), rng_seed, 1 if give_up else 0)

    if T != default_T:
        _set_T(default_T)
    return (sequence.value.decode('utf-8'), dist)


# float str_pf_inverse(char*, const char*, int, float)
_str_pf_inverse = ctypes.CDLL(_vienna_clib).str_pf_inverse
_str_pf_inverse.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                            ctypes.c_long, ctypes.c_uint,
                            ctypes.c_float]
_str_pf_inverse.restype = ctypes.c_float


def str_pf_inverse(seed, structure, rng_seed=None, give_up=False,
                   delta_target=0.0, T=37.0):
    """
    Wrapper to str_pf_inverse
    """
    default_T = _get_T()
    if T != default_T:
        _set_T(T)

    if not rng_seed:
        # seeding identical to cpython random.seed
        import time
        rng_seed = long(time.time() * 256)  # use fractional seconds

    sequence = ctypes.create_string_buffer(seed)
    dist = _str_pf_inverse(sequence.encode('ascii'), structure.encode('ascii'), rng_seed,
                           1 if give_up else 0, delta_target)

    if T != default_T:
        _set_T(default_T)
    return (sequence.value.decode('utf-8'), dist)
