# coding: utf-8

from .__version__ import __version_info__
from .__version__ import __version__

__all__ = ['seq_fold', 'seq_pf_fold', 'seq_subopt', 'seq_eval',\
           'get_T', 'set_T', 'str_inverse', 'str_pf_inverse']

from .viennaRNA import seq_fold, seq_pf_fold, seq_subopt, seq_eval,\
                       get_T, set_T, str_inverse, str_pf_inverse

# previous line also place viennaRNA inside viennaRNA
del viennaRNA
