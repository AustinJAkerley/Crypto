# Title: Elliptic Curve
# Creator: Austin Akerley
# Date Created: 12/25/2019
# Last Editor: Austin Akerley
# Date Last Edited: 01/20/2020
# Associated Book Page Nuber: 299

# INPUT(s) -
# A - type: int, desc: coefficent of x
# B - type: int, desc: constant for the curve
# modulus - type: int, desc: modulus for the curve that defines the field it's in

import random
from math import log2
from crypto.common.mod_inv import mod_inv
from crypto.common.fast_power import fast_power
from crypto.common.mod_sqrt import mod_sqrt

class curve:
    def __init__(self, A, B, modulus): # Curve is of the mathematical form: y^2 = x^3 + A*x + B
        self.A = A
        self.B = B
        self.modulus = modulus
        self.divisor = None
        self.l = int(modulus.bit_length() / 2)
        self.max_msg = 0
        for _ in range(0, self.l):
            self.max_msg = (self.max_msg << 1) | 1

    def slope(self, P, Q): # Where P and Q are tuples
        if P == Q:
            inv_2y_p = mod_inv((2*P[1]) % self.modulus, self.modulus)
            if isinstance(inv_2y_p, tuple):
                d = inv_2y_p[1]
                return [None, None, d]
            slope = ((3*P[0]*P[0] + self.A) * inv_2y_p) % self.modulus
            return slope
        else:
            y_diff = (P[1]-Q[1])%self.modulus
            x_diff = (P[0]-Q[0])%self.modulus
            inv_x_diff  = mod_inv(x_diff, self.modulus)
            if isinstance(inv_x_diff,tuple):
                d = inv_x_diff[1]
                return [None, None, d]
            slope = (y_diff * inv_x_diff)%self.modulus
            return slope

    def add(self, P, Q): # Where P and Q are tuples
        if P[0] is None and P[1] is None:
            return Q
        if Q[0] is None and Q[1] is None:
            return P

        slope = self.slope(P, Q)

        if slope == [None, None, None]:
            return (None, None)

        x_r = (slope * slope - P[0] - Q[0]) % self.modulus
        y_r = (slope * (P[0] - x_r) - P[1]) % self.modulus

        return (x_r, y_r)

    def double_and_add(self, P, n): # P is a point on the curve, n is an integer
        R = (None, None) # Represents the point at infinity
        addend = P

        while n:
            if n & 1:
                R = self.add(R, addend)
            addend = self.add(addend, addend)
            n >>= 1

        return R
    
    def multiply(self, P, n):
        return self.double_and_add(P, n)

    def encrypt(self, plaintext, pubkey): # plaintext is an integer, pubkey is a tuple (x, y)
        k = random.randint(1, self.modulus-1)
        R = self.double_and_add(self.base_point(), k)
        S = (plaintext * pow(pubkey[0], k, self.modulus)) % self.modulus

        return (R, S)

    def decrypt(self, ciphertext, privkey): # ciphertext is a tuple (R, S), privkey is an integer
        R, S = ciphertext
        x_r, y_r = R
        S_prime = (S * pow(x_r, privkey, self.modulus)) % self.modulus

        return S_prime

    def base_point(self): # Returns a base point on the curve
        x = 2
        while True:
            y_squared = (x*x*x + self.A*x + self.B) % self.modulus
            y = mod_sqrt(y_squared, self.modulus)
            if y != None:
                return (x, y)
            x += 1

    def is_point_on_curve(self, P):
        if P[0] is None or P[1] is None:
            return False
        x, y = P
        return (y * y) % self.modulus == (x * x * x + self.A * x + self.B) % self.modulus

    def __repr__(self):
        return f"Curve: y^2 = x^3 + {self.A}x + {self.B} mod {self.modulus}"