viennaRNA
=========

Python wrapper for the ViennaRNA Package (RNAlib)

Allows access to fold, pf_fold, subopt, energy_of_structure, inverse_fold and
inverse_pf_fold. Additional functions are available for sequence/structure 
analysis.

|RNAlib function      |python call         |
|---------------------|--------------------|
|fold                 |seq_fold            |
|pf_fold              |seq_pf_fold         |
|subopt               |seq_subopt          |
|energy_of_structure  |seq_eval            |
|inverse_fold         |str_inverse         |
|inverse_pf_fold      |str_pf_inverse      |

|RNAlib               |python call         |
|---------------------|--------------------|
|n.a.                 |str_base_pairs      |
|n.a.                 |seq_str_compatible  |

Installation is done through distutils. Run "python setup.py build", "python 
setup.py install" to build and install the library into the local site-packages
folder.

Tests are available to run in the test folder. Simply run "python -m unittest 
discover" from the project root. These are not installed in the procedure above.