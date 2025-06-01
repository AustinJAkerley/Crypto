#!/usr/bin/python3
# Title: Unit Test for Naive Factoring Algorithm
# Creator: Austin Akerley
# Date Created: 12/25/2019
# Last Editor: Austin Akerley
# Date Last Edited: 02/03/2020
# Associated Book Page Nuber: N/A

import unittest
from ..naive_factor import naive_factor

class TestNaiveFactor(unittest.TestCase):
    def test_naive_factor_1(self):
        print("\n\nRunning test for cryptanalysis module: naive_factor")
        h = 100
        expected_prime_factors = [2, 2, 5, 5]
        result = naive_factor(h)
        self.assertEqual(result["prime_factors"], expected_prime_factors)

    def test_naive_factor_2(self):
        h = 97
        expected_prime_factors = [97]
        result = naive_factor(h)
        self.assertEqual(result["prime_factors"], expected_prime_factors)

if __name__ == '__main__':
    unittest.main()
