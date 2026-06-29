# Title: HAWK "Guessing Game" Cryptanalysis - toy reproduction
# Creator: Austin Akerley
# Date Created: 06/29/2026
# Last Editor: Austin Akerley
# Date Last Edited: 06/29/2026
# Associated Book Page Nuber: N/A

# A self-contained, toy-scale reproduction of the *central mechanism* of
#     "Cryptanalysis of HAWK: a Guessing Game"
#     B. Nelson, J. Limbrey, C. Ling, A. Mendelsohn, IACR ePrint 2026/1318.
#
# The paper recovers a HAWK secret key by repeatedly *re-randomising* the public
# Gram matrix:
#
#   * conjugate the public Gram matrix G by a randomly sampled short,
#     lower-triangular unimodular matrix U to get   G' = U^* G U ;
#   * this conjugation leaves the underlying module-LIP / lattice isomorphism
#     class UNCHANGED (G and G' describe the very same lattice) - it only
#     re-randomises an attached "nrdPIP" instance;
#   * for some lucky proportion of the sampled U the attached problem becomes
#     EASY, so the attacker plays a guessing game: keep resampling U until the
#     instance lands in an easy class, then solve it and read off a short secret
#     basis.
#
# What is faithfully reproduced here (and rigorously checked):
#   * the conjugation move G' = U^T G U with U short, lower-triangular, unimodular
#   * the invariant that G' is an isometric Gram matrix of the SAME lattice
#   * the "guess, test, repeat" loop driven by a cheap success oracle
#   * end-to-end recovery of a valid secret basis B' with B'^T B' == G.
#
# What is abstracted away (the genuinely research-grade, number-field machinery
# that cannot be faithfully implemented - let alone verified - here):
#   * solving the nrdPIP instance via the Lenstra-Silverberg algorithm
#   * the subfield / cyclotomic descent
#   * the four number-theoretic heuristics the paper's polynomial-time claim
#     rests on (which the authors themselves do not yet verify experimentally).
# All of that is collapsed into the bounded short-vector `success_oracle` below:
# over Z^n "the instance is easy" simply means "the lattice's length-1 vectors
# have small coordinates in this basis", which a cheap bounded search can find.
# Re-randomising with U is exactly what moves those short vectors into reach.

import random
import itertools

from .toy_linalg import (
    transpose,
    matmul,
    determinant,
    quadratic_form,
    inverse_unimodular,
    is_symmetric,
)
from .hawk import (
    keygen,
    gram,
    verify_keypair,
    random_lower_triangular_unimodular,
)


def conjugate(G, U):
    # The core re-randomisation move: G' = U^T G U.
    # INPUT:  G - type: matrix, desc: a Gram matrix
    #         U - type: matrix, desc: a unimodular basis change
    # OUTPUT: type: matrix, desc: the conjugated Gram matrix G'
    return matmul(matmul(transpose(U), G), U)


def is_isometric_gram(G, G_prime, U):
    # Rigorously verify the paper's central invariant for the toy setting: that
    # G' is an isometric Gram matrix of the SAME lattice as G, exhibited by the
    # explicit unimodular change of basis U. Concretely we check that
    #   * U is unimodular (a genuine basis change of the same lattice),
    #   * G' = U^T G U exactly,
    #   * G' is symmetric and has the same determinant as G
    #     (an isometry invariant).
    # INPUT:  G, G_prime - type: matrix, desc: the two Gram matrices
    #         U          - type: matrix, desc: the claimed unimodular conjugator
    # OUTPUT: type: bool, desc: True iff all invariant checks pass
    if determinant(U) not in (1, -1):
        return False
    if conjugate(G, U) != G_prime:
        return False
    if not is_symmetric(G_prime):
        return False
    if determinant(G_prime) != determinant(G):
        return False
    return True


def success_oracle(G_prime, search_bound=2):
    # The cheap "is this instance easy now?" test that stands in for solving the
    # nrdPIP instance. It brute-forces all integer coordinate vectors with
    # entries in [-search_bound, search_bound] and collects the lattice's
    # length-1 vectors (those with x^T G' x == 1). The instance counts as EASY
    # iff this cheap, bounded search already exposes n linearly independent
    # length-1 vectors - i.e. a full set of shortest vectors with small
    # coordinates in the current basis.
    #
    # INPUT:  G_prime      - type: matrix (n x n), desc: conjugated Gram matrix
    #         search_bound - type: int, desc: the cheap coordinate budget C
    # OUTPUT: type: matrix (n x n) or None, desc: on success, a matrix V whose
    #         COLUMNS are n independent length-1 coordinate vectors of G'; None
    #         if the bounded search did not expose a full set (instance not easy)
    n = len(G_prime)
    found = []
    for coords in itertools.product(range(-search_bound, search_bound + 1),
                                    repeat=n):
        x = list(coords)
        if quadratic_form(G_prime, x) == 1:
            if _extends_independent_set(found, x):
                found.append(x)
                if len(found) == n:
                    return transpose(found)  # columns = the length-1 vectors
    return None


def _extends_independent_set(rows, candidate):
    # Helper: True iff appending `candidate` to the list of integer row vectors
    # `rows` keeps them linearly independent over the rationals. Uses exact
    # fraction-free style Gaussian elimination via Python's Fraction so there is
    # no floating point error at these tiny sizes.
    from fractions import Fraction
    matrix = [[Fraction(v) for v in r] for r in rows] + \
             [[Fraction(v) for v in candidate]]
    pivot_row = 0
    cols = len(matrix[0])
    for col in range(cols):
        pivot = None
        for r in range(pivot_row, len(matrix)):
            if matrix[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pv = matrix[pivot_row][col]
        matrix[pivot_row] = [v / pv for v in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][col] != 0:
                factor = matrix[r][col]
                matrix[r] = [a - factor * b
                             for a, b in zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row == len(matrix)


def recover_secret_from_oracle(U, V):
    # Turn a successful oracle hit into a recovered HAWK secret basis.
    #
    # The oracle found V, whose columns are length-1 vectors of G' = U^T G U.
    # Mapping them back through U gives X = U V whose columns are length-1
    # vectors of the ORIGINAL public form G. Writing G = B^T B, a length-1
    # vector x satisfies ||B x|| = 1, i.e. B x = +/- e_k; n independent such
    # vectors force B X to be a signed permutation matrix P, hence
    #     X^T G X = (B X)^T (B X) = P^T P = I.
    # Therefore the recovered basis B' = X^{-1} is unimodular and satisfies
    #     B'^T B' = (X^{-1})^T X^{-1} = (X X^T)^{-1}... = G,
    # i.e. B' is a valid short secret for the public key G (it equals the
    # original secret up to a signed permutation of its rows).
    #
    # INPUT:  U - type: matrix, desc: the winning conjugator
    #         V - type: matrix, desc: oracle output (length-1 vectors of G')
    # OUTPUT: type: matrix, desc: a recovered secret basis B' with B'^T B' = G
    X = matmul(U, V)
    return inverse_unimodular(X)


def play_guessing_game(G, search_bound=2, conjugator_bound=3,
                       max_tries=20000, rng=None):
    # Run the full attack against a public Gram matrix G: keep sampling short
    # lower-triangular unimodular conjugators U, form G' = U^T G U, and ask the
    # success oracle whether the re-randomised instance is now easy. As soon as
    # it is, recover and return a valid secret basis.
    #
    # INPUT:  G               - type: matrix, desc: the public key (Gram matrix)
    #         search_bound    - type: int, desc: oracle coordinate budget C
    #         conjugator_bound- type: int, desc: sub-diagonal bound for U
    #         max_tries       - type: int, desc: cap on guesses before giving up
    #         rng             - type: random.Random or None
    # OUTPUT: type: dict, with keys
    #   "recovered_basis" - type: matrix or None, desc: recovered secret B'
    #   "tries"           - type: int, desc: number of conjugators sampled
    #   "winning_U"       - type: matrix or None, desc: the conjugator that won
    #   "success"         - type: bool
    if rng is None:
        rng = random.Random()
    n = len(G)
    for attempt in range(1, max_tries + 1):
        U = random_lower_triangular_unimodular(n, bound=conjugator_bound,
                                               rng=rng)
        G_prime = conjugate(G, U)
        V = success_oracle(G_prime, search_bound=search_bound)
        if V is not None:
            B_recovered = recover_secret_from_oracle(U, V)
            return {
                "recovered_basis": B_recovered,
                "tries": attempt,
                "winning_U": U,
                "success": True,
            }
    return {
        "recovered_basis": None,
        "tries": max_tries,
        "winning_U": None,
        "success": False,
    }


def _demo():
    # Self-contained demonstration: generate a toy HAWK key pair, then recover a
    # valid secret from the public Gram matrix alone via the guessing game.
    rng = random.Random(2026)
    key = keygen(n=3, entry=2, elementary=5, rng=rng)
    B, G = key["secret_basis"], key["public_gram"]

    print("Toy HAWK key pair (paper: ePrint 2026/1318)")
    print("  secret basis B (sk):", B)
    print("  public Gram  G (pk):", G)
    print("  check  B^T B == G :", gram(B) == G)

    result = play_guessing_game(G, search_bound=2, conjugator_bound=3,
                                rng=rng)
    if not result["success"]:
        print("\nGuessing game did not converge within the try budget.")
        return

    B_rec = result["recovered_basis"]
    U = result["winning_U"]
    G_prime = conjugate(G, U)

    print("\nGuessing game won after", result["tries"], "conjugation(s).")
    print("  winning short lower-tri unimodular U:", U)
    print("  re-randomised Gram G' = U^T G U      :", G_prime)
    print("  invariant: G' isometric to G via U   :",
          is_isometric_gram(G, G_prime, U))
    print("  recovered secret basis B'            :", B_rec)
    print("  recovered B' reproduces G (B'^T B'=G):", gram(B_rec) == G)
    print("  recovered B' is a valid HAWK secret  :", verify_keypair(B_rec, G))


if __name__ == "__main__":
    _demo()

# OUTPUT - play_guessing_game returns a recovered secret basis B' (and the
# winning conjugator U and try count). B' satisfies B'^T B' == G, so it is a
# valid HAWK secret recovered from the public key alone, reproducing - at toy
# scale - the structure of the ePrint 2026/1318 attack.
