# Title: Elliptic Curve El Gammal Cipher
# Creator: Austin Akerley
# Date Created: 12/30/2019
# Last Editor: Austin Akerley
# Date Last Edited: 01/20/2020
# Associated Book Page Number: 319

# INPUT(s) -
# E - type: curve, desc: the elliptic curve which to do the mathsss on
# P - type: tuple, desc: the shared public pointd

import random
from crypto.common.curve import curve
from crypto.common.mod_sqrt import mod_sqrt
from crypto.common.fast_power import fast_power

class ecc_el_gammal:
    def __init__(self, E, P):
        self.E = E
        self.style = ["whole point", "x only"]
        if isinstance(P, int):
            y2 = (fast_power(P, 3, self.E.modulus) + (P*self.E.A) + self.E.B) % self.E.modulus
            y = mod_sqrt(y2, self.E.modulus)[0]
            self.P = (P,mod_sqrt(y, self.E.modulus)[0])
        self.P = P

    def private_keygen(self):
        if self.E.modulus is None and self.E.modulus == 0:
            return None
        self.private_key = random.randint(1, self.E.modulus)
        print("Your Private Key: " + str(self.private_key))
        return self.private_key;

    def public_keygen(self, E = None, P = None, private_key = None, output_type = "x only"):
        if E is not None:
            self.E = E;
        if P is not None:
            if isinstance(P, int):
                y2 = (fast_power(P, 3, self.E.modulus) + (P*self.E.A) + self.E.B) % self.E.modulus
                y = mod_sqrt(y2, self.E.modulus)[0]
                self.P = (P,mod_sqrt(y, self.E.modulus)[0])
            self.P = P
        if private_key is not None:
            self.private_key = private_key;
        if None in [self.E, self.P, self.private_key]:
            return None;
        self.QA = self.E.multiply(self.P, self.private_key);
        if output_type == self.style[0]:
            return self.QA
        elif output_type == self.style[1]:
            return self.QA[0]
        else:
            print("invalid type")
            return None