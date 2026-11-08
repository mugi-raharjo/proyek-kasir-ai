from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from database import (
    get_products,
    get_product_by_id,
    tambah_produk as simpan_produk,
    update_produk,
    produk_memiliki_transaksi,
    hapus_produk,
    nonaktifkan_produk,
    simpan_transaksi,
    get_riwayat_transaksi,
    get_detail_transaksi
)

class ProdukInput(BaseModel):
    nama: str
    harga: int = Field(gt=0)
    stok: int = Field(ge=0)

    @field_validator("nama")
    @classmethod
    def validasi_nama(cls, nilai):
        if not nilai.strip():
            raise ValueError("Nama produk tidak boleh kosong.")

        return nilai.strip()

class DetailTransaksiInput(BaseModel):
    produk_id: int
    jumlah: int = Field(gt=0)

class TransaksiInput(BaseModel):
    items: list[DetailTransaksiInput] = Field(min_length=1)
    uang_dibayar: int = Field(ge=0)

app = FastAPI()

@app.get("/")
def halaman_utama():
    return {
        "pesan": "API Kasir AI berhasil dijalankan!"
    }

@app.get("/produk")
def tampilkan_produk():
    produk = get_products()
    return produk

@app.get("/produk/{produk_id}")
def tampilkan_produk_berdasarkan_id(produk_id: int):
    produk = get_product_by_id(produk_id)

    if produk is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    return produk

@app.post("/produk", status_code=201)
def tambah_produk(produk: ProdukInput):
    produk_id = simpan_produk(
        produk.nama,
        produk.harga,
        produk.stok
    )

    produk_baru = get_product_by_id(produk_id)

    return {
        "pesan": "Produk berhasil ditambahkan",
        "data": produk_baru
    }

@app.put("/produk/{produk_id}")
def ubah_produk(produk_id: int, produk: ProdukInput):
    produk_lama = get_product_by_id(produk_id)

    if produk_lama is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    update_produk(
        produk_id,
        produk.nama,
        produk.harga,
        produk.stok
    )

    produk_diperbarui = get_product_by_id(produk_id)

    return {
        "pesan": "Produk berhasil diperbarui",
        "data": produk_diperbarui
    }

@app.delete("/produk/{produk_id}")
def hapus_produk_api(produk_id: int):
    produk = get_product_by_id(produk_id)

    if produk is None:
        raise HTTPException(
            status_code=404,
            detail="Produk tidak ditemukan"
        )

    memiliki_transaksi = produk_memiliki_transaksi(produk_id)

    if memiliki_transaksi:
        nonaktifkan_produk(produk_id)

        return {
            "pesan": "Produk memiliki riwayat transaksi dan berhasil dinonaktifkan",
            "aksi": "dinonaktifkan",
            "id": produk_id
        }

    hapus_produk(produk_id)

    return {
        "pesan": "Produk berhasil dihapus permanen",
        "aksi": "dihapus permanen",
        "id": produk_id
    }

@app.post("/transaksi", status_code=201)
def buat_transaksi(transaksi: TransaksiInput):
    daftar_barang = []
    total = 0
    
    for item in transaksi.items:
        produk = get_product_by_id(item.produk_id)

        if produk is None:
            raise HTTPException(
                status_code=404,
                detail=f"Produk dengan ID {item.produk_id} tidak ditemukan."
            )

        if produk["aktif"] == 0:
            raise HTTPException(
                status_code=400,
                detail=f"Produk {produk['nama']} sudah tidak aktif."
            )

        if item.jumlah <= 0:
            raise HTTPException(
                status_code=400,
                detail="Jumlah barang harus lebih dari 0."
            )

        harga = produk["harga"]
        jumlah = item.jumlah
        subtotal = harga * jumlah

        barang = {
            "produk_id": produk["id"],
            "nama": produk["nama"],
            "harga": harga,
            "jumlah": jumlah,
            "subtotal": subtotal
        }

        daftar_barang.append(barang)
        total += subtotal

    uang_diterima = transaksi.uang_dibayar

    if uang_diterima < total:
        raise HTTPException(
            status_code=400,
            detail="Uang pembayaran kurang."
        )

    kembalian = uang_diterima - total

    try:
        transaksi_id = simpan_transaksi(
            daftar_barang,
            total,
            uang_diterima,
            kembalian
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "pesan": "Transaksi berhasil disimpan",
        "transaksi_id": transaksi_id,
        "total": total,
        "uang_diterima": uang_diterima,
        "kembalian": kembalian
    }

@app.get("/transaksi")
def baca_riwayat_transaksi():
    riwayat = get_riwayat_transaksi()

    return riwayat

@app.get("/transaksi/{transaksi_id}")
def baca_detail_transaksi(transaksi_id: int):
    detail = get_detail_transaksi(transaksi_id)

    if not detail:
        raise HTTPException(
            status_code=404,
            detail="Transaksi tidak ditemukan."
        )

    return detail