# Title: El-Gammal Cipher
# Creator: Austin Akerley
# Date Created: 11/26/2019
# Last Editor: Austin Akerley
# Date Last Edited: 01/20/2020
# Associated Book Page Nuber: 70

# INPUT(s) -
# g - type: int, desc: generator
# private_key - type: int, desc: my private key
# modulus - type: int, desc: the modulus
# public key - type: int, desc: the other persons public key
# cipher_text_1 - type: int, desc: the first cipher text block from the other person
# cipher_text_2 - type: int, desc: the second cipher text block from the other person

import random
from crypto.common.fast_power import fast_power
from crypto.common.mod_inv import mod_inv

class el_gammal:
    def __init__(self, g=None, private_key=None, modulus=None, public_key=None, cipher_text_1=None, cipher_text_2=None):
        if g is not None:
            self.set_g(g)
        if modulus is not None:
            self.set_modulus(modulus)
        if private_key is not None:
            self.set_private_key(private_key)
        if public_key is not None:
            self.set_public_key(public_key)
        if cipher_text_1 is not None:
            self.set_cipher_text_1(cipher_text_1)
        if cipher_text_2 is not None:
            self.set_cipher_text_2(cipher_text_2)

    def set_g(self, g):
        self.g=g

    def set_modulus(self, modulus):
        self.modulus = modulus

    def set_private_key(self, private_key):
        self.private_key = private_key

    def set_public_key(self, public_key):
        self.public_key = public_key

    def set_cipher_text_1(self, cipher_text_1):
        self.cipher_text_1 = cipher_text_1

    def set_cipher_text_2(self, cipher_text_2):
        self.cipher_text_2 = cipher_text_2

    def gen_public_key(self):
        # Returns g^a mod p, where a is the private key
        return fast_power(self.g, self.private_key, self.modulus)

    def encrypt(self, message, k=None):
        # Encrypts the message using the recipient's public key
        if self.public_key is None:
            raise ValueError("Public key must be set for encryption.")
        if k is None:
            k = random.randint(1, self.modulus - 2)
        c1 = fast_power(self.g, k, self.modulus)
        c2 = (message * fast_power(self.public_key, k, self.modulus)) % self.modulus
        return [c1, c2]

    def decrypt(self, cipher_text_1, cipher_text_2):
        # Decrypts the ciphertext using the private key
        if self.private_key is None:
            raise ValueError("Private key must be set for decryption.")
        s = fast_power(cipher_text_1, self.private_key, self.modulus)
        s_inv = mod_inv(s, self.modulus)
        message = (cipher_text_2 * s_inv) % self.modulus
        return message