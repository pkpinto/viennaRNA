viennaRNA
=========

Python wrapper for the ViennaRNA Package (RNAlib)

Allows access to fold, pf_fold, subopt, energy_of_structure, inverse_fold and
inverse_pf_fold. Temperature can be set/get directly and additional functions
are available for sequence/structure analysis.

|RNAlib function     |python call         |
|--------------------|--------------------|
|fold                |seq_fold            |
|pf_fold             |seq_pf_fold         |
|subopt              |seq_subopt          |
|energy_of_structure |seq_eval            |
|inverse_fold        |str_inverse         |
|inverse_pf_fold     |str_pf_inverse      |

|RNAlib variable     |python call         |
|--------------------|--------------------|
|temperature         |get_T / set_T       |

|RNAlib              |python call         |
|--------------------|--------------------|
|n.a.                |str_base_pairs      |
|n.a.                |seq_str_compatible  |
