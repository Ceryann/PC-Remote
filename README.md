# PC Remote

[![Bahasa Indonesia](https://img.shields.io/badge/Bahasa%20Indonesia-0969da?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/English-6e7781?style=for-the-badge)](README.en.md)

PC Remote mengubah HP Android menjadi **touchpad, keyboard, dan gamepad PS4 (DualShock 4)** untuk laptop Windows. Tidak ada aplikasi yang dipasang di HP: cukup scan QR dari program di laptop, lalu buka di browser. Semuanya berjalan lewat Wi-Fi atau jaringan lokal, tanpa internet.

- Tanpa APK di HP, pairing cukup scan QR
- Touchpad dengan gestur 1 sampai 4 jari, keyboard HP dengan tombol laptop tambahan
- Controller PS4 virtual dengan analog dinamis, getaran, dan tata letak yang bisa diatur (preset)
- Kontrol volume dan kecerahan layar
- Bisa dipakai 2 HP sekaligus
- Antarmuka berbahasa Indonesia

## Unduh

| Komponen | Link | Keterangan |
|---|---|---|
| **PCRemote.exe** (versi terbaru) | [Unduh PCRemote.exe](https://github.com/Ceryann/PC-Remote/releases/latest/download/PCRemote.exe) | Wajib. Windows 10/11 64-bit. Tanpa instalasi, cukup klik dua kali. |
| **Driver ViGEmBus** | [Unduh ViGEmBus 1.22.0](https://github.com/nefarius/ViGEmBus/releases/download/v1.22.0/ViGEmBus_1.22.0_x64_x86_arm64.exe) | Hanya untuk tab **Controller**. Pasang sekali saja. Touchpad dan keyboard tidak membutuhkannya. |

Semua versi ada di halaman [Releases](https://github.com/Ceryann/PC-Remote/releases). Halaman resmi driver: [ViGEmBus Releases](https://github.com/nefarius/ViGEmBus/releases).

> Windows SmartScreen bisa menampilkan peringatan "tidak dikenal" untuk file .exe baru. Pilih **More info**, lalu **Run anyway**.

## Mulai cepat

> **Penting:** jalankan PCRemote.exe dengan **Run as administrator**. Tanpa hak administrator, Windows memblokir input ke game, Task Manager, dan jendela lain yang berjalan sebagai administrator, sehingga touchpad dan keyboard tidak berfungsi di sana. Tips: agar tidak perlu klik kanan setiap kali, klik kanan file, pilih **Properties**, buka tab **Compatibility**, centang **Run this program as an administrator**, lalu **OK**.

1. Unduh **PCRemote.exe**, lalu jalankan dengan **klik kanan, Run as administrator** (jawab **Yes** di pop-up UAC). Jendela hitam akan menampilkan **QR code**.
2. Kalau muncul jendela Windows Firewall, centang **Private networks** lalu **Allow access**.
3. Pastikan HP dan laptop ada di **Wi-Fi atau router yang sama**.
4. Scan QR dengan kamera HP, lalu buka link-nya di browser.
5. Kalau di bagian atas halaman muncul **Connected** (titik hijau), kamu siap memakainya.

Jendela hitam harus tetap terbuka selama dipakai. Menutupnya menghentikan server. Alamat dan token berubah setiap server dijalankan ulang, jadi scan QR lagi setelah menjalankan ulang.

## Panduan dan fitur

### Touchpad

| Gestur | Aksi |
|---|---|
| 1 jari geser | Gerakkan kursor |
| 1 jari tap | Klik kiri |
| 1 jari tahan, lalu geser | Drag and drop |
| 2 jari tap | Klik kanan |
| 2 jari geser | Scroll (atas-bawah dan kiri-kanan) |
| 2 jari pinch | Zoom (Ctrl + scroll) |
| 3 jari tap | Klik tengah |
| 3 jari geser kanan / kiri | Alt+Tab / Alt+Shift+Tab |
| 3 jari geser atas / bawah | Task View / Tampilkan desktop |
| 4 jari tap | Tampilkan desktop (Win+D) |
| 4 jari geser kiri / kanan | Pindah virtual desktop |
| 4 jari geser atas / bawah | Task View / Tampilkan desktop |

### Keyboard

- Ketuk kotak teks, lalu ketik dengan **keyboard bawaan HP**. Teks langsung muncul di laptop. **Enter** mengirim baris baru dan mengosongkan kotak.
- Di atas kotak ada tombol laptop: **Ctrl, Alt, Shift, Win** (tap untuk mengaktifkan, otomatis lepas setelah dipakai), **Esc, Tab, Start, Backspace, Del, Enter**, panah, **Home, End, PgUp, PgDn, PrtSc**, dan **F1 sampai F12** (geser baris F ke samping).
- Tombol Backspace, Del, panah, PgUp, dan PgDn berulang otomatis kalau ditahan.
- Kombinasi tombol: aktifkan modifier lalu tekan tombol berikutnya. Contoh **Alt+Tab**: tap **Alt**, lalu **Tab**. Contoh **Ctrl+C**: tap **Ctrl**, lalu ketik huruf **c** di keyboard HP.
- Karakter yang didukung hanya ASCII (tanpa emoji atau huruf beraksen).

### Controller

- Laptop mengenali HP sebagai **Wireless Controller (DualShock 4)**. Butuh driver ViGEmBus.
- Tombol lengkap: ✕ ○ □ △, L1/R1, L2/R2 (analog), L3/R3, Share, Options, PS, **Touchpad** (hanya klik seperti menekan touchpad DualShock 4, area sentuhnya tidak aktif), dan D-Pad.
- **Analog dinamis**: sentuh area kosong di separuh kiri layar untuk analog kiri, atau separuh kanan untuk analog kanan. Lingkaran analog muncul di titik sentuhmu, seperti game mobile. Bisa diganti ke analog tetap.
- **L2/R2** terkirim penuh saat ditekan. Geser jari ke atas sambil menahan untuk mengurangi nilainya.
- **Getaran** tombol bisa diatur di Pengaturan.
- Layar otomatis masuk fullscreen dan landscape saat membuka tab Controller.

**Atur tata letak** (tombol di bagian bawah layar Controller):
- Seret tombol ke posisi yang kamu mau.
- Sentuh sebuah tombol sampai terpilih (garis biru), lalu pakai **Tombol +/-** untuk mengubah ukuran tombol itu saja. **Semua +/-** mengubah ukuran semua tombol.
- **Preset**: simpan beberapa tata letak (Preset 1, Preset 2, dan seterusnya). **+ Preset** membuat preset baru dari salinan yang sedang aktif (maksimal 8). **Hapus preset** menghapus yang aktif.
- **Reset** mengembalikan preset yang aktif ke tata letak bawaan.
- **Analog: Dinamis/Tetap** untuk mengganti mode analog.

### Sistem

- Volume dan kecerahan memakai **bar geser** seperti panel volume Windows: ikon di kiri, tombol **-** dan **+** di sisi bar (tiap ketukan 2%, tahan untuk mengulang), dan angka persen di kanan.
- **Volume**: ketuk **ikon speaker** untuk Mute / Unmute. Volume dibaca dan diatur lewat Windows Core Audio (dijalankan lewat PowerShell di balik layar). Kalau gagal, bar dinonaktifkan dan tombol -/+ memakai tombol volume bawaan Windows.
- **Kecerahan layar**: bar yang sama (5% sampai 100%). Hanya untuk layar bawaan laptop. Monitor eksternal dan PC desktop biasanya tidak didukung.

### Pengaturan

Sensitivitas kursor, kecepatan scroll, deadzone analog, ukuran semua tombol controller, dan durasi getaran (0 = mati). Semua disimpan di HP dan bertahan antar sesi.

### Dua HP sekaligus

- Maksimal 2 HP tersambung bersamaan, keduanya memakai QR yang sama.
- Setiap HP mendapat controller virtual sendiri: **Player 1** dan **Player 2** (tampil di status, misalnya `Connected · P2 · 12 ms`).
- Mouse dan keyboard dipakai bersama. HP ketiga yang tersambung menggantikan HP yang paling lama.

### Status koneksi

Di bagian atas halaman: **Connected** (hijau, beserta angka latensi dalam ms), **Reconnecting** (menyambung ulang otomatis kalau Wi-Fi sempat putus), atau **Disconnected**.

## Menyambungkan HP

HP dan laptop harus ada di jaringan lokal yang sama. Pilih salah satu:

- **Router yang sama** (paling umum). Sebaiknya pakai band **5 GHz**.
- **Hotspot HP**: laptop menyambung ke hotspot HP. Tidak butuh kuota. Atur hotspot ke 5 GHz.
- **Mobile Hotspot Windows**: HP menyambung ke hotspot laptop.
- **USB debugging** (opsional, tanpa Wi-Fi): colok kabel, aktifkan USB debugging di HP, jalankan `adb reverse tcp:8765 tcp:8765` (perlu Android Platform-Tools), lalu buka `http://localhost:8765/?token=...` di browser HP dengan token yang dicetak server.

Bluetooth tidak didukung: browser HP tidak bisa berperan sebagai mouse, keyboard, atau gamepad Bluetooth.

Keamanan: setiap sesi memakai token acak di URL, dan request tanpa token yang benar ditolak. Program hanya berjalan di jaringan lokal dan tidak membuka koneksi ke internet.

## Pemecahan masalah

| Masalah | Solusi |
|---|---|
| QR tidak terbuka atau HP tidak bisa terhubung | Pastikan satu jaringan. Izinkan di Firewall (centang Private). Wi-Fi tamu sering memisahkan perangkat, jadi pakai jaringan utama atau hotspot. Server juga mencetak alamat alternatif di jendela hitam. |
| Input tidak jalan di game, Task Manager, atau jendela lain | Pastikan **PCRemote.exe dijalankan sebagai Administrator** (klik kanan, Run as administrator). Pop-up UAC tidak bisa dikontrol program mana pun, jawab langsung di laptop. Game dengan anti-cheat sering memblokir input mouse dan keyboard, jadi pakai tab Controller. |
| Controller tidak terdeteksi | Pasang **ViGEmBus**, lalu jalankan ulang PCRemote.exe. Cek di Windows **Set up USB game controllers** apakah muncul Wireless Controller. |
| Kadang lag atau delay | Perhatikan angka ms di atas. Pakai 5 GHz, matikan hemat baterai di HP, colok charger laptop, dan jauhkan dari unduhan besar di jaringan yang sama. |
| Kecerahan tidak berubah | Fitur ini hanya untuk layar bawaan laptop. Pastikan PCRemote.exe dijalankan sebagai Administrator. |
| Teks tidak muncul | Hanya karakter ASCII yang didukung. |

## Untuk pengembang

Server memakai Python (FastAPI, uvicorn, pyautogui, vgamepad) dan klien berupa satu halaman web tanpa dependensi eksternal.

| File | Fungsi |
|---|---|
| `server.py` | Server WebSocket, QR, token, kontrol mouse/keyboard, controller, volume, kecerahan |
| `index.html` | Halaman kontrol di HP |
| `requirements.txt` | Dependensi Python |
| `.github/workflows/build.yml` | Build `PCRemote.exe` lewat GitHub Actions |
| `README.md` / `README.en.md` | Dokumentasi (Indonesia / English) |

**Jalankan dari kode:** `pip install -r requirements.txt`, lalu `python server.py`. Variabel opsional: `PORT` (default 8765) dan `HOST_IP` (memaksa IP di QR).

**Build dan rilis:**
- Setiap push ke `main` membuat build dan menyimpannya sebagai *artifact* di tab Actions.
- Untuk merilis versi baru: buka **Releases**, **Draft a new release**, buat tag baru (misalnya `v1.1.0`), lalu **Publish release**. Dalam beberapa menit `PCRemote.exe` otomatis terlampir di release itu, dan link **Unduh** di atas langsung menunjuk ke versi terbaru.
- Workflow memasang `vgamepad` dengan menyalin paketnya karena `pip install vgamepad` macet di komputer build GitHub.

## Batasan

- Hanya Windows 10/11 (64-bit) dan klien Android.
- Tanpa streaming layar, tanpa akses lewat internet, tanpa umpan balik getar dari game ke HP, dan tanpa gyro.
