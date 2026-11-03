from unittest.mock import MagicMock, patch
from database import simpan_transaksi


daftar_barang = [
    {
        "produk_id": 1,
        "nama": "Buku",
        "harga": 10000,
        "jumlah": 2,
        "subtotal": 20000
    }
]


def uji_harga_berubah():
    koneksi_mock = MagicMock()
    cursor_mock = koneksi_mock.cursor.return_value


    cursor_mock.fetchone.return_value = (12000, 9)

    with patch("database.get_connection", return_value=koneksi_mock):
        try:
            simpan_transaksi(
                daftar_barang,
                total=20000,
                uang_diterima=25000,
                kembalian=5000
            )

        except ValueError as error:
            print("Pengujian harga berhasil:")
            print(error)

        else:
            raise AssertionError("Harga berbeda seharusnya ditolak.")

    koneksi_mock.rollback.assert_called_once()
    koneksi_mock.commit.assert_not_called()


def uji_stok_tidak_cukup():
    koneksi_mock = MagicMock()
    cursor_mock = koneksi_mock.cursor.return_value


    cursor_mock.fetchone.return_value = (10000, 1)

    with patch("database.get_connection", return_value=koneksi_mock):
        try:
            simpan_transaksi(
                daftar_barang,
                total=20000,
                uang_diterima=25000,
                kembalian=5000
            )

        except ValueError as error:
            print("Pengujian stok berhasil:")
            print(error)

        else:
            raise AssertionError("Stok tidak cukup seharusnya ditolak.")

    koneksi_mock.rollback.assert_called_once()
    koneksi_mock.commit.assert_not_called()


def uji_rollback_detail_transaksi():
    koneksi_mock = MagicMock()
    cursor_mock = koneksi_mock.cursor.return_value


    cursor_mock.fetchone.return_value = (10000, 9)


    cursor_mock.execute.side_effect = [
        None,
        None,
        None,
        Exception("Gagal menyimpan detail transaksi.")
    ]

    with patch("database.get_connection", return_value=koneksi_mock):
        try:
            simpan_transaksi(
                daftar_barang,
                total=20000,
                uang_diterima=25000,
                kembalian=5000
            )

        except Exception as error:
            print("Pengujian rollback berhasil:")
            print(error)

        else:
            raise AssertionError("Seharusnya terjadi error.")

    koneksi_mock.rollback.assert_called_once()
    koneksi_mock.commit.assert_not_called()
    cursor_mock.close.assert_called_once()
    koneksi_mock.close.assert_called_once()


uji_harga_berubah()
uji_stok_tidak_cukup()
uji_rollback_detail_transaksi()