from database import get_products

daftar_produk = get_products()

for produk in daftar_produk:
    print(
        produk["id"],
        produk["nama"],
        produk["harga"],
        produk["stok"]
    )