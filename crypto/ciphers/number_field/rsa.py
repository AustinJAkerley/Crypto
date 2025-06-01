# Title: RSA Public Key Encryption
# Creator: Austin Akerley
# Date Created: 03/07/2020
# Last Editor: Austin Akerley
# Date Last Edited: 04/19/2020
# Associated Book Page Nuber: 123

from crypto.common.fast_power import fast_power
from crypto.common.eea import eea
from crypto.common.mod_inv import mod_inv
import random

class rsa:
    def __init__(self, p = None, q = None, e = None, N = None):
        self.p = p
        self.q = q
        self.e = e
        self.N = N
        if None not in [self.p, self.q] and N is None:
            self.N = p * q

    def set_p(self, p):
        self.p = p

    def set_q(self, q):
        self.q = q

    def set_N(self, N):
        self.N = N

    def gen_e(self, p = None, q = None):
        if (p is not None):
            self.p = p
        if (q is not None):
            self.q = q
        if self.p is None or self.q is None:
            raise ValueError("p and q must be set before generating e")
        phi = (self.p - 1) * (self.q - 1)
        while True:
            e = random.randint(3, phi - 1)
            if eea(e, phi).get("gcd") == 1:
                break
        self.e = e
        return e

    def set_e(self, e):
        if self.q is None or self.p is None:
            raise ValueError("(self.) p and q cannot be None")
        if eea(e, (self.p-1)*(self.q-1)).get("gcd") == 1:
            self.e = e
        else:
            raise ValueError("Invalid e value, gcd of input e and (p-1)*(q-1) must be 1")

    def encrypt(self, m, N=None, e=None):
        # Encrypt message m with public key (N, e)
        if N is not None:
            self.N = N
        if e is not None:
            self.e = e
        if self.N is None or self.e is None:
            raise ValueError("N and e must be set before encryption")
        return fast_power(m, self.e, self.N)

    def decrypt(self, c, p=None, q=None, e=None):
        # Decrypt ciphertext c with private key (p, q, e)
        if p is not None:
            self.p = p
        if q is not None:
            self.q = q
        if e is not None:
            self.e = e
        if self.p is None or self.q is None or self.e is None:
            raise ValueError("p, q, and e must be set before decryption")
        self.N = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)
        d = mod_inv(self.e, phi)
        self.d = d
        return fast_power(c, d, self.N)

    def publish_public_info(self):
        print("e: " + str(self.e) + " | N: " + str(self.N))
        return {"e": self.e, "N": self.N}