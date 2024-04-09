#!/usr/bin/python3
# Title: Functional Unit Test for Chinese Remainder Theorem
# Creator: Austin Akerley
# Date Created: 11/26/2019
# Last Editor: Austin Akerley
# Date Last Edited: 01/19/2020
# Associated Book Page Nuber: 84

import unittest
from crypto.cryptanalysis.list_small_primes import list_small_primes

class TestSmallPrimesGenerator(unittest.TestCase):
    def test_list_small_primes_1(self):
        print("\n\nRunning test for cryptanalysis module: list_small_primes")
        OneToOneHundo = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        MyOneToOneHundo = list_small_primes(100)
        self.assertEqual(OneToOneHundo, MyOneToOneHundo)


if __name__ == '__main__':
    unittest.main()
