# coding: utf-8

from .__version__ import __version__

__all__ = ['seq_fold', 'seq_pf_fold', 'seq_subopt']

from .viennaRNA import seq_fold, seq_pf_fold, seq_subopt
# previous line also place viennaRNA inside viennaRNA
del viennaRNA
