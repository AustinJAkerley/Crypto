# Title: Naive Factoring Algorithm
# Creator: Austin Akerley
# Date Created: 12/25/2019
# Last Editor: Austin Akerley
# Date Last Edited: 02/03/2020
# Associated Book Page Nuber: N/A

# INPUT(s) -
# h - type: int, desc: number to try to factor
# smooth - type: int, desc: tells the program the upper limit to check if divisble by

from .list_small_primes import list_small_primes

def naive_factor(h, smooth=1000):
    prime_factors = []
    small_primes = list_small_primes(smooth)
    divisors = []
    # Compile a list of factors up to a certain smoothness then attempt to find the smallest solution to g^c % p = 1 , where c is any combination of the factors of g
    for prime in small_primes:
        while h % prime == 0:
            h = h/prime
            prime_factors.append(prime)
            new_divisors = []
            for divisor in divisors:
                new_divisor = divisor * prime
                new_divisors.append(new_divisor)
            for nd in new_divisors:
                if nd not in divisors:
                    divisors.append(nd)
            if prime not in divisors:
                divisors.append(prime)
    h = int(h)
    if h!=1:
        prime_factors.append(h)
        new_divisors = []
        for divisor in divisors:
            new_divisor = divisor * h
            new_divisors.append(new_divisor)
        divisors.append(h)
        for nd in new_divisors:
            if nd not in divisors:
                divisors.append(nd)
    prime_factors_dict = {}
    for prime_factor in prime_factors:
        if prime_factor not in prime_factors_dict:
            prime_factors_dict.update({prime_factor:1})
        else:
            prime_factors_dict[prime_factor] += 1
    return {"divisors":divisors, "prime_factors": prime_factors, "prime_factors_dict" : prime_factors_dict}
