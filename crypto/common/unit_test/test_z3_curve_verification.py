#!/usr/bin/python3
# Title: Unit Test for Z3 Curve Verification
# Creator: Austin Akerley
# Date Created: 06/06/2026
# Last Editor: Austin Akerley
# Date Last Edited: 06/06/2026
# Associated Book Page Nuber: 299

import unittest
from ..z3_curve_verification import (
    verify_add_matches_spec,
    verify_multiply_matches_spec,
    prove_closure,
    prove_commutativity,
    prove_associativity,
    on_curve_points,
)

# (A, B, p) triples covering a range of curve shapes and field sizes
CURVES = [
    (3, 8, 13),     # baseline curve from test_curve.py
    (2, 3, 7),      # small field
    (1, 1, 5),      # minimal non-trivial prime
    (0, 7, 11),     # A=0 (secp256k1-style)
    (2, 3, 17),     # slightly larger prime
    (1, 6, 19),     # 19-element field
    (4, 20, 29),    # larger prime, more points
]

# Associativity has 18 bitvector variables; primes above ~19 make Z3 very slow.
CURVES_FOR_ASSOCIATIVITY = [c for c in CURVES if c[2] <= 19]


class TestZ3CurveVerification(unittest.TestCase):

    def test_add_matches_spec(self):
        print("\n\nRunning Z3 add-vs-spec for multiple curves")
        for A, B, p in CURVES:
            with self.subTest(A=A, B=B, p=p):
                pts = len(on_curve_points(A, B, p))
                ok, mismatches = verify_add_matches_spec(A, B, p)
                print(f"  curve({A}, {B}, {p}): {pts} points, add OK={ok}")
                self.assertTrue(ok, f"curve({A},{B},{p}) add mismatches: {mismatches[:3]}")

    def test_multiply_matches_spec(self):
        print("\n\nRunning Z3 multiply-vs-spec for multiple curves")
        for A, B, p in CURVES:
            with self.subTest(A=A, B=B, p=p):
                ok, mismatches = verify_multiply_matches_spec(A, B, p)
                print(f"  curve({A}, {B}, {p}): multiply OK={ok}")
                self.assertTrue(ok, f"curve({A},{B},{p}) multiply mismatches: {mismatches[:3]}")

    def test_closure(self):
        print("\n\nRunning Z3 closure proof for multiple curves")
        for A, B, p in CURVES:
            with self.subTest(A=A, B=B, p=p):
                proved, ce = prove_closure(A, B, p)
                print(f"  curve({A}, {B}, {p}): closure proved={proved}")
                self.assertTrue(proved, f"curve({A},{B},{p}) closure failed: {ce}")

    def test_commutativity(self):
        print("\n\nRunning Z3 commutativity proof for multiple curves")
        for A, B, p in CURVES:
            with self.subTest(A=A, B=B, p=p):
                proved, ce = prove_commutativity(A, B, p)
                print(f"  curve({A}, {B}, {p}): commutativity proved={proved}")
                self.assertTrue(proved, f"curve({A},{B},{p}) commutativity failed: {ce}")

    def test_associativity(self):
        print("\n\nRunning Z3 associativity proof for multiple curves")
        for A, B, p in CURVES_FOR_ASSOCIATIVITY:
            with self.subTest(A=A, B=B, p=p):
                proved, ce = prove_associativity(A, B, p)
                print(f"  curve({A}, {B}, {p}): associativity proved={proved}")
                self.assertTrue(proved, f"curve({A},{B},{p}) associativity failed: {ce}")


if __name__ == '__main__':
    unittest.main()
