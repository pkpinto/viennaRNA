import pytest
import viennaRNA as vrna


class TestRNA:

    def test_fold(self):

        sequence = 'CGCAGGGAUACCCGCGCC'

        structure, mfe = vrna.seq_fold(sequence)
        assert(structure == '(((.(((...))))))..')
        assert(abs(mfe - (-6.000000)) < 0.00001)

        structure, gfe = vrna.seq_pf_fold(sequence)
        assert(structure == '(((.(({...))})))..')
        assert(abs(gfe - (-6.504920)) < 0.00001)

    def test_suboptimal(self):

        sequence = 'CGCAGGGAUACCCGCGCC'
        # delta is chosen to avoid the degenerate structures
        sol_tuples = vrna.seq_subopt(sequence, 1.35, sort=True)
        expected_sol_tuples = (('(((.(((...))))))..', -6.000000),
                               ('(((.((....)).)))..', -5.900000),
                               ('.((.(((...)))))...', -4.700000))

        for i, s in enumerate(sol_tuples):
            assert(s[0] == expected_sol_tuples[i][0])
            assert(abs(s[1] - expected_sol_tuples[i][1]) < 0.00001)

    def test_eval(self):

        sequence = 'CGCAGGGAUACCCGCGCC'
        structure = '(((.((.....)))))..'

        energy = vrna.seq_eval(sequence, structure, T=37.0)
        assert(abs(energy - (-3.900000)) < 0.00001)
        energy = vrna.seq_eval(sequence, structure, T=15.0)
        assert(abs(energy - (-6.590000)) < 0.00001)

    def test_compatibility_check(self):

        sequence = 'CGCAGGGAUACCCGCGCC'
        structure = '(((.((.....)))))..'
        assert(vrna.seq_str_compatible(sequence, structure))

        sequence = 'AAUAGGGAUACCCGCGCC'
        assert(not vrna.seq_str_compatible(sequence, structure))
        energy = vrna.seq_eval(sequence, structure)
        assert(abs(energy - (6.300000)) < 0.00001)

    def test_inverse_fold(self):

        sequence = 'AAUAGGGAUACCCGCGCC'
        target_structure = '(((.((.....)))))..'

        # # sequence has a ground state structure
        # # different from target structure
        # structure, mfe = vrna.seq_fold(sequence)
        # assert(structure == '....(((...))).....')
        # assert(abs(mfe - (-2.50)) < 0.00001)

        # # sequence is not stable in target structure
        # self.assertFalse(vrna.seq_str_compatible(sequence, target_structure))
        # energy = vrna.seq_eval(sequence, target_structure)
        # assert(abs(energy - (6.30)) < 0.00001)

        # find target sequence stable in target structure
        target_sequence, dist = vrna.str_inverse(sequence,
                                                target_structure,
                                                rng_seed=12345)
        assert(target_sequence == 'AGUAGGGAUAGCCGCUCC')
        assert(abs(dist) < 0.00001)

        # # confirm target structure is ground state of target sequence
        # structure, mfe = vrna.seq_fold(target_sequence)
        # assert(structure == target_structure)
        # assert(abs(mfe - (-2.00)) < 0.00001)
