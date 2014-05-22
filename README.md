viennaRNA
=========

Python wrapper for the ViennaRNA Package (RNAlib)

Allows access to fold, pf_fold, subopt, energy_of_structure, inverse_fold and
inverse_pf_fold. Additionally, temperature can be set/get directly.

|RNAlib              |python call    |
|--------------------|---------------|
|fold                |seq_fold       |
|pf_fold             |seq_pf_fold    |
|subopt              |seq_subopt     |
|energy_of_structure |seq_eval       |
|temperature         |get_T / set_T  |
|inverse_fold        |str_inverse    |
|inverse_pf_fold     |str_pf_inverse |
