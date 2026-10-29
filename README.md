# ETS Sistem Robot Otonom: Pemetaan 3D Point Cloud Quadcopter

Repositori ini berisi implementasi **3D Mapping Point Cloud** secara *real-time* menggunakan wahana *quadcopter* pada simulator **CoppeliaSim** berbasis **Python (ZeroMQ Remote API)**.

Proyek ini disusun untuk memenuhi Evaluasi Tengah Semester (ETS) mata kuliah **Sistem Robot Otonom**, Departemen Teknik Elektro, Institut Teknologi Sepuluh Nopember (ITS).

---

## 📌 Anggota & Informasi Proyek

* **Penyusun:** Nasrul (NRP. 5022241067)
* **Dosen Pengampu:** Muhammad Qomaruz Zaman, S.T., M.T., Ph.D.
* **Instansi:** Departemen Teknik Elektro, FTEIC - Institut Teknologi Sepuluh Nopember
* **Repositori GitHub:** https://github.com/nasruul/ETS-SRO-Nasrul.git
* **Demo Proses (YouTube):** https://youtu.be/beXEb19Ait4
* **Demo Hasil 3D (YouTube):** https://youtu.be/66v9deKGp1Y

---

## 🛠️ Arsitektur & Fitur Utama

1. **GUI Drone Controller (Tkinter + Multi-Key Holding):**
   * Pengendalian drone interaktif dengan dukungan tombol simultan (W/A/S/D untuk gerak planar, I/K untuk elevasi Z).
   * Pemrosesan *background thread* 50 Hz untuk pergerakan wahana yang halus tanpa *freezing* pada antarmuka.
2. **ZeroMQ Remote API Communication:**
   * Pengiriman data sinyal buffer `fast3D_data` dari sensor laser scanner CoppeliaSim ke skrip Python.
3. **Transformasi Koordinat Homogen:**
   * Konversi titik lokal sensor $P_{\text{local}}$ ke sistem koordinat dunia $P_{\text{global}}$ menggunakan matriks homogen $T_{\text{sensor}}^{\text{world}} \in \mathbb{R}^{4 \times 4}$.
4. **Voxel Grid Downsampling Filter:**
   * Reduksi redundansi data *point cloud* menggunakan filter kisi *voxel* ($s = 0.03\text{ m}$) untuk efisiensi komputasi visual.
5. **Visualisasi 3D Matplotlib:**
   * Plotting *point cloud* bergradasi warna elevasi $Z$ menggunakan *colormap* `turbo` lengkap dengan *colorbar* dan garis trajektori penerbangan drone.

---

## 🎮 Kontrol Navigasi Drone

| Tombol Keyboard | Aksi Navigasi | Sumbu Gerak |
| :---: | :--- | :--- |
| **W / S** | Maju / Mundur | Translatif Sumbu Y |
| **A / D** | Kiri / Kanan | Translatif Sumbu X |
| **I / K** | Naik / Turun | Elevasi Sumbu Z |
| **Stop & Plot 3D Map** | Hentikan penerbangan & render visualisasi 3D | Trigger Plotting Matplotlib |

---

## 📁 Struktur Berkas

.
├── 3Dmapping.py        # Skrip utama Python (GUI Controller, ZMQ API, Transformasi & Plot 3D)
├── 3DMapping.ttt       # File scene simulasi CoppeliaSim
├── quadcopter.lua      # Script Lua ekstrak untuk kontrol quadcopter
├── sensor_fast3d.lua   # Script Lua ekstrak untuk penangkap/pemancar buffer sensor 3D
├── controller.png      # Screenshot antarmuka GUI Drone Controller
├── 3d_map_result.png   # Hasil render grafik 3D point cloud & trajektori drone
├── main.pdf            # Laporan akhir ter-compile (PDF)
└── README.md           # Dokumentasi repositori

---

## 🚀 Cara Menjalankan Proyek

### 1. Persyaratan Sistem & Instalasi Pustaka
Pastikan **Python 3.10+** dan **CoppeliaSim V4.x** sudah terinstal di komputer Anda. Buka terminal atau PowerShell, lalu jalankan perintah berikut:

`pip install numpy matplotlib coppeliasim-zmqremoteapi-client`

### 2. Langkah Eksekusi Kode & Simulasi
1. **Buka Scene CoppeliaSim:**
   * Jalankan aplikasi **CoppeliaSim**.
   * Pilih menu `File` -> `Open scene...`, lalu muat file `3DMapping.ttt`.
2. **Jalankan Simulasi:**
   * Tekan tombol **Play** (ikon segitiga biru) di toolbar atas CoppeliaSim untuk mengaktifkan mesin simulasi.
3. **Eksekusi Script Python:**
   * Buka Terminal / PowerShell di dalam folder proyek ini.
   * Jalankan perintah: `python 3Dmapping.py`
4. **Kendalikan Drone:**
   * Jendela pop-up **Drone Controller** akan muncul.
   * Gunakan kombinasi tombol `W`, `A`, `S`, `D`, `I`, dan `K` untuk mengarahkan drone mengelilingi rintangan di area simulasi.
5. **Render & Simpan Peta 3D:**
   * Tekan tombol merah **"Stop & Plot 3D Map"** pada GUI.
   * Program akan otomatis menghentikan penerbangan, memproses *voxel grid filter*, menyimpan gambar `3d_map_result.png`, dan menampilkan window grafik 3D interaktif.

> **💡 Catatan Penanganan Error Script Lua:**
> Jika terjadi error pada script bawaan CoppeliaSim (misalnya sensor tidak mengirimkan data `fast3D_data` atau drone tidak merespon):
> 1. Double-click ikon script Lua pada objek `Quadcopter` atau `fast3D` di panel *Scene Hierarchy* CoppeliaSim.
> 2. Salin seluruh isi dari file `quadcopter.lua` (untuk drone) atau `sensor_fast3d.lua` (untuk sensor) yang ada di repositori ini.
> 3. *Paste* kode tersebut ke dalam editor script CoppeliaSim untuk menggantikan kode lama, lalu simpan (*Save & Close*).