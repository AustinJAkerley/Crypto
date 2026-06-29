# Title: Tiny Exact-Integer Linear Algebra Helpers (toy scale)
# Creator: Austin Akerley
# Date Created: 06/29/2026
# Last Editor: Austin Akerley
# Date Last Edited: 06/29/2026
# Associated Book Page Nuber: N/A

# Small, dependency-free integer matrix routines used by the toy HAWK
# "guessing game" demonstration. Everything works on matrices represented as
# lists of lists of Python ints so the arithmetic is exact (no floats, no
# numpy). These are only meant for the tiny dimensions (n <= ~4) used in the
# cryptanalysis demo, so the implementations favour clarity over speed.

# A "matrix" here is a list of rows, each row a list of ints, e.g.
#   [[1, 0],
#    [2, 1]]
# A "vector" is a plain list of ints.


def identity(n):
    # INPUT:  n - type: int, desc: dimension
    # OUTPUT: type: matrix, desc: the n x n identity matrix
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def transpose(M):
    # INPUT:  M - type: matrix
    # OUTPUT: type: matrix, desc: M^T
    return [list(row) for row in zip(*M)]


def matmul(A, B):
    # INPUT:  A - type: matrix (n x m)
    #         B - type: matrix (m x p)
    # OUTPUT: type: matrix, desc: the product A*B (n x p)
    m = len(B)
    cols = len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(cols)]
            for i in range(len(A))]


def matvec(M, x):
    # INPUT:  M - type: matrix (n x n)
    #         x - type: vector (length n)
    # OUTPUT: type: vector, desc: the product M*x
    return [sum(M[i][k] * x[k] for k in range(len(x))) for i in range(len(M))]


def equal(A, B):
    # INPUT:  A, B - type: matrix
    # OUTPUT: type: bool, desc: True iff A and B have identical entries
    return A == B


def is_symmetric(M):
    # INPUT:  M - type: matrix (n x n)
    # OUTPUT: type: bool, desc: True iff M == M^T
    return M == transpose(M)


def quadratic_form(G, x):
    # Evaluate the integer quadratic form x^T G x. For a Gram matrix G = B^T B
    # this equals the squared Euclidean norm ||B x||^2 of the lattice vector
    # with coordinate vector x.
    # INPUT:  G - type: matrix (n x n), desc: (Gram) matrix of the form
    #         x - type: vector (length n), desc: integer coordinate vector
    # OUTPUT: type: int, desc: the value x^T G x
    n = len(G)
    total = 0
    for i in range(n):
        for j in range(n):
            total += x[i] * G[i][j] * x[j]
    return total


def determinant(M):
    # Exact integer determinant via Laplace cofactor expansion. Only intended
    # for the tiny matrices used in the demo.
    # INPUT:  M - type: matrix (n x n)
    # OUTPUT: type: int, desc: det(M)
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    det = 0
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        det += ((-1) ** j) * M[0][j] * determinant(minor)
    return det


def is_unimodular(M):
    # A square integer matrix is unimodular iff its determinant is +/-1; such a
    # matrix has an integer inverse and represents a lattice basis change.
    # INPUT:  M - type: matrix (n x n)
    # OUTPUT: type: bool, desc: True iff det(M) in {1, -1}
    return determinant(M) in (1, -1)


def adjugate(M):
    # The classical adjugate (transpose of the cofactor matrix). For an
    # invertible M, M^{-1} = adjugate(M) / det(M).
    # INPUT:  M - type: matrix (n x n)
    # OUTPUT: type: matrix, desc: adj(M)
    n = len(M)
    if n == 1:
        return [[1]]
    cof = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j + 1:]
                     for r, row in enumerate(M) if r != i]
            cof[i][j] = ((-1) ** (i + j)) * determinant(minor)
    return transpose(cof)


def inverse_unimodular(M):
    # Exact integer inverse of a unimodular matrix. Because det(M) = +/-1 the
    # adjugate already has integer entries and dividing by the determinant keeps
    # it integral, so the inverse is itself a unimodular integer matrix.
    # INPUT:  M - type: matrix (n x n), desc: must be unimodular
    # OUTPUT: type: matrix, desc: M^{-1}
    det = determinant(M)
    if det not in (1, -1):
        raise ValueError(
            "inverse_unimodular requires a unimodular matrix (det=+/-1), "
            "got det=" + str(det))
    adj = adjugate(M)
    return [[adj[i][j] // det for j in range(len(M))] for i in range(len(M))]
