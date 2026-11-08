import unittest
from fastapi.testclient import TestClient

import database

database.get_connection = database.get_test_connection

from api import app

client = TestClient(app)

class TestProdukAPI(unittest.TestCase):

    def test_get_semua_produk(self):
        response = client.get("/produk")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        produk = data[0]

        self.assertIn("id", produk)
        self.assertIn("nama", produk)
        self.assertIn("harga", produk)
        self.assertIn("stok", produk)

    def test_tambah_produk_harga_negatif(self):
        response = client.post(
            "/produk",
            json={
                "nama": "Produk Test",
                "harga": -10000,
                "stok": 5
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_tambah_produk_stok_negatif(self):
        response = client.post(
            "/produk",
            json={
                "nama": "Produk Test",
                "harga": 10000,
                "stok": -5
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_tambah_produk_nama_kosong(self):
        response = client.post(
            "/produk",
            json={
                "nama": "   ",
                "harga": 10000,
                "stok": 5
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_get_produk_tidak_ditemukan(self):
        response = client.get("/produk/99999")

        self.assertEqual(response.status_code, 404)

        data = response.json()

        self.assertEqual(
            data["detail"],
            "Produk tidak ditemukan"
        )

    def test_tambah_produk_berhasil(self):
        produk_id = None

        try:
            response = client.post(
                "/produk",
                json={
                    "nama": "Produk Testing Otomatis",
                    "harga": 10000,
                    "stok": 5
                }
            )

            self.assertEqual(response.status_code, 201)

            hasil = response.json()

            produk_id = hasil["data"]["id"]

            self.assertEqual(
                hasil["pesan"],
                "Produk berhasil ditambahkan"
            )

            self.assertEqual(
                hasil["data"]["nama"],
                "Produk Testing Otomatis"
            )

            self.assertEqual(
                hasil["data"]["harga"],
                10000
            )

            self.assertEqual(
                hasil["data"]["stok"],
                5
            )

        finally:
            if produk_id is not None:
                response_hapus = client.delete(
                    f"/produk/{produk_id}"
                )

                self.assertEqual(response_hapus.status_code, 200)

    def test_ubah_produk_berhasil(self):
        produk_id = None

        try:
            response_tambah = client.post(
                "/produk",
                json={
                    "nama": "Produk Sebelum Diubah",
                    "harga": 10000,
                    "stok": 5
                }
            )

            self.assertEqual(response_tambah.status_code, 201)

            hasil_tambah = response_tambah.json()

            produk_id = hasil_tambah["data"]["id"]

            response_ubah = client.put(
                f"/produk/{produk_id}",
                json={
                    "nama": "Produk Setelah Diubah",
                    "harga": 15000,
                    "stok": 10
                }
            )

            self.assertEqual(response_ubah.status_code, 200)

            hasil_ubah = response_ubah.json()

            self.assertEqual(
                hasil_ubah["pesan"],
                "Produk berhasil diperbarui"
            )

            self.assertEqual(
                hasil_ubah["data"]["nama"],
                "Produk Setelah Diubah"
            )

            self.assertEqual(
                hasil_ubah["data"]["harga"],
                15000
            )

            self.assertEqual(
                hasil_ubah["data"]["stok"],
                10
            )

        finally:
            if produk_id is not None:
                response_hapus = client.delete(
                    f"/produk/{produk_id}"
                )

                self.assertEqual(response_hapus.status_code, 200)

    def test_ubah_produk_tidak_ditemukan(self):
        response = client.put(
            "/produk/99999",
            json={
                "nama": "Produk Test",
                "harga": 10000,
                "stok": 5
            }
        )

        self.assertEqual(response.status_code, 404)

        data = response.json()

        self.assertEqual(
            data["detail"],
            "Produk tidak ditemukan"
        )

    def test_ubah_produk_harga_negatif(self):
        response = client.put(
            "/produk/1",
            json={
                "nama": "Buku",
                "harga": -10000,
                "stok": 5
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_ubah_produk_stok_negatif(self):
        response = client.put(
            "/produk/1",
            json={
                "nama": "Buku",
                "harga": 10000,
                "stok": -5
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_ubah_produk_nama_kosong(self):
        response = client.put(
            "/produk/1",
            json={
                "nama": "   ",
                "harga": 10000,
                "stok": 5
            }
        )

        self.assertEqual(response.status_code, 422)

    def test_hapus_produk_tidak_ditemukan(self):
        response = client.delete("/produk/999999")

        self.assertEqual(response.status_code, 404)

    def test_hapus_produk_berhasil(self):
        response_tambah = client.post(
            "/produk",
            json={
                "nama": "Produk Test Hapus",
                "harga": 5000,
                "stok": 10
            }
        )

        self.assertEqual(response_tambah.status_code, 201)

        produk_id = response_tambah.json()["data"]["id"]

        response_hapus = client.delete(f"/produk/{produk_id}")

        self.assertEqual(response_hapus.status_code, 200)

    def test_hapus_produk_yang_memiliki_transaksi(self):

        response_tambah = client.post(
            "/produk",
            json={
                "nama": "Produk Test Nonaktif",
                "harga": 5000,
                "stok": 10
            }
        )

        produk_id = response_tambah.json()["data"]["id"]

        response_transaksi = client.post(
            "/transaksi",
            json={
                "items": [
                    {
                        "produk_id": produk_id,
                        "jumlah": 1
                    }
                ],
                "uang_dibayar": 5000
            }
        )

        self.assertEqual(response_transaksi.status_code, 201)

        response_hapus = client.delete(f"/produk/{produk_id}")

        self.assertEqual(response_hapus.status_code, 200)
        self.assertEqual(response_hapus.json()["aksi"], "dinonaktifkan")

        response_produk = client.get(f"/produk/{produk_id}")

        self.assertEqual(response_produk.status_code, 200)
        self.assertEqual(response_produk.json()["aktif"], 0)

if __name__ == "__main__":
    unittest.main()