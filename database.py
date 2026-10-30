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
    koneksi = get_connection()
    cursor = koneksi.cursor()

    try:
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
        koneksi.rollback()
        raise

    finally:
        cursor.close()
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
