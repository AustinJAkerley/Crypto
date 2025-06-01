# Title: Lenstras Factorization Algorithm
# Creator: Austin Akerley
# Date Created: 12/31/2019
# Last Editor: Austin Akerley
# Date Last Edited: 01/20/2020
# Associated Book Page Nuber: 329

# INPUT(s) -
# n - type: int, desc: composite number where n = p*q, where p and q are both primes

import random
from math import sqrt
from math import log2
from crypto.common.curve import curve
from crypto.common.mod_inv import mod_inv

def lenstras_algorithm(n, max_curves=2000, max_multiplies=20000): # n is a composite number of two large primes, p and q ; n = p*q
    for i in range(max_curves):
        A = random.randint(1, n-1)
        a = random.randint(1, n-1)
        b = random.randint(1, n-1)
        B = ((b*b)%n - (a*a*a)%n - A * a) % n
        E = curve(A, B, n)
        P = (a, b)
        for X in range(2, max_multiplies):
            Q = E.multiply(P, X)
            P = Q
            if isinstance(Q, tuple) and len(Q) == 3 and Q[2] is not None:
                d = Q[2]
                print(f"Found factor in multiply: d={d}")
                # Only accept nontrivial factors
                if 1 < d < n and n % d == 0:
                    return d
                # If d is trivial, break to try a new curve
                else:
                    break
    print("No factor found after max_curves.")
    return None  # No factor found after max_curves

# OUTPUT - type: int
# d - type: int, desc: a factor of n