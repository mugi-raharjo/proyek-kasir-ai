import matplotlib.pyplot as plt
import pandas as pd

from database import (
    get_data_analisis_produk,
    get_ringkasan_penjualan,
    get_omzet_harian,
    get_data_penjualan_produk
)

from utils import format_rupiah


def analisis_produk_terlaris():
    data_produk = get_data_analisis_produk()

    df = pd.DataFrame(data_produk)

    df = df.sort_values(
        by="total_terjual",
        ascending=False
    )

    produk_terlaris = df.head(5)

    print("\n===== 5 PRODUK TERLARIS =====")
    print(produk_terlaris)


def analisis_pendapatan_tertinggi():
    data_produk = get_data_analisis_produk()

    df = pd.DataFrame(data_produk)

    df = df.sort_values(
        by="total_pendapatan",
        ascending=False
    )

    produk_tertinggi = df.head(5)

    print("\n===== 5 PRODUK DENGAN PENDAPATAN TERTINGGI =====")
    print(produk_tertinggi)


def analisis_ringkasan_penjualan():
    ringkasan = get_ringkasan_penjualan()

    print("\n===== RINGKASAN PENJUALAN =====")
    print("Jumlah transaksi:", ringkasan["jumlah_transaksi"])
    print("Total omzet:", format_rupiah(ringkasan["total_omzet"]))
    print("Rata-rata transaksi:", format_rupiah(ringkasan["rata_rata_transaksi"]))


def buat_grafik_penjualan():
    data_produk = get_data_analisis_produk()

    df = pd.DataFrame(data_produk)


    df_terlaris = df.sort_values(
        by="total_terjual",
        ascending=False
    )

    plt.bar(
        df_terlaris["nama"],
        df_terlaris["total_terjual"]
    )

    plt.title("Jumlah Produk Terjual")
    plt.xlabel("Nama Produk")
    plt.ylabel("Jumlah Terjual")

    plt.show()


    df_pendapatan = df.sort_values(
        by="total_pendapatan",
        ascending=False
    )

    plt.bar(
        df_pendapatan["nama"],
        df_pendapatan["total_pendapatan"]
    )

    plt.title("Pendapatan Setiap Produk")
    plt.xlabel("Nama Produk")
    plt.ylabel("Total Pendapatan")

    plt.show()


def analisis_omzet_harian():
    data_harian = get_omzet_harian()

    df = pd.DataFrame(data_harian)

    df["perubahan_omzet"] = df["omzet"].diff()
    df["persentase_perubahan"] = (df["omzet"].pct_change() * 100).round(2)
    df["moving_average_3_hari"] = df["omzet"].rolling(window=3).mean()

    print("\n===== ANALISIS OMZET HARIAN =====")
    print(df)

    print("\nTotal omzet seluruh hari:", format_rupiah(df["omzet"].sum()))


def grafik_omzet_harian():
    data_harian = get_omzet_harian()

    df = pd.DataFrame(data_harian)

    df["moving_average_3_hari"] = df["omzet"].rolling(window=3).mean()

    plt.plot(
        df["tanggal"],
        df["omzet"],
        marker="o"
    )

    plt.plot(
    df["tanggal"],
    df["moving_average_3_hari"],
    marker="o"
    )

    plt.legend(["Omzet Aktual", "Moving Average 3 Hari"])
    plt.title("Perkembangan Omzet Harian")
    plt.xlabel("Tanggal")
    plt.ylabel("Omzet")

    plt.xticks(rotation=45)

    plt.grid(True)
    plt.tight_layout()

    plt.show()


def analisis_rata_rata_penjualan():
    data_produk = get_data_penjualan_produk()

    jumlah_hari = 7

    print("\n===== RATA-RATA PENJUALAN HARIAN =====")

    for produk in data_produk:
        rata_rata = produk["total_terjual"] / jumlah_hari

        print(
            produk["nama"],
            ":", round(rata_rata, 2),
            "unit per hari"
        )


def analisis_kebutuhan_stok():
    data_produk = get_data_penjualan_produk()

    jumlah_hari = 7
    lead_time = 3
    safety_stock = 5

    print("\n===== ANALISIS KEBUTUHAN STOK =====")

    for produk in data_produk:
        rata_rata = produk["total_terjual"] / jumlah_hari

        rop = (rata_rata * lead_time) + safety_stock

        stok = produk["stok"]

        target_stok = (rata_rata * jumlah_hari) + safety_stock

        jumlah_pemesanan = target_stok - stok

        if jumlah_pemesanan < 0:
            jumlah_pemesanan = 0

        if stok <= rop:
            status = "PERLU PESAN ULANG"
        else:
            status = "STOK AMAN"

        print("\nNama Produk:", produk["nama"])
        print("Stok Saat Ini:", stok)
        print("Rata-rata Penjualan:", round(rata_rata, 2))
        print("Reorder Point:", round(rop, 2))
        print("Target Stok:", round(target_stok))
        print("Status:", status)
        print("Jumlah Pemesanan:", round(jumlah_pemesanan))


def menu_analisis():
    while True:
        print("\n===== MENU ANALISIS PENJUALAN =====")
        print("1. Produk terlaris")
        print("2. Ringkasan penjualan")
        print("3. Pendapatan tertinggi")
        print("4. Analisis omzet harian")
        print("5. Rata-rata penjualan harian")
        print("6. Analisis kebutuhan stok")
        print("7. Kembali ke menu utama")

        pilihan = input("Pilih menu analisis: ").strip()

        if pilihan == "1":
            analisis_produk_terlaris()

        elif pilihan == "2":
            analisis_ringkasan_penjualan()

        elif pilihan == "3":
            analisis_pendapatan_tertinggi()

        elif pilihan == "4":
            analisis_omzet_harian()
            grafik_omzet_harian()

        elif pilihan == "5":
            analisis_rata_rata_penjualan()

        elif pilihan == "6":
            analisis_kebutuhan_stok()

        elif pilihan == "7":
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    analisis_produk_terlaris()
    analisis_ringkasan_penjualan()
    analisis_pendapatan_tertinggi()
    buat_grafik_penjualan()
    analisis_omzet_harian()
    grafik_omzet_harian()
    analisis_rata_rata_penjualan()
    analisis_kebutuhan_stok()