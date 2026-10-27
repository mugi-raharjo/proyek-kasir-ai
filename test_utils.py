from utils import hitung_subtotal, format_rupiah

assert hitung_subtotal(10000, 2) == 20000
assert hitung_subtotal(15000, 3) == 45000
assert hitung_subtotal(5000, 1) == 5000

assert format_rupiah(26000) == "Rp 26.000"

try:
    hitung_subtotal(10000, 0)
except ValueError:
    pass
else:
    raise AssertionError("Jumlah nol seharusnya ditolak!")

try:
    hitung_subtotal(0, 2)
except ValueError:
    pass
else:
    raise AssertionError("Harga nol seharusnya ditolak!")

try:
    hitung_subtotal(10000, -2)
except ValueError:
    pass
else:
    raise AssertionError("Jumlah negatif seharusnya ditolak!")

print("Semua pengujian berhasil!")