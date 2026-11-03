import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    koneksi = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "db_kasir")
    )
    return koneksi


def get_products():
    koneksi = get_connection()
    cursor = koneksi.cursor(dictionary=True)

    cursor.execute("SELECT id, nama, harga, stok FROM produk")

    produk = cursor.fetchall()

    cursor.close()
    koneksi.close()

    return produk

def simpan_transaksi(daftar_barang, total, uang_diterima, kembalian):

    if not isinstance(daftar_barang, list) or not daftar_barang:
        raise ValueError("Keranjang transaksi tidak boleh kosong.")

    if not all(
        isinstance(nilai, int) and not isinstance(nilai, bool)
        for nilai in [total, uang_diterima, kembalian]
    ):
        raise ValueError(
            "Total, pembayaran, dan kembalian harus berupa bilangan bulat."
        )

    total_validasi = 0

    for barang in daftar_barang:
        if not isinstance(barang, dict):
            raise ValueError("Setiap barang harus berupa dictionary.")

        kolom_wajib = [
            "produk_id",
            "nama",
            "harga",
            "jumlah",
            "subtotal"
        ]

        if not all(kolom in barang for kolom in kolom_wajib):
            raise ValueError("Data barang tidak lengkap.")
        produk_id = barang["produk_id"]
        harga = barang["harga"]
        jumlah = barang["jumlah"]
        subtotal = barang["subtotal"]

        if not all(
            isinstance(nilai, int) and not isinstance(nilai, bool)
            for nilai in [produk_id, harga, jumlah, subtotal]
        ):
            raise ValueError("Data barang harus berupa bilangan bulat.")

        if produk_id <= 0 or harga <= 0 or jumlah <= 0:
            raise ValueError("ID, harga, dan jumlah harus lebih dari 0.")

        subtotal_validasi = harga * jumlah

        if subtotal != subtotal_validasi:
            raise ValueError(
                f"Subtotal barang {barang['nama']} tidak sesuai."
            )

        total_validasi += subtotal_validasi

    if total != total_validasi:
        raise ValueError("Total transaksi tidak sesuai dengan detail barang.")

    if uang_diterima < total_validasi:
        raise ValueError("Uang pembayaran tidak mencukupi.")

    if kembalian != uang_diterima - total_validasi:
        raise ValueError("Perhitungan kembalian tidak sesuai.")

    koneksi = None
    cursor = None

    try:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        # Memeriksa harga dan stok terbaru dari database
        for barang in daftar_barang:
            cursor.execute(
                """
                SELECT harga, stok
                FROM produk
                WHERE id = %s
                FOR UPDATE
                """,
                (barang["produk_id"],)
            )

            produk = cursor.fetchone()

            if produk is None:
                raise ValueError(
                    f"Produk {barang['nama']} tidak ditemukan."
                )

            harga_database, stok_database = produk

            if barang["harga"] != harga_database:
                raise ValueError(
                    f"Harga produk {barang['nama']} telah berubah."
                )

            if barang["jumlah"] > stok_database:
                raise ValueError(
                    f"Stok produk {barang['nama']} tidak mencukupi."
                )

        # Menyimpan data transaksi utama
        cursor.execute(
            """
            INSERT INTO transaksi (total, uang_diterima, kembalian)
            VALUES (%s, %s, %s)
            """,
            (total, uang_diterima, kembalian)
        )

        transaksi_id = cursor.lastrowid

        for barang in daftar_barang:
            cursor.execute(
                """
                UPDATE produk
                SET stok = stok - %s
                WHERE id = %s AND stok >= %s
                """,
                (
                    barang["jumlah"],
                    barang["produk_id"],
                    barang["jumlah"]
                )
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Stok produk {barang['nama']} tidak mencukupi."
                )

            cursor.execute(
                """
                INSERT INTO detail_transaksi
                (transaksi_id, produk_id, harga, jumlah, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    transaksi_id,
                    barang["produk_id"],
                    barang["harga"],
                    barang["jumlah"],
                    barang["subtotal"]
                )
            )

        koneksi.commit()
        return transaksi_id

    except Exception:
        if koneksi is not None:
            koneksi.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if koneksi is not None:
            koneksi.close()

def get_riwayat_transaksi():
    koneksi = get_connection()
    cursor = koneksi.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
        transaksi.id,
        transaksi.tanggal,
        transaksi.total,
        transaksi.uang_diterima,
        transaksi.kembalian,
        produk.nama,
        detail_transaksi.harga,
        detail_transaksi.jumlah,
        detail_transaksi.subtotal
        FROM transaksi
        JOIN detail_transaksi
        ON transaksi.id = detail_transaksi.transaksi_id
        JOIN produk
        ON detail_transaksi.produk_id = produk.id
        ORDER BY transaksi.id DESC
        """
    )

    riwayat = cursor.fetchall()

    cursor.close()
    koneksi.close()

    return riwayat


def get_detail_transaksi(id_transaksi):
    koneksi = get_connection()
    cursor = koneksi.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
        transaksi.id,
        transaksi.tanggal,
        transaksi.total,
        transaksi.uang_diterima,
        transaksi.kembalian,
        produk.nama,
        detail_transaksi.harga,
        detail_transaksi.jumlah,
        detail_transaksi.subtotal
        FROM transaksi
        JOIN detail_transaksi
        ON transaksi.id = detail_transaksi.transaksi_id
        JOIN produk
        ON detail_transaksi.produk_id = produk.id
        WHERE transaksi.id = %s
        ORDER BY produk.nama ASC
        """,
        (id_transaksi,)
    )

    detail = cursor.fetchall()

    cursor.close()
    koneksi.close()

    return detail

def get_data_analisis_produk():
    koneksi = get_connection()
    cursor = koneksi.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            produk.id AS produk_id,
            produk.nama,
            SUM(detail_transaksi.jumlah) AS total_terjual,
            SUM(detail_transaksi.subtotal) AS total_pendapatan
        FROM detail_transaksi
        JOIN produk
        ON detail_transaksi.produk_id = produk.id
        GROUP BY produk.id, produk.nama
        ORDER BY total_terjual DESC
        """
    )

    data_produk = cursor.fetchall()

    cursor.close()
    koneksi.close()

    return data_produk

def get_ringkasan_penjualan():
    koneksi = get_connection()
    cursor = koneksi.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            COUNT(*) AS jumlah_transaksi,
            COALESCE(SUM(total), 0) AS total_omzet,
            COALESCE(AVG(total), 0) AS rata_rata_transaksi
        FROM transaksi
        """
    )

    ringkasan = cursor.fetchone()

    cursor.close()
    koneksi.close()

    return ringkasan

def get_omzet_harian():
    koneksi = get_connection()
    cursor = koneksi.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            DATE(tanggal) AS tanggal,
            SUM(total) AS omzet
        FROM transaksi
        GROUP BY DATE(tanggal)
        ORDER BY tanggal ASC
        """
    )

    data_harian = cursor.fetchall()

    cursor.close()
    koneksi.close()

    return data_harian


def get_data_penjualan_produk():
    koneksi = get_connection()
    cursor = koneksi.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            produk.id AS produk_id,
            produk.nama,
            produk.stok,
            COALESCE(
                SUM(
                    CASE
                        WHEN transaksi.id IS NOT NULL
                        THEN detail_transaksi.jumlah
                        ELSE 0
                    END
                ), 0
            ) AS total_terjual
        FROM produk
        LEFT JOIN detail_transaksi
        ON produk.id = detail_transaksi.produk_id
        LEFT JOIN transaksi
        ON detail_transaksi.transaksi_id = transaksi.id
        AND transaksi.tanggal >= '2026-10-27 00:00:00'
        AND transaksi.tanggal < '2026-11-03 00:00:00'
        GROUP BY produk.id, produk.nama, produk.stok
        ORDER BY total_terjual DESC
        """
    )

    data_produk = cursor.fetchall()

    cursor.close()
    koneksi.close()

    return data_produk