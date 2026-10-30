from utils import hitung_subtotal, format_rupiah
from database import (
    get_products,
    simpan_transaksi,
    get_riwayat_transaksi,
    get_detail_transaksi
)

def tampilkan_struk(daftar_barang, total):
    print("\n===== STRUK BELANJA =====")

    for barang in daftar_barang:
        print("Nama barang:", barang["nama"])
        print("Harga:", format_rupiah(barang["harga"]))
        print("Jumlah:", barang["jumlah"])
        print("Subtotal:", format_rupiah(barang["subtotal"]))

    print("--------------------------------")
    print("Total belanja:", format_rupiah(total))

def tampilkan_riwayat_transaksi():
    riwayat = get_riwayat_transaksi()

    print("\n===== RIWAYAT TRANSAKSI =====")

    if not riwayat:
        print("Belum ada transaksi.")
        return

    id_transaksi_sebelumnya = None

    for barang in riwayat:
        if barang["id"] != id_transaksi_sebelumnya:
            if id_transaksi_sebelumnya is not None:
                print("================================")

            print("ID Transaksi:", barang["id"])
            print("Tanggal:", barang["tanggal"])

            print(
                "Total Transaksi:",
                format_rupiah(barang["total"])
            )
            print(
                "Uang Diterima:",
                format_rupiah(barang["uang_diterima"])
            )
            print(
                "Kembalian:",
                format_rupiah(barang["kembalian"])
            )

            id_transaksi_sebelumnya = barang["id"]

        print("Nama Barang:", barang["nama"])
        print("Harga:", format_rupiah(barang["harga"]))
        print("Jumlah:", barang["jumlah"])
        print("Subtotal:", format_rupiah(barang["subtotal"]))
        print("--------------------------------")


def tampilkan_detail_transaksi():
    id_transaksi = input_angka("Masukkan ID transaksi: ")

    detail = get_detail_transaksi(id_transaksi)

    if not detail:
        print("Transaksi tidak ditemukan.")
        return

    transaksi = detail[0]

    print("\n===== DETAIL TRANSAKSI =====")
    print("ID Transaksi:", transaksi["id"])
    print("Tanggal:", transaksi["tanggal"])
    print("Total:", format_rupiah(transaksi["total"]))
    print("Uang Diterima:", format_rupiah(transaksi["uang_diterima"]))
    print("Kembalian:", format_rupiah(transaksi["kembalian"]))
    print("--------------------------------")

    for barang in detail:
        print("Nama Barang:", barang["nama"])
        print("Harga:", format_rupiah(barang["harga"]))
        print("Jumlah:", barang["jumlah"])
        print("Subtotal:", format_rupiah(barang["subtotal"]))
        print("--------------------------------")


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

def input_angka_atau_batal(pesan):
    while True:
        masukan = input(pesan).strip()

        if masukan.lower() == "batal":
            return None

        try:
            angka = int(masukan)

            if angka > 0:
                return angka
            else:
                print("Angka harus lebih dari 0!")

        except ValueError:
            print("Input harus berupa angka atau ketik 'batal'.")


def proses_pembayaran(total):
    while True:
        uang_diterima = input_angka_atau_batal(
            "Masukkan uang pembayaran (atau ketik 'batal'): Rp "
        )

        if uang_diterima is None:
            return None

        if uang_diterima >= total:
            kembalian = uang_diterima - total

            print("Kembalian:", format_rupiah(kembalian))

            return uang_diterima, kembalian

        else:
            kekurangan = total - uang_diterima

            print(
                "Uang belum cukup. Kekurangan:",
                format_rupiah(kekurangan)
            )


def input_barang(daftar_barang):
    daftar_produk = get_products()

    print("\n ===== DAFTAR PRODUK =====")

    for produk in daftar_produk:
        print(
            "ID:", produk["id"],
            "| Nama:", produk["nama"],
            "| Harga:", format_rupiah(produk["harga"]),
            "| Stok:", produk["stok"]
        )

    while True:
        id_produk = input_angka_atau_batal("Pilih ID produk: ")

        if id_produk is None:
            return "batal"

        produk_dipilih = None

        for produk in daftar_produk:
            if produk["id"] == id_produk:
                produk_dipilih = produk
                break

        if produk_dipilih is not None:
            break

        print("ID produk tidak ditemukan!")

    jumlah_di_keranjang = 0

    for barang_lama in daftar_barang:
        if barang_lama["produk_id"] == produk_dipilih["id"]:
            jumlah_di_keranjang += barang_lama["jumlah"]

    stok_tersedia = produk_dipilih["stok"] - jumlah_di_keranjang

    if stok_tersedia <= 0:
        print("Stok produk ini sudah habis untuk keranjang.")
        print("Silakan pilih produk lain")
        return None

    while True:
        jumlah = input_angka_atau_batal("Masukan jumlah barang: ")

        if jumlah is None:
            return "batal"

        if jumlah <= stok_tersedia:
            break

        print("Stok tidak mencukupi.")
        print("Stok yang masih bisa ditambahkan:", stok_tersedia)

    harga = produk_dipilih["harga"]
    nama_barang = produk_dipilih["nama"]
    subtotal = hitung_subtotal(harga, jumlah)

    barang = {
        "produk_id": produk_dipilih["id"],
        "nama": nama_barang,
        "harga": harga,
        "jumlah": jumlah,
        "subtotal": subtotal
    }

    return barang

def main():
    while True:
        print("\n===== PROGRAM KASIR =====")
        print("1. Transaksi baru")
        print("2. Riwayat transaksi")
        print("3. Detail transaksi")
        print("4. Keluar")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            daftar_barang = []
            total = 0
            jawaban = "ya"
            transaksi_dibatalkan = False

            while jawaban == "ya":
                barang = input_barang(daftar_barang)

                if barang == "batal":
                    transaksi_dibatalkan = True
                    break

                if barang is None:
                    jawaban = "ya"
                    continue

                subtotal = barang["subtotal"]
                total = total + subtotal
                daftar_barang.append(barang)

                print("Subtotal barang:", format_rupiah(subtotal))

                while True:
                    jawaban = input(
                        "Tambah barang lagi? "
                    ).strip().lower()

                    if jawaban == "ya" or jawaban == "tidak":
                        break

                    print("Jawaban harus berupa ya atau tidak!")

            if transaksi_dibatalkan:
                print("Transaksi dibatalkan.")
                continue

            if not daftar_barang:
                print("Transaksi dibatalkan karena belum ada barang.")
                continue

            tampilkan_struk(daftar_barang, total)

            hasil_pembayaran = proses_pembayaran(total)

            if hasil_pembayaran is None:
                print("Transaksi dibatalkan saat pembayaran.")
                continue

            uang_diterima, kembalian = hasil_pembayaran

            try:
                transaksi_id = simpan_transaksi(
                    daftar_barang,
                    total,
                    uang_diterima,
                    kembalian
                )

                print("Transaksi berhasil disimpan!")
                print("ID transaksi:", transaksi_id)
                print("===== TERIMA KASIH =====")

            except Exception as error:
                print("Transaksi gagal disimpan:", error)
                print("Silakan periksa database dan stok produk.")

        elif pilihan == "2":
            tampilkan_riwayat_transaksi()

        elif pilihan == "3":
            tampilkan_detail_transaksi()

        elif pilihan == "4":
            print("Program kasir ditutup.")
            break

        else:
            print("Pilihan tidak valid. Masukkan 1, 2, 3, atau 4.")


if __name__ == "__main__":
    main()