# Title: Jacobi Symbol
# Creator: Austin Akerley
# Date Created: 11/26/2019
# Last Editor: Austin Akerley
# Date Last Edited: 02/09/2020
# Associated Book Page Nuber: 28

# INPUT(s) -
# a - type: int, desc: numerator
# n - type: int, desc: denominator (must be odd and > 0)

from .fast_power import fast_power

def jacobi_symbol(a, n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    if n == 1:
        return result
    else:
        return 0