# viennaRNA

[![Join the chat at https://gitter.im/pmsppinto/viennaRNA](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pmsppinto/viennaRNA?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Python wrapper for the ViennaRNA Package ([RNAlib](https://www.tbi.univie.ac.at/RNA/)). At this time, the lastest latest stable release is Version 2.4.14 from August 13th 2019. Its source code can be found in https://github.com/ViennaRNA/ViennaRNA.

This library allows access to fold, pf_fold, subopt, energy_of_structure, inverse_fold and inverse_pf_fold. Additional functions are available for sequence/structure analysis.

| RNAlib function      | python call         |
|----------------------|---------------------|
| fold                 | seq_fold            |
| pf_fold              | seq_pf_fold         |
| subopt               | seq_subopt          |
| energy_of_structure  | seq_eval            |
| inverse_fold         | str_inverse         |
| inverse_pf_fold      | str_pf_inverse      |

| RNAlib               | python call         |
|----------------------|---------------------|
| n.a.                 | str_base_pairs      |
| n.a.                 | seq_str_compatible  |

## Installation

Use pip to install this package, after cloning from github:
```
pip install .
```

Ensure that ViennaRNA ([RNAlib](https://www.tbi.univie.ac.at/RNA/)) has been installed in a location available to the c compiler:
```
export LIBRARY_PATH=$C_INCLUDE_PATH;<ViennaRNA base path>/lib"
export C_INCLUDE_PATH=$C_INCLUDE_PATH;<ViennaRNA base path>/include"
```

## Tests

Unit tests have been implemented using pytest. To run them, additional dependencies need be installed:
```
pip install ".[test]"
```

The tests can then be run using:
```
python -m pytest -v tests/
```
from the root of the repo (running it explicitly on the tests/ directory avoids interference with the venv folders).