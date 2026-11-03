import unittest

from utils import hitung_subtotal, format_rupiah


class TestUtils(unittest.TestCase):

    def test_hitung_subtotal(self):
        self.assertEqual(hitung_subtotal(10000, 2), 20000)
        self.assertEqual(hitung_subtotal(15000, 3), 45000)
        self.assertEqual(hitung_subtotal(5000, 1), 5000)

    def test_format_rupiah(self):
        self.assertEqual(format_rupiah(26000), "Rp 26.000")

    def test_jumlah_nol(self):
        with self.assertRaises(ValueError):
            hitung_subtotal(10000, 0)

    def test_harga_nol(self):
        with self.assertRaises(ValueError):
            hitung_subtotal(0, 2)

    def test_jumlah_negatif(self):
        with self.assertRaises(ValueError):
            hitung_subtotal(10000, -2)


if __name__ == "__main__":
    unittest.main()