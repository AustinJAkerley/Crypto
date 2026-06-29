# Toy Reproduction of "Cryptanalysis of HAWK: a Guessing Game"

**Author:** Austin Akerley
**Paper:** B. Nelson, J. Limbrey, C. Ling, A. Mendelsohn,
*"Cryptanalysis of HAWK: a Guessing Game"*, IACR ePrint **2026/1318**.
**Code:** `crypto/cryptanalysis/lattice/` — `toy_linalg.py`, `hawk.py`,
`hawk_guessing_game.py`, and `unit_test/test_hawk_guessing_game.py`.

## What the paper does

HAWK is a post-quantum signature scheme whose security rests on the (module)
**Lattice Isomorphism Problem** (LIP). The signer knows a *short, good* basis
`B` of a lattice and publishes only the **Gram matrix** `G = B* B`, which fixes
every inner product (hence every vector length) while hiding the basis itself.
Recovering any short basis `B'` with `B'* B' = G` breaks the scheme.

The attack is a **guessing game**:

1. Conjugate the public Gram matrix by a randomly sampled **short,
   lower-triangular, unimodular** matrix `U` to get `G' = U* G U`.
2. This conjugation leaves the underlying module-LIP / lattice isomorphism class
   **unchanged** — `G` and `G'` describe the *same* lattice — but it
   re-randomises an attached **nrdPIP** instance.
3. For some lucky proportion of sampled `U`, that attached instance becomes
   **easy** (solvable via the Lenstra–Silverberg algorithm plus a subfield
   descent). So you keep resampling `U` — the "guess, test, repeat" loop — until
   you land in an easy class.
4. Solve the easy instance and read off a short secret basis.

The polynomial-time claim relies on **four number-theoretic heuristics** that
the authors themselves do not (yet) verify experimentally; they are careful not
to claim HAWK is outright "broken."

## What this toy reproduces (and verifies rigorously)

The demo runs the **exact structure** of the attack over the plain integers
`Z^n` instead of over a cyclotomic ring, at dimension `n = 2..4`:

| Paper concept | Toy analog (this code) |
|---|---|
| Secret good basis `B` over a ring | Short lower-triangular **unimodular** integer matrix `B` (`hawk.random_lower_triangular_unimodular`) |
| Public key: Gram matrix `G = B* B` | `G = Bᵀ B` over `Z` (`hawk.gram`, `hawk.keygen`) |
| Re-randomise: `G' = U* G U`, `U` short lower-tri unimodular | `conjugate(G, U)` with `U` from the same family (`hawk_guessing_game.conjugate`) |
| Invariant: `G'` is the same lattice as `G` | `is_isometric_gram(G, G', U)`: checks `U` unimodular, `G' = Uᵀ G U`, `G'` symmetric, `det G' = det G` |
| Guess, test, repeat until the instance is easy | `play_guessing_game` loops sampling `U` until the oracle fires |
| Recover the secret from the easy instance | `recover_secret_from_oracle` → `B'` with `B'ᵀ B' = G` |

End to end, `play_guessing_game` recovers a basis `B'` that **exactly**
reproduces the public Gram matrix (`B'ᵀ B' == G`), i.e. a valid HAWK secret
obtained from the public key alone.

### Why the recovery is exact (not heuristic)

The oracle returns `n` independent **length-1** coordinate vectors of `G'`
(vectors `x` with `xᵀ G' x = 1`). Mapping them back through `U` gives a matrix
`X = U V` whose columns are length-1 vectors of `G`. Since `G = Bᵀ B`, a
length-1 vector satisfies `||B x|| = 1`, so `B x = ±e_k`; `n` independent such
vectors force `B X` to be a **signed permutation matrix** `P`. Hence

```
Xᵀ G X = (B X)ᵀ (B X) = Pᵀ P = I,
```

so the recovered basis `B' = X⁻¹` is unimodular and satisfies `B'ᵀ B' = G`
identically. `B'` equals the original secret up to a signed permutation of its
rows — an equally valid short secret. This is proven, not assumed.

## What is abstracted away (the research-grade machinery)

The toy deliberately does **not** implement the parts that cannot be faithfully
built — let alone *verified* — in a pure-Python teaching library, and which the
paper itself only supports under unverified heuristics:

* solving the **nrdPIP** instance,
* the **Lenstra–Silverberg** algorithm and the **subfield / cyclotomic
  descent**,
* the **four number-theoretic heuristics** underpinning the polynomial-time
  claim.

All of that collapses into the bounded `success_oracle`. Over `Z^n`, *"the
re-randomised instance is now easy"* simply means *"the lattice's length-1
vectors have small coordinates in this basis"*, which a cheap bounded search
(coordinates in `[-C, C]`) can expose. Re-randomising with `U` is exactly what
moves those short vectors into reach of the cheap search — faithfully mirroring
how the paper's conjugation moves the nrdPIP instance into an easy class.

So the **mechanism and the central invariant** are reproduced and tested; the
number-field cryptanalysis that makes the real attack work is honestly modeled
by an oracle rather than re-implemented.

## Running it

```
python -m crypto.cryptanalysis.lattice.hawk_guessing_game   # end-to-end demo
python -m unittest crypto.cryptanalysis.lattice.unit_test.test_hawk_guessing_game
```

The demo prints the toy key pair, the winning conjugator `U`, the re-randomised
Gram matrix `G'`, the verified isometry invariant, and the recovered secret
basis together with the check `B'ᵀ B' == G`.

## AI usage

I used an AI assistant to help locate the paper (the PDF host was unreachable
from my environment, so the design is based on the public abstract/summary of
ePrint 2026/1318) and to help structure the toy reduction. All mathematics here
is exact and checked by the unit tests; no claim is made to reproduce the
paper's number-field results or its heuristic polynomial-time analysis.
