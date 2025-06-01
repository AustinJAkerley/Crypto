#!/usr/bin/python3
# Title: Unit Test for Lenstras Algorithm
# Creator: Austin Akerley
# Date Created: 12/31/2019
# Last Editor: Austin Akerley
# Date Last Edited:12/31/2019
# Associated Book Page Nuber: 327

import time
import unittest
from crypto.cryptanalysis.ecc.lenstras_algorithm import lenstras_algorithm

class TestLenstrasAlgorithm(unittest.TestCase):
    def test_lenstras_algorithm_8bit(self):
        from crypto.common.random_prime import random_prime
        import time
        print("\n\nRunning test for ecc cryptanalysis module: lenstras_algorithm 8bit")
        p = random_prime(8)  # 8-bit prime
        q = random_prime(8)  # 8-bit prime
        while p == q:
            q = random_prime(8)
        n = p * q
        print(f"Trying to factor n={n} (p={p}, q={q})")
        start = time.time()
        d = lenstras_algorithm(n, max_curves=2000, max_multiplies=20000)
        elapsed = time.time() - start
        print("Found factor:", d)
        print(f"Time to factor: {elapsed:.4f} seconds")
        self.assertIn(d, [p, q])

    def test_lenstras_algorithm_16bit(self):
        from crypto.common.random_prime import random_prime
        import time
        print("\n\nRunning test for lenstras_algorithm with 16-bit primes")
        p = random_prime(16)
        q = random_prime(16)
        while p == q:
            q = random_prime(16)
        n = p * q
        print(f"Trying to factor n={n} (p={p}, q={q})")
        start = time.time()
        d = lenstras_algorithm(n, max_curves=3000, max_multiplies=30000)
        elapsed = time.time() - start
        print("Found factor:", d)
        print(f"Time to factor: {elapsed:.4f} seconds")
        self.assertIn(d, [p, q])

    def test_lenstras_algorithm_24bit(self):
        from crypto.common.random_prime import random_prime
        import time
        print("\n\nRunning test for lenstras_algorithm with 24-bit primes")
        p = random_prime(24)
        q = random_prime(24)
        while p == q:
            q = random_prime(24)
        n = p * q
        print(f"Trying to factor n={n} (p={p}, q={q})")
        start = time.time()
        d = lenstras_algorithm(n, max_curves=5000, max_multiplies=50000)
        elapsed = time.time() - start
        print("Found factor:", d)
        print(f"Time to factor: {elapsed:.4f} seconds")
        self.assertIn(d, [p, q])

    def test_lenstras_algorithm_32bit(self):
        from crypto.common.random_prime import random_prime
        import time
        print("\n\nRunning test for lenstras_algorithm with 32-bit primes")
        p = random_prime(32)
        q = random_prime(32)
        while p == q:
            q = random_prime(32)
        n = p * q
        print(f"Trying to factor n={n} (p={p}, q={q})")
        start = time.time()
        d = lenstras_algorithm(n, max_curves=20000, max_multiplies=100000)
        elapsed = time.time() - start
        print("Found factor:", d)
        print(f"Time to factor: {elapsed:.4f} seconds")
        self.assertIn(d, [p, q])

    def test_lenstras_algorithm_40bit(self):
        from crypto.common.random_prime import random_prime
        import time
        print("\n\nRunning test for lenstras_algorithm with 40-bit primes")
        p = random_prime(40)
        q = random_prime(40)
        while p == q:
            q = random_prime(40)
        n = p * q
        print(f"Trying to factor n={n} (p={p}, q={q})")
        start = time.time()
        d = lenstras_algorithm(n, max_curves=50000, max_multiplies=200000)
        elapsed = time.time() - start
        print("Found factor:", d)
        print(f"Time to factor: {elapsed:.4f} seconds")
        self.assertIn(d, [p, q])
