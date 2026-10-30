from database import get_riwayat_transaksi

riwayat = get_riwayat_transaksi()

for barang in riwayat:
    print("ID Transaksi:", barang["id"])
    print("Nama Barang:", barang["nama"])
    print("Jumlah:", barang["jumlah"])
    print("Subtotal:", barang["subtotal"])
    print("----------------------")