# Title: Z3 Verification of the Elliptic Curve Group Law
# Creator: Austin Akerley
# Date Created: 05/29/2026
# Last Editor: Austin Akerley
# Date Last Edited: 05/29/2026
# Associated Book Page Nuber: 299
#
# Uses Z3 as a spec oracle to check crypto.common.curve against the
# chord-and-tangent group law for every point on the curve at once.
#
# INPUT(s) -
# A - type: int, desc: x-coefficient of the curve y^2 = x^3 + A*x + B
# B - type: int, desc: constant term of the curve
# p - type: int, desc: prime field modulus

from z3 import (
    BitVec, BitVecVal, Solver, And, Or, Not, URem, ULT, sat, unsat,
)
from crypto.common.curve import curve

# Bit width large enough to hold intermediate products without overflow.
# Largest product is s*s or s*x3 (< p^2), well within 32 bits for small primes.
_WIDTH = 32


def _bv(name):
    return BitVec(name, _WIDTH)


def _mod(expr, p):
    return URem(expr, BitVecVal(p, _WIDTH))


def _on_curve(x, y, A, B, p): # Z3 constraint: (x, y) lies on y^2 = x^3 + A*x + B (mod p)
    return _mod(y * y, p) == _mod(x * x * x + A * x + B, p)


def _in_field(vars, p): # Z3 constraint: all variables are field elements in [0, p)
    pv = BitVecVal(p, _WIDTH)
    return And([ULT(v, pv) for v in vars])


# Chord-and-tangent addition spec for distinct x1 != x2.
# Rearranged into non-negative sums so URem is well behaved:
#   s*(x2 - x1) == y2 - y1   <=>   s*x2 + y1 == s*x1 + y2
#   x3 == s^2 - x1 - x2      <=>   x3 + x1 + x2 == s^2
#   y3 == s*(x1 - x3) - y1   <=>   y3 + y1 + s*x3 == s*x1
def _add_formula(solver, x1, y1, x2, y2, s, x3, y3, p):
    solver.add(_mod(s * x2 + y1, p) == _mod(s * x1 + y2, p))
    solver.add(_mod(x3 + x1 + x2, p) == _mod(s * s, p))
    solver.add(_mod(y3 + y1 + s * x3, p) == _mod(s * x1, p))


def _model(solver):
    m = solver.model()
    return {str(d): m[d].as_long() for d in m.decls()}


def on_curve_points(A, B, p): # Returns all affine points on y^2 = x^3 + A*x + B (mod p)
    return [
        (x, y)
        for x in range(p)
        for y in range(p)
        if (y * y - (x * x * x + A * x + B)) % p == 0
    ]


def spec_sum_via_z3(A, B, p, P, Q):
    # Use Z3 to solve the group-law spec for the sum of distinct points P and Q.
    # Returns (x3, y3) or None if the spec is unsatisfiable for these inputs.
    x3, y3, s = _bv("x3"), _bv("y3"), _bv("s")
    solver = Solver()
    solver.add(_in_field([x3, y3, s], p))
    x1, y1 = BitVecVal(P[0], _WIDTH), BitVecVal(P[1], _WIDTH)
    x2, y2 = BitVecVal(Q[0], _WIDTH), BitVecVal(Q[1], _WIDTH)
    _add_formula(solver, x1, y1, x2, y2, s, x3, y3, p)
    if solver.check() != sat:
        return None
    m = solver.model()
    return (m[x3].as_long(), m[y3].as_long())


def verify_add_matches_spec(A, B, p):
    # Exhaustive differential check of curve.add against the Z3 spec.
    # For every pair of distinct on-curve points (x1 != x2), runs curve.add
    # and confirms it equals the point Z3 derives from the group-law spec.
    # Returns (ok: bool, mismatches: list).
    my_curve = curve(A, B, p)
    points = on_curve_points(A, B, p)
    mismatches = []
    for P in points:
        for Q in points:
            if P[0] == Q[0]:
                continue  # skip doubling / vertical-line cases
            actual = my_curve.add(P, Q)
            expected = spec_sum_via_z3(A, B, p, P, Q)
            if expected is None or tuple(actual[:2]) != expected:
                mismatches.append({"P": P, "Q": Q,
                                   "curve.add": actual, "z3_spec": expected})
    return (len(mismatches) == 0, mismatches)


# Tangent-doubling spec for P == Q (y1 != 0).
# Rearranged into non-negative sums so URem is well behaved:
#   s*(2*y1) == 3*x1^2 + A   <=>   s*2*y1 == 3*x1*x1 + A
#   x3 == s^2 - 2*x1         <=>   x3 + 2*x1 == s^2
#   y3 == s*(x1 - x3) - y1   <=>   y3 + y1 + s*x3 == s*x1
def _double_formula(solver, x1, y1, s, x3, y3, A, p):
    solver.add(_mod(s * 2 * y1, p) == _mod(3 * x1 * x1 + A, p))
    solver.add(_mod(x3 + 2 * x1, p) == _mod(s * s, p))
    solver.add(_mod(y3 + y1 + s * x3, p) == _mod(s * x1, p))


# Point at infinity (identity element). curve.py uses (None, None); we use None internally.
INFINITY = None


def _norm(point): # Normalize so curve.py's (None, None) and our None both mean O
    if point is None:
        return INFINITY
    if len(point) >= 2 and point[0] is None and point[1] is None:
        return INFINITY
    return (point[0], point[1])


def spec_add_via_z3(A, B, p, P, Q):
    # Full group-law sum using Z3 as the spec oracle.
    # Handles all cases: identity, P + (-P) = O, doubling, and generic addition.
    # Returns a point (x, y) or INFINITY.
    P, Q = _norm(P), _norm(Q)
    if P is INFINITY:
        return Q
    if Q is INFINITY:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 % p == x2 % p and (y1 + y2) % p == 0: # P + (-P) = O (same x, opposite y)
        return INFINITY

    x3, y3, s = _bv("x3"), _bv("y3"), _bv("s")
    solver = Solver()
    solver.add(_in_field([x3, y3, s], p))
    bx1, by1 = BitVecVal(x1, _WIDTH), BitVecVal(y1, _WIDTH)
    bx2, by2 = BitVecVal(x2, _WIDTH), BitVecVal(y2, _WIDTH)

    if x1 % p == x2 % p and y1 % p == y2 % p:
        _double_formula(solver, bx1, by1, s, x3, y3, A, p) # Point doubling (tangent)
    else:
        _add_formula(solver, bx1, by1, bx2, by2, s, x3, y3, p) # Generic addition (chord)

    if solver.check() != sat:
        return None
    m = solver.model()
    return (m[x3].as_long(), m[y3].as_long())


def spec_multiply_via_z3(A, B, p, P, n):
    # Reference scalar multiplication n*P built entirely from the Z3 add spec.
    # Never calls curve.multiply; applies spec_add_via_z3 via double-and-add.
    # Returns a point or INFINITY.
    result = INFINITY
    addend = _norm(P)
    k = n
    while k > 0:
        if k & 1:
            result = spec_add_via_z3(A, B, p, result, addend)
        addend = spec_add_via_z3(A, B, p, addend, addend)
        k >>= 1
    return result


def verify_multiply_matches_spec(A, B, p, max_n=None):
    # Exhaustive differential check of curve.multiply against the Z3-driven spec.
    # For every on-curve point P and scalar n in [0, max_n], runs curve.multiply(P, n)
    # and compares to the Z3 spec result. Defaults max_n to len(points) + 1 to cover
    # a full cycle through the point at infinity. Returns (ok: bool, mismatches: list).
    my_curve = curve(A, B, p)
    points = on_curve_points(A, B, p)
    if max_n is None:
        max_n = len(points) + 1
    mismatches = []
    for P in points:
        for n in range(0, max_n + 1):
            actual = _norm(my_curve.multiply(P, n))
            expected = spec_multiply_via_z3(A, B, p, P, n)
            if actual != expected:
                mismatches.append({"P": P, "n": n,
                                   "curve.multiply": actual, "z3_spec": expected})
    return (len(mismatches) == 0, mismatches)


def prove_closure(A, B, p):
    # Prove (over the spec) that P + Q is always on the curve for x1 != x2.
    # Returns (proved: bool, counterexample: dict | None).
    x1, y1, x2, y2, x3, y3, s = (
        _bv("x1"), _bv("y1"), _bv("x2"), _bv("y2"), _bv("x3"), _bv("y3"), _bv("s"),
    )
    solver = Solver()
    solver.add(_in_field([x1, y1, x2, y2, x3, y3, s], p))
    solver.add(_on_curve(x1, y1, A, B, p))
    solver.add(_on_curve(x2, y2, A, B, p))
    solver.add(x1 != x2)
    _add_formula(solver, x1, y1, x2, y2, s, x3, y3, p)
    solver.add(Not(_on_curve(x3, y3, A, B, p))) # Negation: result is NOT on the curve
    result = solver.check()
    if result == unsat:
        return True, None
    if result == sat:
        return False, _model(solver)
    raise RuntimeError(f"Z3 returned unknown: {result}")


def prove_commutativity(A, B, p):
    # Prove (over the spec) that P + Q == Q + P for all distinct points.
    # Returns (proved: bool, counterexample: dict | None).
    x1, y1, x2, y2 = _bv("x1"), _bv("y1"), _bv("x2"), _bv("y2")
    sPQ, x3, y3 = _bv("sPQ"), _bv("x3"), _bv("y3")  # result of P + Q
    sQP, x4, y4 = _bv("sQP"), _bv("x4"), _bv("y4")  # result of Q + P
    solver = Solver()
    solver.add(_in_field([x1, y1, x2, y2, x3, y3, x4, y4, sPQ, sQP], p))
    solver.add(_on_curve(x1, y1, A, B, p))
    solver.add(_on_curve(x2, y2, A, B, p))
    solver.add(x1 != x2)
    _add_formula(solver, x1, y1, x2, y2, sPQ, x3, y3, p)  # P + Q
    _add_formula(solver, x2, y2, x1, y1, sQP, x4, y4, p)  # Q + P
    solver.add(Or(_mod(x3, p) != _mod(x4, p), _mod(y3, p) != _mod(y4, p))) # Negation: results differ
    result = solver.check()
    if result == unsat:
        return True, None
    if result == sat:
        return False, _model(solver)
    raise RuntimeError(f"Z3 returned unknown: {result}")


def main():
    # Concrete instance: curve(3, 8, 13), the same curve used by test_curve.py.
    A, B, p = 3, 8, 13
    print(f"Verifying crypto.common.curve on: y^2 = x^3 + {A}x + {B} (mod {p})\n")

    ok, mismatches = verify_add_matches_spec(A, B, p)
    pts = len(on_curve_points(A, B, p))
    if ok:
        print(f"[IMPLEMENTATION] curve.add MATCHES the Z3 group-law spec for "
              f"ALL distinct on-curve point pairs ({pts} points checked exhaustively).")
    else:
        print(f"[IMPLEMENTATION] curve.add DISAGREES with the spec. "
              f"Counterexamples found by Z3:")
        for mm in mismatches[:5]:
            print(f"    {mm}")

    ok, mismatches = verify_multiply_matches_spec(A, B, p)
    if ok:
        print(f"[MULTIPLY]       curve.multiply MATCHES the Z3-driven spec for "
              f"ALL on-curve points and scalars (incl. doubling & infinity).")
    else:
        print(f"[MULTIPLY]       curve.multiply DISAGREES with the spec. "
              f"Counterexamples found by Z3:")
        for mm in mismatches[:5]:
            print(f"    {mm}")

    proved, ce = prove_closure(A, B, p)
    if proved:
        print("[CLOSURE]        PROVED for ALL distinct on-curve points "
              "(Z3 returned unsat -> no counterexample exists).")
    else:
        print(f"[CLOSURE]        FAILED. Counterexample found by Z3: {ce}")

    proved, ce = prove_commutativity(A, B, p)
    if proved:
        print("[COMMUTATIVITY]  PROVED for ALL distinct on-curve points "
              "(Z3 returned unsat -> no counterexample exists).")
    else:
        print(f"[COMMUTATIVITY]  FAILED. Counterexample found by Z3: {ce}")

    print("\nNaive unit tests check a handful of points; Z3 checks your "
          "implementation against the spec on every point on the curve.")


if __name__ == "__main__":
    main()
