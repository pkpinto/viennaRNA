import pytest
import viennaRNA as vrna


class TestRNA:

    def test_fold(self):

        sequence = 'CGCAGGGAUACCCGCGCC'

        structure, mfe = vrna.sequence_fold(sequence)
        assert(structure == '(((.(((...))))))..')
        assert(abs(mfe - (-6.000000)) < 0.00001)

        structure, gfe = vrna.pf_sequence_fold(sequence)
        assert(structure == '(((.(({...))})))..')
        assert(abs(gfe - (-6.504920)) < 0.00001)

    def test_suboptimal(self):

        sequence = 'CGCAGGGAUACCCGCGCC'
        # delta is chosen to avoid the degenerate structures
        sol_tuples = vrna.subopt_structures(sequence, 1.35, sort=True)
        expected_sol_tuples = (('(((.(((...))))))..', -6.000000),
                               ('(((.((....)).)))..', -5.900000),
                               ('.((.(((...)))))...', -4.700000))

        for i, s in enumerate(sol_tuples):
            assert(s[0] == expected_sol_tuples[i][0])
            assert(abs(s[1] - expected_sol_tuples[i][1]) < 0.00001)

        sols_in_delta = len(sol_tuples)
        sol_tuples = vrna.subopt_structures(sequence, 1.35, sort=False)
        assert(len(sol_tuples) == sols_in_delta)

    def test_eval(self):

        sequence = 'CGCAGGGAUACCCGCGCC'
        structure = '(((.((.....)))))..'

        energy = vrna.eval_structure(sequence, structure, T=37.0)
        assert(abs(energy - (-3.900000)) < 0.00001)
        energy = vrna.eval_structure(sequence, structure, T=15.0)
        assert(abs(energy - (-6.590000)) < 0.00001)

    def test_compatibility_check(self):

        sequence = 'CGCAGGGAUACCCGCGCC'
        structure = '(((.((.....)))))..'
        assert(vrna.seq_str_compatible(sequence, structure))

        sequence = 'AAUAGGGAUACCCGCGCC'
        assert(not vrna.seq_str_compatible(sequence, structure))
        energy = vrna.eval_structure(sequence, structure)
        assert(abs(energy - (6.300000)) < 0.00001)

    def test_inverse_fold(self):

        sequence = 'AAUAGGGAUACCCGCGCC'
        target_structure = '(((.((.....)))))..'

        # sequence has a ground state structure
        # different from target structure
        structure, mfe = vrna.sequence_fold(sequence)
        assert(structure == '....(((...))).....')
        assert(abs(mfe - (-2.600000)) < 0.00001)

        # sequence is not stable in target structure
        assert(not vrna.seq_str_compatible(sequence, target_structure))
        energy = vrna.eval_structure(sequence, target_structure)
        assert(abs(energy - (6.30)) < 0.00001)

        # find target sequence stable in target structure
        target_sequence, _ = vrna.sequence_design(sequence, target_structure, rng_seed=12345)
        assert(target_sequence == 'AGUAGGGAUAGCCGCUCC')
        # confirm target structure is ground state of target sequence
        structure, mfe = vrna.sequence_fold(target_sequence)
        assert(structure == target_structure)
        assert(abs(mfe - (-1.600000)) < 0.00001)
        # and without rng seed
        # it's stochastic, we cannot guarantee the target, only that it differs from sequence
        target_sequence, _ = vrna.sequence_design(sequence, target_structure)
        assert(target_sequence != sequence)

        # find target sequence stable in target structure
        target_sequence, _ = vrna.pf_sequence_design(sequence, target_structure, rng_seed=12345)
        assert(target_sequence == 'GCGAGCUCAAUGCCGCAA')
        # and without rng seed
        # it's stochastic, we cannot guarantee the target, only that it differs from sequence
        target_sequence, _ = vrna.pf_sequence_design(sequence, target_structure)
        assert(target_sequence != sequence)
