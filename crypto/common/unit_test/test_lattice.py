#!/usr/bin/python3
# Title: Unit Test for Lattice
# Creator: Austin Akerley
# Date Created: 06/01/2025
# Associated Book Page Number: TBD

import unittest
import numpy as np
from crypto.common.lattice import lattice

class TestLattice(unittest.TestCase):
    """
    Unit tests for the lattice class.
    """
    def test_lattice_init_with_basis(self):
        """
        Test initialization with a given basis matrix.
        """
        basis = [[1, 0], [0, 1]]
        L = lattice(basis_matrix=basis)
        np.testing.assert_array_equal(L.get_basis(), np.array(basis))
        self.assertEqual(L.dimension, 2)
        self.assertEqual(L.rank, 2)

    def test_lattice_init_with_n_q(self):
        """
        Test initialization with random basis using n and q.
        """
        n = 4
        q = 17
        L = lattice(n=n, q=q)
        basis = L.get_basis()
        self.assertEqual(basis.shape, (n, n))
        self.assertTrue(np.all((basis >= 0) & (basis < q)))
        self.assertEqual(L.dimension, n)
        self.assertEqual(L.rank, n)

    def test_lattice_init_and_get_basis(self):
        """
        Test get_basis method and dimension/rank properties.
        """
        basis = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        L = lattice(basis_matrix=basis)
        np.testing.assert_array_equal(L.get_basis(), np.array(basis))
        self.assertEqual(L.dimension, 3)
        self.assertEqual(L.rank, 3)

    def test_lattice_add_vectors(self):
        """
        Test vector addition.
        """
        L = lattice([[1, 0], [0, 1]])
        v1 = np.array([1, 2])
        v2 = np.array([3, 4])
        result = L.add_vectors(v1, v2)
        np.testing.assert_array_equal(result, np.array([4, 6]))

    def test_lattice_scalar_mult(self):
        """
        Test scalar multiplication.
        """
        L = lattice([[1, 0], [0, 1]])
        v = np.array([2, 3])
        result = L.scalar_mult(5, v)
        np.testing.assert_array_equal(result, np.array([10, 15]))

    def test_lattice_lattice_vector(self):
        """
        Test lattice vector generation (integer linear combination).
        """
        basis = [[2, 1], [1, 3]]
        L = lattice(basis_matrix=basis)
        coeffs = [4, 5]
        # 4*[2,1] + 5*[1,3] = [8+5, 4+15] = [13, 19]
        result = L.lattice_vector(coeffs)
        np.testing.assert_array_equal(result, np.array([13, 19]))

    def test_encode_decode_message(self):
        """
        Test encoding and decoding of messages to/from bit arrays.
        """
        # Test encoding and decoding a string
        msg = "hello"
        n = 40  # 5 bytes * 8 bits = 40 bits
        bits = lattice.encode(msg, n)
        self.assertEqual(len(bits), n)
        decoded = lattice.decode(bits)
        self.assertEqual(decoded, msg)

        # Test encoding and decoding bytes
        msg_bytes = b"test"
        n = 32  # 4 bytes * 8 bits = 32 bits
        bits = lattice.encode(msg_bytes, n)
        self.assertEqual(len(bits), n)
        decoded = lattice.decode(bits)
        self.assertEqual(decoded, msg_bytes.decode('utf-8'))

        # Test padding
        msg_short = "a"
        n = 24  # 1 byte * 8 bits = 8 bits, pad to 24
        bits = lattice.encode(msg_short, n)
        self.assertEqual(len(bits), n)
        decoded = lattice.decode(bits)
        self.assertTrue(decoded.startswith("a"))

if __name__ == '__main__':
    unittest.main()
