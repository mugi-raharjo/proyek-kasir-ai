from database import get_data_penjualan_produk

data_produk = get_data_penjualan_produk()

print("\n===== DATA PENJUALAN PRODUK =====")

for produk in data_produk:
    print(produk)