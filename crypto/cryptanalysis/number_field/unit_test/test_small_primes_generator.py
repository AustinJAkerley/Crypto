#!/usr/bin/python3
# Title: Unit Test for Small Primes Generator
# Creator: Austin Akerley
# Date Created: 11/26/2019
# Last Editor: Austin Akerley
# Date Last Edited: 01/18/2019
# Associated Book Page Nuber: N/A

import unittest
from ..list_small_primes import list_small_primes

class TestSmallPrimesGenerator(unittest.TestCase):
    def test_small_primes_1(self):
        print("\n\nRunning test for cryptanalysis module: list_small_primes")
        max_val = 20
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19]
        primes = list_small_primes(max_val)
        self.assertEqual(primes, expected_primes)

if __name__ == '__main__':
    unittest.main()
