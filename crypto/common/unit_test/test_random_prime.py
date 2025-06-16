#!/usr/bin/python3
# Title: Unit Test for Random Prime Generator
# Creator: Austin Akerley
# Date Created: 09/09/2020
# Last Editor: Austin Akerley
# Date Last Edited: 09/09/2020
# Associated Book Page Nuber:

import unittest
from ..random_prime import random_prime
from ..primality_test import primality_test

class TestRandomPrimeGenerator(unittest.TestCase):
    def test_random_prime_1(self):
        print("\n\nGenerating 64-bit random prime number...\n")
        rand_prime = random_prime(64)
        self.assertEqual(primality_test(rand_prime), True)

    def test_random_prime_2(self):
        print("\n\nGenerating 128-bit random prime number...\n")
        rand_prime = random_prime(128)
        self.assertEqual(primality_test(rand_prime), True)

    def test_random_prime_3(self):
        print("\n\nGenerating 256-bit random prime number...\n")
        rand_prime = random_prime(256)
        self.assertEqual(primality_test(rand_prime), True)

    def test_random_prime_4(self):
        print("\n\nGenerating 512-bit random prime number...\n")
        rand_prime = random_prime(512)
        self.assertEqual(primality_test(rand_prime), True)

if __name__ == '__main__':
    unittest.main()
