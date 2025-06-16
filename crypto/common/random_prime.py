import os
from .primality_test import primality_test

def random_prime(bits):
    while True:
        random_bytes = os.urandom((bits + 7) // 8)
        candidate = int.from_bytes(random_bytes, 'big') | (1 << (bits - 1)) | 1
        if primality_test(candidate): return candidate