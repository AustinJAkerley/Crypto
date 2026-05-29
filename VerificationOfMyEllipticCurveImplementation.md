# Z3 Verification of my Elliptic Curve Implementation

**Author:** Austin Akerley  
**Target code:** `crypto/common/curve.py` and its dependencies (`mod_inv.py`, `eea.py`, `fast_power.py`, `mod_sqrt.py`)

## Problem statement

I created this  python cryptography library by folowing a few undergraduate and graduate textbooks in my free time. However, my implementation of curve always bothered me, it never felt right and it was stitched together. Therefore, my project will be using Z3 to verify my implementation of the elliptic curve, it's functions add and mulitply, and some of the dependencies it uses from the library.

Let's get into the details: `crypto/common/curve.py` implements the elliptic-curve group law over an elliptic field: point addition (`add`/`slope`), scalar multiplication (`double_and_add`), and the on-curve check (`is_point_on_curve`) for curves `y^2 = x^3 + A·x + B (mod p)`. The only assurance that the arithmetic is correct is 11 test cases I scraped together in `test_curve.py`. This prototype **imports the real `curve` class** and uses Z3 as an independent specification. Input: a concrete curve (`A`, `B`, `p`). Output: either a proof that an algebraic property holds for *every* point on the curve, or a concrete counterexample. 

A solver is the right tool because unit tests can only check points a human happened to pick — Z3 searches the entire field symbolically and either proves the property (`unsat` on the negation) or returns a witness of a bug. This is why it beats naive.

## Working prototype

My prototype is located at **`crypto/common/z3_curve_verification.py`**. 

### The Spec
The spec is three equations that any correct point addition must satisfy, derived directly from the chord-and-tangent geometry of elliptic curves. To add P=(x1,y1) and Q=(x2,y2), you draw the line through them, find where it intersects the curve a third time, then reflect over the x-axis. That gives:

```
s·(x2 - x1) ≡ y2 - y1  (mod p)   # slope of the chord
x3 ≡ s² - x1 - x2       (mod p)   # x-coordinate of the result
y3 ≡ s·(x1 - x3) - y1   (mod p)   # y-coordinate of the result
```

These come from substituting the line `y = s(x - x1) + y1` into `y² = x³ + Ax + B` and solving for the new point on the curve. Whereas my curve.py implementation computes `s` explicitly via `mod_inv_curve` (EEA). The spec doesn't compute anything — it just asserts "find an `s` in `[0, p)` such that all three equations hold" and lets Z3 solve. The two approaches are completely independent, so if they agree on every input that's meaningful, and if they disagree Z3 hands back the exact point that broke it.


### The Test Code
This is how the Z3 verification prototype breaks down -
1. `verify_add_matches_spec` is an exhaustive differential test of `curve.add`: enumerate every distinct on-curve pair, call `curve.add`, and have Z3 solve the group-law spec for the correct sum. 2. 
2. `verify_multiply_matches_spec` does the same for scalar multiplication, comparing `curve.multiply` against a reference `n·P` built entirely from the Z3 add oracle (`spec_multiply_via_z3`, which handles doubling, the identity, and `P + (−P) = O`). 
3. `prove_closure` and `prove_commutativity` prove those properties hold over the spec for *every* point by asserting the negation and checking for `unsat`. The key part of the encoding is the slope constraint `s·(x2 − x1) ≡ (y2 − y1) (mod p)` — instead of running the extended euclidean algorithm (EEA), Z3 reasons about the modular inverse for all inputs at once. Nonlinear modular arithmetic is encoded with fixed-width **bit-vectors** (multiplication and `URem` are decidable there) so Z3 returns immediately instead of stalling on unbounded nonlinear integers.

Install and run by running the following in a terminal (preferably Linux if you're cool):
```
pip install -r requirements.txt   # installs z3-solver
python -m crypto.common.z3_curve_verification
```

**Input:** 
the curve `y^2 = x^3 + 3x + 8 (mod 13)`, same as `test_curve.py`. 

**Output:**
```
[IMPLEMENTATION] curve.add MATCHES the Z3 group-law spec for ALL distinct on-curve point pairs (8 points checked exhaustively).
[MULTIPLY]       curve.multiply DISAGREES with the spec. Counterexamples found by Z3:
    {'P': (9, 6), 'n': 7, 'curve.multiply': None, 'z3_spec': (9, 6)}
    {'P': (9, 7), 'n': 7, 'curve.multiply': None, 'z3_spec': (9, 7)}
[CLOSURE]        PROVED for ALL distinct on-curve points (Z3 returned unsat -> no counterexample exists).
[COMMUTATIVITY]  PROVED for ALL distinct on-curve points (Z3 returned unsat -> no counterexample exists).
```

### It Found A Real Bug!

The output above shows `curve.multiply((9,6), 7)` returning `None` where Z3 expects `(9,6)`. Here's why.

On `y² = x³ + 3x + 8 (mod 13)`, the point `P = (9,6)` has **order 3**:

- `1·P = (9,6)`
- `2·P = (9,7)`
- `3·P = O` (the point at infinity)

Since `7 mod 3 = 1`, the correct answer is `7·P = P = (9,6)`. Note that `(9,7) = −(9,6)` because `6 + 7 = 13 ≡ 0 (mod 13)`, so `2·P = −P`.

Trace `double_and_add(P, 7)` — `7 = 111₂`, bits low→high, `R` is the accumulator and `addend` is the running double:

1. **bit 1 (n=7):** `R = add(O, P) = (9,6)`. `addend = add(P,P) = 2P = (9,7)`.
2. **bit 1 (n=3):** `R = add((9,6),(9,7))`. ← **`P + (−P)` step.** `addend = add((9,7),(9,7)) = 4P = (9,6)`.
3. **bit 1 (n=1):** `R = add(R, (9,6))`. Then n→0, stop.

At step 2, the correct group law gives `O`, so step 3 becomes `add(O,(9,6)) = (9,6)` — the right answer.

What my implementation does at step 2: `add((9,6),(9,7))` has no `P + (−P)` guard, so it calls `slope`. The generic branch computes `x_diff = (9−9) mod 13 = 0` and `mod_inv_curve(0, 13)` fails, returning `(False, 13)`. `slope` returns `[None, None, 13]` and `add` returns `(None, None, 13)`.

`double_and_add` sees `len(R) == 3` and immediately returns `(None, None, 13)` — aborting before step 3 runs. `_norm` collapses that to `None`. The 11 unit tests miss this because none of my multiply chains pass through the identity.

## Plan for the final
1. Generalize the encoding to accept any `(A, B, p)` instead of the hardcoded curve.
2. Fix the `curve.add`/`double_and_add` identity bug the multiply verifier uncovered (return `(None, None)` for vertical-line additions over a prime field) and re-run to confirm `unsat`.
3. Prove associativity `(P + Q) + R == P + (Q + R)` over the spec.

## AI Usage Policy

I had AI help me draft the spec and get down to the heart of how to solve for the curve point addition declaratively. I used the Claude Opus 4.7 model.