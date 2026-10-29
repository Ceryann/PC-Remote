# PC Remote Controller

HP Android jadi touchpad, keyboard, dan gamepad PS4 untuk laptop Windows. Tanpa APK, tanpa internet.

## Menjalankan
1. `pip install -r requirements.txt` (vgamepad memasang driver ViGEmBus, setujui prompt-nya)
2. `python server.py`
3. Scan QR di terminal dengan HP yang satu Wi-Fi.

Jika HP tidak bisa terhubung, jalankan perintah `netsh` yang dicetak server (CMD sebagai Administrator).

## Cara menyambungkan HP dan laptop
Keduanya harus ada di jaringan lokal yang sama. Pilih salah satu:

| Cara | Langkah |
|---|---|
| **Router yang sama** (paling stabil) | Sambungkan HP dan laptop ke Wi-Fi/router yang sama, jalankan server, scan QR. |
| **Hotspot HP** | Hidupkan hotspot di HP, sambungkan laptop ke sana. Tidak butuh kuota karena hanya lokal. |
| **Hotspot Windows** | Hidupkan Mobile Hotspot di laptop, sambungkan HP ke sana. |

Jika QR tidak terbuka:
- Server mencetak alamat alternatif bila laptop punya lebih dari satu jaringan. Coba satu per satu di browser HP.
- Atau paksa IP: `set HOST_IP=192.168.x.x` sebelum menjalankan server (cek IP lewat `ipconfig`).
- Wi-Fi tamu (guest) atau Wi-Fi publik sering memisahkan antar perangkat (client isolation), jadi HP dan laptop tidak saling terlihat. Pakai jaringan utama atau hotspot.
- Pastikan jaringan di Windows bertipe **Private** dan port sudah diizinkan di Firewall (perintah `netsh` dicetak server).

Bluetooth tidak didukung: browser HP tidak bisa berperan sebagai mouse/keyboard/gamepad Bluetooth.

## Gestur touchpad
| Gestur | Aksi |
|---|---|
| 1 jari geser / tap | Kursor / klik kiri |
| Tahan lalu geser | Drag & drop |
| 2 jari tap / geser / pinch | Klik kanan / scroll / zoom (Ctrl+scroll) |
| 3 jari tap | Klik tengah |
| 3 jari geser kanan/kiri | Alt+Tab / Alt+Shift+Tab |
| 3 jari geser atas/bawah | Task View / Show desktop |
| 4 jari tap | Show desktop (Win+D) |
| 4 jari geser kiri/kanan | Pindah virtual desktop |
| 4 jari geser atas/bawah | Task View / Show desktop |

Mapping 3 dan 4 jari ada di `touchend` pada `index.html`, mudah diubah.

## Controller
- Tab Controller masuk fullscreen + landscape. Posisi tombol bisa digeser lewat "Atur tata letak".
- L2/R2 analog: tekan = penuh, geser jari ke atas = dilepas pelan.
- Verifikasi: Windows > "Set Up USB Game Controllers" harus menampilkan **Wireless Controller**.
- Jika sumbu Y analog terbalik, ubah `INVERT_STICK_Y = True` di `server.py`.

## Build satu file .exe
```
pip install pyinstaller
pyinstaller --onefile --name PCRemote --add-data "index.html;." --collect-all vgamepad --collect-submodules uvicorn server.py
```

## Batasan v1
- Ketikan hanya karakter ASCII (tanpa emoji/aksen).
- 1 client aktif; client baru memutus client lama.
