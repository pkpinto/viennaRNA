# viennaRNA

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://travis-ci.org/pkpinto/viennaRNA.svg?branch=master)](https://travis-ci.org/pkpinto/viennaRNA)
[![Code Coverage](https://codecov.io/gh/pkpinto/viennaRNA/branch/master/graph/badge.svg)](https://codecov.io/gh/pkpinto/viennaRNA)
[![Join the chat at https://gitter.im/pkpintoHUB/viennaRNA](https://badges.gitter.im/pkpintoHUB/viennaRNA.svg)](https://gitter.im/pkpintoHUB/viennaRNA?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Python wrapper for the ViennaRNA Package ([RNAlib](https://www.tbi.univie.ac.at/RNA/)). At this time, the lastest latest stable release is Version 2.4.14 from August 13th 2019. Its source code can be found in https://github.com/ViennaRNA/ViennaRNA.

This library allows access to a small subset of the RNALib functions: vrna_fold, vrna_pf_fold, subopt, vrna_eval_structure_simple, inverse_fold and inverse_pf_fold. Version 4.0 of this API now references the new (thread-safe) RNALib interface where possible. The python function calls have been changed *in a not backwards compatible* way to highlight the new calls:

| RNAlib function             | python call          |
|-----------------------------|----------------------|
| vrna_fold                   |    sequence_fold     |
| vrna_pf_fold                | pf_sequence_fold     |
| subopt                      | subopt_structures    |
| vrna_eval_structure_simple  | eval_structure       |
| inverse_fold                |    sequence_design   |
| inverse_pf_fold             | pf_sequence_design   |

Additional functions are available for sequence/structure analysis:

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
export LIBRARY_PATH="$LIBRARY_PATH:<RNALib base path>/lib"
export C_INCLUDE_PATH="$C_INCLUDE_PATH:<RNALib base path>/include"
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
