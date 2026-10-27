def hitung_subtotal(harga, jumlah):
    if harga <= 0:
        raise ValueError("Harga harus lebih dari 0!")

    if jumlah <= 0:
        raise ValueError("Jumlah harus lebih dari 0!")

    subtotal = harga * jumlah
    return subtotal

def format_rupiah(angka):
    hasil = format(angka, ",").replace(",", ".")
    return "Rp " + hasil