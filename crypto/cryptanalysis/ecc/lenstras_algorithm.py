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
import threading
import queue

def lenstras_algorithm(n, max_curves=2000, max_multiplies=20000):
    """
    Threaded version: Each curve gets a thread. First thread to find a factor returns it immediately.
    """
    result_queue = queue.Queue()
    stop_event = threading.Event()

    def worker(n, max_multiplies, result_queue, stop_event):
        A = random.randint(1, n-1)
        a = random.randint(1, n-1)
        b = random.randint(1, n-1)
        B = ((b*b)%n - (a*a*a)%n - A * a) % n
        E = curve(A, B, n)
        P = (a, b)
        for X in range(2, max_multiplies):
            if stop_event.is_set():
                return
            Q = E.multiply(P, X)
            P = Q
            if isinstance(Q, tuple) and len(Q) == 3 and Q[2] is not None:
                d = Q[2]
                # Only accept nontrivial factors
                if 1 < d < n and n % d == 0:
                    if not stop_event.is_set():
                        result_queue.put(d)
                        stop_event.set()
                    return
                else:
                    break

    threads = []
    for i in range(max_curves):
        t = threading.Thread(target=worker, args=(n, max_multiplies, result_queue, stop_event), daemon=True)
        t.start()
        threads.append(t)

    factor = None
    # Wait for a factor or for all threads to finish
    while True:
        try:
            factor = result_queue.get(timeout=0.1)
            break
        except queue.Empty:
            if not any(t.is_alive() for t in threads):
                break
    stop_event.set()
    for t in threads:
        if t.is_alive():
            t.join(timeout=0.1)
    if factor:
        return factor
    print("No factor found after max_curves (threaded).")
    return None  # No factor found after max_curves

# OUTPUT - type: int
# d - type: int, desc: a factor of n