# Proyek Kasir — Python dan MySQL

Program kasir berbasis Python yang menggunakan MySQL untuk mengelola produk, stok, transaksi, dan riwayat pembelian.

## Fitur

- Menampilkan daftar produk dan stok.
- Memilih produk dan menentukan jumlah pembelian.
- Memvalidasi input dan memeriksa ketersediaan stok.
- Menghitung subtotal, total belanja, dan kembalian.
- Membatalkan transaksi sebelum pembayaran selesai.
- Menyimpan transaksi dan memperbarui stok di database MySQL.
- Menampilkan riwayat dan detail transaksi.
- Memformat nominal uang dalam Rupiah.

## Teknologi

- Python
- MySQL
- `mysql-connector-python`
- `python-dotenv`
- Git dan GitHub

## Struktur Proyek

```text
proyek-kasir-ai/
├── main.py
├── utils.py
├── database.py
├── test_utils.py
├── test_database.py
├── test_riwayat.py
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

## Menjalankan Program

Jalankan perintah berikut dari folder utama proyek:

```powershell
python main.py
```

## Pengujian

Uji fungsi subtotal, format Rupiah, dan validasi:

```powershell
python test_utils.py
```

Uji pembacaan daftar produk:

```powershell
python test_database.py
```

Uji pembacaan riwayat transaksi:

```powershell
python test_riwayat.py
```

`test_database.py` dan `test_riwayat.py` merupakan skrip pengujian manual yang membaca data dari database. Pastikan konfigurasi database sudah benar sebelum menjalankannya.

## Catatan Pengembangan

Proyek ini dikembangkan secara bertahap sebagai sarana belajar Python, database, SQL, pengujian, Git, dan GitHub. Walaupun nama repositorinya `proyek-kasir-ai`, versi saat ini berfokus pada aplikasi kasir berbasis Python dan MySQL. Fitur AI akan dikembangkan pada tahap berikutnya.
