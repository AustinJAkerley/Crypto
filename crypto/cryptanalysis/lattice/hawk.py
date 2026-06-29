# Title: Toy module-LIP / HAWK-style Key Generation
# Creator: Austin Akerley
# Date Created: 06/29/2026
# Last Editor: Austin Akerley
# Date Last Edited: 06/29/2026
# Associated Book Page Nuber: N/A

# A deliberately tiny, pure-Python caricature of the HAWK signature scheme's key
# material, used by the "guessing game" cryptanalysis demo in this folder.
#
# HAWK is built on the (module) Lattice Isomorphism Problem (LIP): the signer
# knows a *short, good* basis B of a lattice, and publishes only the Gram matrix
#     G = B^T B
# of that basis. The Gram matrix pins down all the inner products of the basis
# vectors (hence every lattice vector length) while hiding the basis itself.
# Recovering any short basis B' with B'^T B' = G breaks the scheme.
#
# This module mirrors only that *shape* of the problem over the plain integers
# Z^n instead of over a cyclotomic ring. The secret is a short unimodular
# integer matrix B (so the lattice is isometric to Z^n and has minimum 1) and
# the public key is its integer Gram matrix G. No rings, no number fields - just
# enough structure to run the attack's central mechanism end to end.

import random

from .toy_linalg import (
    transpose,
    matmul,
    identity,
    determinant,
    is_symmetric,
)

# INPUT(s) for keygen -
# n         - type: int,         desc: lattice dimension (keep small, e.g. 2-4)
# entry     - type: int,         desc: magnitude bound on the off-diagonal
#                                       entries of the secret basis (its
#                                       "shortness" - smaller is shorter)
# elementary- type: int,         desc: number of random shear/elementary factors
#                                       multiplied together to build the secret
# rng       - type: random.Random or None, desc: optional seeded RNG so the demo
#                                       and tests are reproducible


def random_unimodular(n, entry=1, elementary=4, rng=None):
    # Build a random unimodular (det = +/-1) integer matrix as a product of
    # random elementary "shear" matrices plus random row sign flips. Because
    # every factor has determinant +/-1, so does the product, and the entries
    # stay small when `entry` and `elementary` are small.
    if rng is None:
        rng = random.Random()
    if n < 1:
        raise ValueError("dimension n must be >= 1")
    M = identity(n)
    for _ in range(elementary):
        E = identity(n)
        i, j = rng.sample(range(n), 2)
        E[i][j] = rng.randint(-entry, entry)
        M = matmul(M, E)
    for i in range(n):
        if rng.random() < 0.5:
            M[i] = [-x for x in M[i]]
    return M


def random_lower_triangular_unimodular(n, bound=2, rng=None):
    # Sample a short, lower-triangular, unimodular integer matrix: the +/-1
    # diagonal forces det = +/-1 (unimodular), the zeros above the diagonal make
    # it lower-triangular, and the small strictly-lower entries make it "short".
    #
    # This is both the shape of the toy *secret* basis and the family of
    # *conjugators* used in the guessing game - matching the paper, where the
    # re-randomising conjugation is by a short lower-triangular unimodular matrix
    # tied to the module structure of the secret.
    # INPUT:  n     - type: int, desc: dimension
    #         bound - type: int, desc: magnitude bound on sub-diagonal entries
    #         rng   - type: random.Random or None
    # OUTPUT: type: matrix (n x n), desc: a short lower-triangular unimodular U
    if rng is None:
        rng = random.Random()
    U = identity(n)
    for i in range(n):
        U[i][i] = rng.choice([1, -1])
        for j in range(i):
            U[i][j] = rng.randint(-bound, bound)
    return U


def gram(B):
    # The Gram matrix G = B^T B of a basis B. This is the public key.
    # INPUT:  B - type: matrix (n x n), desc: a lattice basis (columns/rows are
    #                                          basis vectors; for B^T B the
    #                                          convention is irrelevant to the
    #                                          demo as long as it is consistent)
    # OUTPUT: type: matrix (n x n), desc: the symmetric Gram matrix G
    return matmul(transpose(B), B)


def keygen(n=3, entry=2, elementary=5, rng=None):
    # Generate a toy HAWK-style key pair.
    #
    # The secret basis is a short LOWER-TRIANGULAR unimodular matrix B. Making
    # the secret lower-triangular matches the paper's setting, where the short
    # lower-triangular unimodular conjugators used in the guessing game are the
    # natural family for re-randomising this secret's structure. The public key
    # is the Gram matrix G = B^T B, which hides B while fixing every length.
    # INPUT(s): see the parameter block above (`entry` bounds the sub-diagonal
    #           magnitude of B; `elementary` is accepted for API symmetry).
    # OUTPUT:   type: dict, with keys
    #   "secret_basis" - type: matrix, desc: the short unimodular basis B (sk)
    #   "public_gram"  - type: matrix, desc: the Gram matrix G = B^T B (pk)
    if rng is None:
        rng = random.Random()
    B = random_lower_triangular_unimodular(n, bound=entry, rng=rng)
    G = gram(B)
    return {"secret_basis": B, "public_gram": G}


def verify_keypair(B, G):
    # Sanity check that B is a valid HAWK-style secret for the public key G:
    # B must be unimodular and reproduce the Gram matrix, and G must be a
    # symmetric, determinant-1 form.
    # INPUT:  B - type: matrix, desc: candidate secret basis
    #         G - type: matrix, desc: public Gram matrix
    # OUTPUT: type: bool, desc: True iff B^T B == G, det(B) = +/-1, det(G) = 1,
    #                            and G is symmetric
    if not is_symmetric(G):
        return False
    if determinant(B) not in (1, -1):
        return False
    if determinant(G) != 1:
        return False
    return gram(B) == G

# OUTPUT - keygen returns the secret basis (sk) and public Gram matrix (pk);
# verify_keypair returns whether a recovered basis is a valid secret for G.
