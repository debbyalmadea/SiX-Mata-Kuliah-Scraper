# SiX Web Scraper

SiX Web Scraper adalah proyek untuk mengambil data dari Sistem Informasi Akademik SiX milik ITB. Proyek ini fokus pada pengambilan data mata kuliah, kelas mata kuliah, jadwal, dan informasi terkait dari halaman jadwal kuliah pada menu kelas SiX.

## Disclaimer

**Perhatian**: Proyek ini adalah upaya untuk mengambil data dari Sistem Informasi Akademik SiX yang dimiliki oleh Institut Teknologi Bandung (ITB). Data yang diperoleh melalui proyek ini sepenuhnya dimiliki oleh ITB dan digunakan dengan tujuan non-komersial dan pendidikan. Pembuat proyek tidak memiliki kepemilikan atau klaim atas data yang diambil melalui scraping. 

## Prasyarat

Pastikan Anda telah menginstal semua prasyarat yang tercantum dalam file `requirements.txt` sebelum menjalankan proyek ini.

```bash
pip install -r requirements.txt
```

## Penggunaan

Berikut adalah langkah-langkah untuk menjalankan proyek SiX Web Scraper:

1. Ubah nama file `.env.example` menjadi `.env`.

2. Isi semua variabel yang diperlukan dalam file `.env` sesuai dengan konfigurasi Anda.

3. Pastikan Anda memiliki `COOKIES_KHONGGUAN`, yang dapat ditemukan dengan cara berikut:
   - Buka halaman SiX di peramban web.
   - Lakukan inspect element pada laman tersebut.
   - Pergi ke tab Application (Aplikasi) atau Storage (Penyimpanan) di inspect element.
   - Temukan cookies yang memiliki nama `khongguan`.

4. Pastikan server PostgreSQL sudah berjalan dan Anda memiliki database yang sesuai dengan konfigurasi yang diisi di dalam file `.env`.

5. Jalankan web scraper dengan menggunakan perintah berikut:
   ```bash
   python3 scraper.py
    ```
    or
    ```bash
   python scraper.py
    ```
    Sesuaikan perintah dengan lingkungan lokal Anda.
