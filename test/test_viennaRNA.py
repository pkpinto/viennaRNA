#!/usr/bin/env python
# coding: utf-8

import unittest
import viennaRNA as RNA


class viennaRNATest(unittest.TestCase):
    """
    Unit tests for viennaRNA functions.
    """

    def test_fold(self):
        """

        """
        sequence = 'CGCAGGGAUACCCGCGCC'

        structure, mfe = RNA.seq_fold(sequence)

        self.assertTrue(structure == '(((.(((...))))))..')
        self.assertTrue(abs(mfe - (-6.000000)) < 0.00001)

        structure, gfe = RNA.seq_pf_fold(sequence)
        self.assertTrue(structure == '(((.(({...))})))..')
        self.assertTrue(abs(gfe - (-6.504920)) < 0.00001)

    def test_suboptimal(self):
        """

        """
        sequence = 'CGCAGGGAUACCCGCGCC'
        # delta is chosen to avoid the degenerate structures
        sol_tuples = RNA.seq_subopt(sequence, 1.35, sort=True)
        expected_sol_tuples = (('(((.(((...))))))..', -6.000000),
                               ('(((.((....)).)))..', -5.900000),
                               ('.((.(((...)))))...', -4.700000))

        for i, s in enumerate(sol_tuples):
            self.assertTrue(s[0] == expected_sol_tuples[i][0])
            self.assertTrue(abs(s[1] - expected_sol_tuples[i][1]) < 0.00001)

    def test_eval(self):
        """

        """
        sequence = 'CGCAGGGAUACCCGCGCC'
        structure = '(((.((.....)))))..'

        energy = RNA.seq_eval(sequence, structure, T=37.0)
        self.assertTrue(abs(energy - (-3.900000)) < 0.00001)
        energy = RNA.seq_eval(sequence, structure, T=15.0)
        self.assertTrue(abs(energy - (-6.590000)) < 0.00001)

    def test_compatibility_check(self):
        """

        """
        sequence = 'CGCAGGGAUACCCGCGCC'
        structure = '(((.((.....)))))..'
        self.assertTrue(RNA.seq_str_compatible(sequence, structure))

        sequence = 'AAUAGGGAUACCCGCGCC'
        self.assertFalse(RNA.seq_str_compatible(sequence, structure))
        energy = RNA.seq_eval(sequence, structure)
        self.assertTrue(abs(energy - (6.300000)) < 0.00001)

    def test_inverse_fold(self):
        """

        """
        sequence = 'AAUAGGGAUACCCGCGCC'
        target_structure = '(((.((.....)))))..'

        # # sequence has a ground state structure
        # # different from target structure
        # structure, mfe = RNA.seq_fold(sequence)
        # self.assertTrue(structure == '....(((...))).....')
        # self.assertTrue(abs(mfe - (-2.50)) < 0.00001)

        # # sequence is not stable in target structure
        # self.assertFalse(RNA.seq_str_compatible(sequence, target_structure))
        # energy = RNA.seq_eval(sequence, target_structure)
        # self.assertTrue(abs(energy - (6.30)) < 0.00001)

        # find target sequence stable in target structure
        target_sequence, dist = RNA.str_inverse(sequence,
                                                target_structure,
                                                rng_seed=12345)
        self.assertTrue(target_sequence == 'AGUAGGGAUAGCCGCUCC')
        self.assertTrue(abs(dist) < 0.00001)

        # # confirm target structure is ground state of target sequence
        # structure, mfe = RNA.seq_fold(target_sequence)
        # self.assertTrue(structure == target_structure)
        # self.assertTrue(abs(mfe - (-2.00)) < 0.00001)


if __name__ == '__main__':
    unittest.main()
