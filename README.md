# 🎮 Game Refleks Tangan (AI Hand Tracking)

Game interaktif berbasis Computer Vision yang menggunakan kamera untuk mendeteksi gerakan tangan pemain secara *real-time*. Pemain harus meniru gerakan target (Batu, Gunting, Kertas, dll.) secepat mungkin untuk mendapatkan skor.

**Dibuat dengan:** Python, OpenCV, MediaPipe, dan CVZone.

---

## 📋 Fitur
* **Deteksi Tangan Canggih:** Menggunakan AI Google MediaPipe yang presisi.
* **Mode Fullscreen:** Tampilan game memenuhi layar agar lebih seru.
* **Sistem Skor & Waktu:** Tantangan mengejar skor dalam waktu 60 detik.
* **Menu Interaktif:** Navigasi menu menggunakan gerakan mouse.

---

## ⚙️ Persiapan (Prerequisites)

Sebelum memulai, pastikan laptop/PC Anda memenuhi syarat berikut agar tidak error:

1.  **Python 3.10 (WAJIB)**
    * *Peringatan:* Python versi terbaru (3.12 / 3.13) sering **tidak cocok** dengan library MediaPipe.
    * Gunakan Python 3.10 agar game berjalan lancar.
    * Cek versi Anda dengan mengetik di terminal: `python --version`

2.  **Webcam / Kamera**
    * Diperlukan untuk membaca gerakan tangan.

---

## 🚀 Cara Install & Menjalankan

Ikuti langkah-langkah mudah ini:

### 1. Siapkan Folder
Download atau simpan file script game (misalnya `game_tangan.py`) di dalam sebuah folder di laptop Anda (Bebas di mana saja, misal di `Documents/GamePython`).

### 2. Buka Terminal / CMD
* Buka folder tersebut.
* Klik kanan di area kosong -> pilih **"Open in Terminal"** (atau buka CMD lalu arahkan ke folder tersebut dengan perintah `cd`).

### 3. Install Alat (Dependencies)
Copy dan paste perintah "sakti" di bawah ini ke terminal Anda. Perintah ini akan menginstall semua alat yang dibutuhkan sekaligus mencegah error versi:

```bash
pip install opencv-python cvzone mediapipe==0.10.9 protobuf==3.20.3
