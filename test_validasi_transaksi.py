from database import simpan_transaksi

daftar_barang = [
    {
        #"produk_id": 1,
        "nama": "Buku",
        "harga": 10000,
        "jumlah": 2,
        "subtotal": 20000
    },
    {
        "produk_id": 2,
        "nama": "Pensil",
        "harga": 3000,
        "jumlah": 3,
        "subtotal": 9000
    }
]

try:
    simpan_transaksi(
        daftar_barang,
        total=29000,
        uang_diterima=30000,
        kembalian=1000
    )

except ValueError as error:
    print("Validasi berhasil menangkap kesalahan:")
    print(error)