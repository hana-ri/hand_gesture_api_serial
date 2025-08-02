# Hand Gesture Recognition API

Aplikasi ini mendeteksi gesture jari menggunakan webcam dan mengirimkan perintah ke ESP32 melalui serial.

## Persyaratan
- Python 3.12.3 (wajib)
- Lihat `requirements.txt` untuk daftar dependensi Python

## Instalasi
1. Pastikan Python 3.12.3 sudah terpasang di sistem Anda.
2. Install dependensi dengan perintah:
   
   ```bash
   pip install -r requirements.txt
   ```

## Penggunaan
1. Sambungkan ESP32 ke komputer dan pastikan port serial sudah benar di `main.py` (ubah variabel `SERIAL_PORT` jika perlu).
2. Jalankan aplikasi:
   
   ```bash
   python main.py
   ```
3. Arahkan tangan ke kamera, gesture jari akan dideteksi dan perintah dikirim ke ESP32.

## Catatan
- Pastikan port serial sesuai dengan perangkat Anda (misal: `COM8` di Windows).
- Untuk keluar dari aplikasi, tekan tombol `Esc` pada jendela tampilan.
