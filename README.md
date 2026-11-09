# Proyek Kasir AI — Python, MySQL, dan FastAPI

Program kasir berbasis Python yang menggunakan MySQL untuk mengelola produk, stok, transaksi, dan riwayat pembelian. Proyek ini juga menyediakan REST API menggunakan FastAPI.

## Fitur

- Menampilkan daftar produk dan stok.
- Memilih produk dan menentukan jumlah pembelian.
- Memvalidasi input dan memeriksa ketersediaan stok.
- Menghitung subtotal, total belanja, dan kembalian.
- Membatalkan transaksi sebelum pembayaran selesai.
- Menyimpan transaksi dan memperbarui stok di database MySQL.
- Menampilkan riwayat dan detail transaksi.
- Memformat nominal uang dalam Rupiah.
- Menyediakan API untuk pengelolaan produk dan transaksi.
- Melakukan validasi request dan pengujian otomatis API.
- Menganalisis produk terlaris dan pendapatan setiap produk.
- Menampilkan ringkasan penjualan dan tren omzet harian.
- Menghitung rata-rata penjualan dan kebutuhan stok.
- Menampilkan grafik penjualan menggunakan Matplotlib.

## Teknologi

- Python
- MySQL
- FastAPI
- Pydantic
- mysql-connector-python
- python-dotenv
- Pandas
- Matplotlib
- Git dan GitHub

## Struktur Proyek

```text
proyek-kasir-ai/
├── main.py
├── api.py
├── database.py
├── utils.py
├── analisis_penjualan.py
├── test_api.py
├── test_database.py
├── test_riwayat.py
├── test_stok.py
├── test_utils.py
├── test_validasi_database.py
├── test_validasi_transaksi.py
├── requirements.txt
├── .gitignore
└── README.md
```

File `.env` juga diperlukan untuk konfigurasi lokal, tetapi tidak disertakan dalam repositori.

## Persiapan

1. Instal Python dan MySQL.
2. Pastikan server MySQL berjalan.
3. Siapkan database `db_kasir` beserta tabel `produk`, `transaksi`, dan `detail_transaksi`.
4. Buka terminal di folder proyek.
5. Instal dependensi:

```powershell
python -m pip install -r requirements.txt
```

6. Buat file `.env` di folder utama proyek dan isi dengan konfigurasi lokal:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=db_kasir
```

Sesuaikan nilai konfigurasi dengan lingkungan MySQL masing-masing. Jangan mengunggah kata sandi atau informasi rahasia ke repositori publik.

## Menjalankan Program Kasir

Jalankan perintah berikut dari folder utama proyek:

```powershell
python main.py
```

## Pengujian

Uji fungsi subtotal, format Rupiah, dan validasi:

```powershell
python -m unittest test_utils -v
```

Uji pembacaan daftar produk:

```powershell
python test_database.py
```

Uji pembacaan riwayat transaksi:

```powershell
python test_riwayat.py
```

Uji endpoint API:

```powershell
python -m unittest test_api -v
```

`test_database.py` dan `test_riwayat.py` merupakan skrip pengujian manual yang membaca data dari database. Pastikan konfigurasi database sudah benar sebelum menjalankannya.

Pengujian API menggunakan database pengujian `db_kasir_test` agar perubahan selama pengujian tidak memengaruhi database utama `db_kasir`.

File pengujian lainnya:
- `test_stok.py`: menguji fungsi terkait stok.
- `test_validasi_database.py`: menguji validasi pada proses database.
- `test_validasi_transaksi.py`: menguji validasi transaksi.

## Dokumentasi API

API Kasir AI dibangun menggunakan FastAPI dan terhubung dengan database MySQL.

### Menjalankan API

Jalankan perintah berikut dari terminal di folder proyek:

```powershell
python -m uvicorn api:app --reload
```

Alamat lokal API:

http://127.0.0.1:8000

Dokumentasi interaktif Swagger UI:

http://127.0.0.1:8000/docs

### Daftar Endpoint

| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/` | Memeriksa status API |
| GET | `/produk` | Mengambil semua produk |
| GET | `/produk/{produk_id}` | Mengambil produk berdasarkan ID |
| POST | `/produk` | Menambahkan produk |
| PUT | `/produk/{produk_id}` | Memperbarui produk |
| DELETE | `/produk/{produk_id}` | Menghapus atau menonaktifkan produk |
| POST | `/transaksi` | Membuat transaksi baru |
| GET | `/transaksi` | Mengambil riwayat transaksi |
| GET | `/transaksi/{transaksi_id}` | Mengambil detail transaksi |

---

### 1. GET `/`

Memeriksa apakah API berhasil dijalankan.

**Response sukses — 200 OK

```json
{
  "pesan": "API Kasir AI berhasil dijalankan!"
}
```

### 2. GET `/produk`

Mengambil seluruh data produk dari database.

Response — 200 OK

Mengembalikan daftar produk.

### 3. GET `/produk/{produk_id}`

Mengambil data produk berdasarkan ID.

Path parameter:

- `produk_id`: ID produk yang ingin dicari.

Response sukses — 200 OK

Mengembalikan data produk berdasarkan ID.

Response gagal — 404 Not Found

```json
{
  "detail": "Produk tidak ditemukan"
}
```

### 4. POST `/produk`

Menambahkan produk baru ke database.

Request Body:

```json
{
  "nama": "Buku",
  "harga": 10000,
  "stok": 20
}
```

Validasi:

- `nama` tidak boleh kosong atau hanya berisi spasi.
- `harga` harus lebih dari 0.
- `stok` minimal 0.

Response sukses — 201 Created

```json
{
  "pesan": "Produk berhasil ditambahkan",
  "data": {
    "id": 1,
    "nama": "Buku",
    "harga": 10000,
    "stok": 20,
    "aktif": 1
  }
}
```

### 5. PUT `/produk/{produk_id}`

Memperbarui data produk berdasarkan ID.

Path parameter:

- `produk_id`: ID produk yang ingin diperbarui.

Request Body:

```json
{
  "nama": "Buku Tulis",
  "harga": 12000,
  "stok": 25
}
```

Validasi:

Menggunakan aturan validasi yang sama dengan POST `/produk`.

Response sukses — 200 OK

Mengembalikan pesan dan data produk yang telah diperbarui.

Response gagal — 404 Not Found

Jika produk tidak ditemukan.

### 6. DELETE `/produk/{produk_id}`

Menghapus produk berdasarkan ID.

Endpoint ini memiliki dua kemungkinan tindakan.

A. Produk belum memiliki riwayat transaksi

Produk dihapus secara permanen.

Contoh response:

```json
{
  "pesan": "Produk berhasil dihapus permanen",
  "aksi": "dihapus permanen",
  "id": 1
}
```

B. Produk sudah memiliki riwayat transaksi

Produk dinonaktifkan agar riwayat transaksi tetap terjaga.

Contoh response:

```json
{
  "pesan": "Produk memiliki riwayat transaksi dan berhasil dinonaktifkan",
  "aksi": "dinonaktifkan",
  "id": 1
}
```

Response gagal — 404 Not Found

Jika produk tidak ditemukan.

### 7. POST `/transaksi`

Membuat transaksi baru berdasarkan daftar produk yang dibeli.

Request Body:

```json
{
  "items": [
    {
      "produk_id": 1,
      "jumlah": 2
    },
    {
      "produk_id": 2,
      "jumlah": 3
    }
  ],
  "uang_dibayar": 50000
}
```

Validasi:

- `items` minimal berisi satu barang.
- `produk_id` digunakan untuk mencari produk.
- `jumlah` harus lebih dari 0.
- `uang_dibayar` minimal 0.
- Produk harus tersedia dan berstatus aktif.
- Stok produk harus mencukupi.
- Pembayaran harus mencukupi total transaksi.

Response sukses — 201 Created

```json
{
  "pesan": "Transaksi berhasil disimpan",
  "transaksi_id": 15,
  "total": 29000,
  "uang_diterima": 50000,
  "kembalian": 21000
}
```

Kemungkinan response gagal:

- `400 Bad Request`: pembayaran kurang, produk tidak aktif, atau stok tidak mencukupi.
- `404 Not Found`: produk tidak ditemukan.
- `422 Unprocessable Entity`: format atau nilai input tidak memenuhi validasi.

### 8. GET `/transaksi`

Mengambil seluruh riwayat transaksi yang tersimpan di database.

Response — 200 OK

Mengembalikan daftar transaksi beserta rincian setiap produk yang dibeli.

Setiap baris hasil mewakili satu produk dalam suatu transaksi. Informasi transaksi seperti ID, tanggal, total, pembayaran, dan kembalian dapat muncul berulang apabila satu transaksi memiliki beberapa produk.

Contoh response:

```json
[
  {
    "id": 15,
    "tanggal": "2026-11-08T09:30:00",
    "total": 29000,
    "uang_diterima": 50000,
    "kembalian": 21000,
    "nama": "Buku",
    "harga": 10000,
    "jumlah": 2,
    "subtotal": 20000
  },
  {
    "id": 15,
    "tanggal": "2026-11-08T09:30:00",
    "total": 29000,
    "uang_diterima": 50000,
    "kembalian": 21000,
    "nama": "Pensil",
    "harga": 3000,
    "jumlah": 3,
    "subtotal": 9000
  }
]
```

Riwayat diurutkan berdasarkan ID transaksi dari terbesar ke terkecil.

### 9. GET `/transaksi/{transaksi_id}`

Mengambil rincian produk berdasarkan ID transaksi.

Path parameter:

- `transaksi_id`: ID transaksi yang ingin dilihat.

Response sukses — 200 OK

Mengembalikan daftar produk dalam transaksi yang dipilih, termasuk informasi:

- Nama produk.
- Harga produk.
- Jumlah pembelian.
- Subtotal produk.
- Informasi transaksi.

Data produk diurutkan berdasarkan nama secara alfabetis.

Response gagal — 404 Not Found

```json
{
  "detail": "Transaksi tidak ditemukan."
}
```

---

### Validasi dan HTTP Status Code

| Status Code | Keterangan |
|---|---|
| 200 | Permintaan berhasil |
| 201 | Data berhasil dibuat |
| 400 | Permintaan tidak dapat diproses karena aturan bisnis |
| 404 | Data yang dicari tidak ditemukan |
| 422 | Data input tidak memenuhi validasi |

### Teknologi API

- Python
- FastAPI
- Pydantic
- MySQL
- MySQL Connector

## Catatan Pengembangan

Proyek ini dikembangkan secara bertahap sebagai sarana penerapan Python, SQL, MySQL, pengolahan data, pengujian perangkat lunak, Git, GitHub, dan REST API.

Versi saat ini sudah memiliki fitur analisis penjualan dan analisis kebutuhan stok menggunakan rata-rata penjualan, Reorder Point (ROP), dan Safety Stock.

Analisis tersebut masih menggunakan perhitungan berbasis aturan dan belum menggunakan Machine Learning.

Pengembangan berikutnya direncanakan mencakup:
- Prediksi permintaan dan kebutuhan stok menggunakan Machine Learning.
- Rekomendasi produk berdasarkan pola pembelian.
- Asisten kasir berbasis Large Language Model (LLM).