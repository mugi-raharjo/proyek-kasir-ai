daftar_barang = []

def hitung_subtotal(harga, jumlah):
    subtotal = harga * jumlah
    return subtotal

def format_rupiah(angka):
    hasil = format(angka, ",").replace(",", ".")
    return "Rp " + hasil

total = 0
jawaban = "ya"

while jawaban == "ya":
    nama_barang = input("Masukan nama barang: ")
    harga = int(input("Masukan harga barang: "))
    jumlah = int(input("Masukan jumlah barang: "))

    subtotal = hitung_subtotal(harga, jumlah)
    total = total + subtotal

    barang = {
        "nama": nama_barang,
        "harga": harga,
        "jumlah": jumlah,
        "subtotal": subtotal
    }

    daftar_barang.append(barang)

    print("Subtotal barang:", format_rupiah(subtotal))

    jawaban = input("Tambah barang lagi? ")

print("\n===== STRUK BELANJA =====")

for barang in daftar_barang:
    print("Nama barang:", barang["nama"])
    print("Harga:", format_rupiah(barang["harga"]))
    print("Jumlah:", barang["jumlah"])
    print("Subtotal:", format_rupiah(barang["subtotal"]))

print("------------------------------")
print("Total belanja:", format_rupiah(total))

bayar = int(input("Masukan uang pembayaran: "))

if bayar >= total:
    kembalian = bayar - total
    print("Kembalian:", format_rupiah(kembalian))
else:
    kurang = total - bayar
    print("Uang pembayaran kurang:", format_rupiah(kurang))

print("===== TERIMA KASIH =====")