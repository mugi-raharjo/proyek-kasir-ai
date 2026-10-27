from utils import hitung_subtotal, format_rupiah

def tampilkan_struk(daftar_barang, total):
    print("\n===== STRUK BELANJA =====")

    for barang in daftar_barang:
        print("Nama barang:", barang["nama"])
        print("Harga:", format_rupiah(barang["harga"]))
        print("Jumlah:", barang["jumlah"])
        print("Subtotal:", format_rupiah(barang["subtotal"]))

    print("--------------------------------")
    print("Total belanja:", format_rupiah(total))

def proses_pembayaran(total):
    uang_diterima = 0

    while uang_diterima < total:
        bayar = input_angka("Masukkan pembayaran: ")
        uang_diterima = uang_diterima + bayar

        if uang_diterima < total:
            kurang = total - uang_diterima
            print("Uang pembayaran masih kurang:", format_rupiah(kurang))
        else:
            kembalian = uang_diterima - total
            print("Kembalian:", format_rupiah(kembalian))

def input_angka(pesan):
    while True:
        try:
            angka = int(input(pesan))

            if angka > 0:
                return angka
            else:
                print("Angka harus lebih dari 0!")

        except ValueError:
            print("Input harus berupa angka! Coba lagi.")

def input_barang():
    while True:
        nama_barang = input("Masukan nama barang: ").strip()

        if nama_barang != "":
            break
        else:
            print("Nama tidak boleh kosong!")

    harga = input_angka("Masukan harga barang: ")
    jumlah = input_angka("Masukan jumlah barang: ")

    subtotal = hitung_subtotal(harga, jumlah)

    barang = {
        "nama": nama_barang,
        "harga": harga,
        "jumlah": jumlah,
        "subtotal": subtotal
    }

    return barang

def main():
    daftar_barang = []

    total = 0
    jawaban = "ya"

    while jawaban == "ya":
        barang = input_barang()

        subtotal = barang["subtotal"]
        total = total + subtotal

        daftar_barang.append(barang)

        print("Subtotal barang:", format_rupiah(subtotal))

        while True:
            jawaban = input("Tambah barang lagi? ").strip().lower()

            if jawaban == "ya" or jawaban == "tidak":
                break

            print("Jawaban harus berupa ya atau tidak!")

    tampilkan_struk(daftar_barang, total)

    proses_pembayaran(total)

    print("===== TERIMA KASIH =====")

if __name__ == "__main__":
    main()