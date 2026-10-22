def hitung_subtotal(harga, jumlah):
    subtotal = harga * jumlah
    return subtotal

def format_rupiah(angka):
    hasil = format(angka, ",").replace(",", ".")
    return "Rp " + hasil