# ETS Sistem Robot Otonom: Pemetaan 3D Point Cloud Quadcopter

Repositori ini berisi implementasi **3D Mapping Point Cloud** secara *real-time* menggunakan wahana *quadcopter* pada simulator **CoppeliaSim** berbasis **Python (ZeroMQ Remote API)**. 

Proyek ini disusun untuk memenuhi Evaluasi Tengah Semester (ETS) mata kuliah **Sistem Robot Otonom**, Departemen Teknik Elektro, Institut Teknologi Sepuluh Nopember (ITS).

---

## 📌 Anggota & Informasi Proyek

* **Penyusun:** Nasrul (NRP. 5022241067)
* **Dosen Pengampu:** Muhammad Qomaruz Zaman, S.T., M.T., Ph.D.
* **Instansi:** Departemen Teknik Elektro, FTEIC - Institut Teknologi Sepuluh Nopember
* **Repositori GitHub:** [nasruul/ETS-SRO-Nasrul](https://github.com/nasruul/ETS-SRO-Nasrul.git)
* **Demo Proses (YouTube):** [Lihat Video Demo Proses](https://youtu.be/beXEb19Ait4)
* **Demo Hasil 3D (YouTube):** [Lihat Video Hasil 3D Map](https://youtu.be/66v9deKGp1Y)

---

## 🛠️ Arsitektur & Fitur Utama

1. **GUI Drone Controller (Tkinter + Multi-Key Holding):**
   * Pengendalian drone interaktif dengan dukungan tombol simultan (W/A/S/D untuk gerak planar, I/K untuk elevasi Z).
   * Pemrosesan *background thread* $50\text{ Hz}$ untuk pergerakan wahana yang halus tanpa *freezing* pada antarmuka.
2. **ZeroMQ Remote API Communication:**
   * Pengiriman data sinyal buffer `fast3D_data` dari sensor laser scanner CoppeliaSim ke skrip Python.
3. **Transformasi Koordinat Homogen:**
   * Konversi titik lokal sensor $P_{\text{local}}$ ke sistem koordinat dunia $P_{\text{global}}$ menggunakan matriks homogen $T_{\text{sensor}}^{\text{world}} \in \mathbb{R}^{4 \times 4}$.
4. **Voxel Grid Downsampling Filter:**
   * Reduksi redundansi data *point cloud* menggunakan filter kisi *voxel* ($s = 0.03\text{ m}$) untuk efisiensi komputasi visual.
5. **Visualisasi 3D Matplotlib:**
   * Plotting *point cloud* bergradasi warna elevasi $Z$ menggunakan *colormap* `turbo` lengkap dengan *colorbar* dan garis trajektori penerbangan drone.

---

## 📁 Struktur Berkas

```text
.
├── 3Dmapping.py        # Skrip utama Python (GUI Controller, ZMQ API, Transformasi & Plot 3D)
├── 3DMapping.ttt       # File scene simulasi CoppeliaSim
├── 3d_map_result.png   # Hasil render grafik 3D point cloud & trajektori drone
├── main.pdf            # Laporan akhir ter-compile (PDF)
└── README.md           # Dokumentasi repositori
