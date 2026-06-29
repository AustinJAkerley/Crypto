#!/usr/bin/python3
# Title: Unit Test for the toy HAWK "Guessing Game" cryptanalysis
# Creator: Austin Akerley
# Date Created: 06/29/2026
# Last Editor: Austin Akerley
# Date Last Edited: 06/29/2026
# Associated Book Page Nuber: N/A
#
# Exercises the toy reproduction of IACR ePrint 2026/1318
# ("Cryptanalysis of HAWK: a Guessing Game"):
#   * keygen produces a valid (secret basis, public Gram) pair,
#   * the conjugation move G' = U^T G U preserves the lattice (invariant),
#   * the guessing game recovers a secret basis B' with B'^T B' == G,
#   * end-to-end key recovery from the public key alone.

import unittest
import random

from ..hawk import keygen, gram, verify_keypair, random_unimodular
from ..hawk_guessing_game import (
    random_lower_triangular_unimodular,
    conjugate,
    is_isometric_gram,
    success_oracle,
    recover_secret_from_oracle,
    play_guessing_game,
)
from ..toy_linalg import determinant, transpose, matmul, identity


class TestHawkGuessingGame(unittest.TestCase):

    def test_keygen_valid(self):
        print("\n\nRunning test for cryptanalysis module: hawk_guessing_game")
        rng = random.Random(1)
        for n in (2, 3, 4):
            key = keygen(n=n, entry=2, elementary=5, rng=rng)
            B, G = key["secret_basis"], key["public_gram"]
            # Secret basis is unimodular, public Gram is symmetric det-1, and
            # the keypair is internally consistent (B^T B == G).
            self.assertIn(determinant(B), (1, -1))
            self.assertEqual(determinant(G), 1)
            self.assertEqual(gram(B), G)
            self.assertTrue(verify_keypair(B, G))

    def test_conjugation_invariant(self):
        # The central paper invariant: conjugating by a short lower-triangular
        # unimodular U yields a Gram matrix of the SAME lattice.
        rng = random.Random(2)
        for n in (2, 3, 4):
            key = keygen(n=n, entry=2, elementary=5, rng=rng)
            G = key["public_gram"]
            for _ in range(20):
                U = random_lower_triangular_unimodular(n, bound=3, rng=rng)
                G_prime = conjugate(G, U)
                self.assertTrue(is_isometric_gram(G, G_prime, U))
                # Determinant (an isometry invariant) is preserved.
                self.assertEqual(determinant(G_prime), determinant(G))

    def test_isometric_check_rejects_non_unimodular(self):
        # A non-unimodular conjugator changes the lattice and must be rejected
        # by the invariant check.
        rng = random.Random(3)
        key = keygen(n=3, entry=2, elementary=5, rng=rng)
        G = key["public_gram"]
        scale = [[2, 0, 0], [0, 1, 0], [0, 0, 1]]  # det 2, not unimodular
        G_prime = conjugate(G, scale)
        self.assertFalse(is_isometric_gram(G, G_prime, scale))

    def test_oracle_recovers_orthonormal_for_identity_gram(self):
        # On the trivial public form G = I the length-1 vectors are exactly the
        # signed standard basis, so the cheap oracle must find a full set and
        # the recovered "secret" must reproduce I.
        n = 3
        G = identity(n)
        V = success_oracle(G, search_bound=1)
        self.assertIsNotNone(V)
        I = identity(n)  # identity conjugator
        B_rec = recover_secret_from_oracle(I, V)
        self.assertEqual(gram(B_rec), G)

    def test_recovery_reproduces_gram_end_to_end(self):
        # End-to-end: from the public Gram matrix alone, the guessing game
        # recovers a valid HAWK secret basis B' with B'^T B' == G.
        rng = random.Random(2026)
        for seed in range(8):
            key = keygen(n=3, entry=2, elementary=5,
                         rng=random.Random(100 + seed))
            G = key["public_gram"]
            result = play_guessing_game(
                G, search_bound=2, conjugator_bound=3, max_tries=20000,
                rng=random.Random(500 + seed))
            self.assertTrue(result["success"], "guessing game must converge")
            B_rec = result["recovered_basis"]
            # Recovered basis is unimodular and reproduces the public key.
            self.assertIn(determinant(B_rec), (1, -1))
            self.assertEqual(gram(B_rec), G)
            self.assertTrue(verify_keypair(B_rec, G))

    def test_recovered_secret_signs_same_lattice(self):
        # The recovered basis need not equal the original secret, but it must be
        # an equally valid (short, unimodular) secret for the same public key.
        rng = random.Random(7)
        key = keygen(n=3, entry=2, elementary=5, rng=rng)
        B, G = key["secret_basis"], key["public_gram"]
        result = play_guessing_game(G, search_bound=2, conjugator_bound=3,
                                    rng=random.Random(42))
        self.assertTrue(result["success"])
        B_rec = result["recovered_basis"]
        self.assertEqual(gram(B_rec), gram(B))  # same Gram == same lattice form


if __name__ == '__main__':
    unittest.main()
