#!/usr/bin/python3
# Title: Unit Test for Chinese Remainder Theorem
# Creator: Austin Akerley
# Date Created: 11/26/2019
# Last Editor: Austin Akerley
# Date Last Edited: 02/09/2020
# Associated Book Page Nuber: 84

import unittest
from ..crt import crt

class TestCRT(unittest.TestCase):
    def test_crt_1(self):
        print("\n\nRunning test for cryptanalysis module: crt")
        congruences_and_primes = [(8, 13), (2, 11)]
        x = crt(congruences_and_primes)
        expected_x = 73
        self.assertEqual(x, expected_x)

    def test_crt_2(self):
        congruences_and_primes = [(2, 3), (3, 5), (2, 7)]
        x = crt(congruences_and_primes)
        expected_x = 23
        self.assertEqual(x, expected_x)

if __name__ == '__main__':
    unittest.main()
