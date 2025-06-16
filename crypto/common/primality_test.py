import random
from .fast_power import fast_power

def primality_test(n, certainty=40):
    if not isinstance(n, int):
        raise ValueError("n must be an int")
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(certainty):
        a = random.randrange(2, n - 1)
        x = fast_power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = fast_power(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True