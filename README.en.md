# PC Remote

**Language:** [Bahasa Indonesia](README.md) | English

PC Remote turns an Android phone into a **touchpad, keyboard, and PS4 (DualShock 4) gamepad** for a Windows laptop. Nothing is installed on the phone: just scan a QR code shown by the program on your laptop and open it in the browser. Everything runs over Wi-Fi or your local network, with no internet needed.

- No APK on the phone, pairing is just a QR scan
- Touchpad with 1 to 4 finger gestures, phone keyboard with extra laptop keys
- Virtual PS4 controller with a floating (dynamic) analog stick, haptic feedback, and customizable layouts (presets)
- Volume and screen brightness controls
- Works with 2 phones at the same time
- The app interface is in Indonesian (this guide gives the English meaning of each label)

## Download

| Component | Link | Notes |
|---|---|---|
| **PCRemote.exe** (latest version) | [Download PCRemote.exe](https://github.com/Ceryann/PC-Remote/releases/latest/download/PCRemote.exe) | Required. Windows 10/11 64-bit. No installation, just double-click. |
| **ViGEmBus driver** | [Download ViGEmBus 1.22.0](https://github.com/nefarius/ViGEmBus/releases/download/v1.22.0/ViGEmBus_1.22.0_x64_x86_arm64.exe) | Only needed for the **Controller** tab. Install it once. The touchpad and keyboard do not need it. |

All versions are on the [Releases](https://github.com/Ceryann/PC-Remote/releases) page. Official driver page: [ViGEmBus Releases](https://github.com/nefarius/ViGEmBus/releases).

> Windows SmartScreen may show an "unrecognized app" warning for a new .exe file. Click **More info**, then **Run anyway**.

## Quick start

> **Important:** run PCRemote.exe with **Run as administrator**. Without administrator rights, Windows blocks input to games, Task Manager, and other windows that run as administrator, so the touchpad and keyboard will not work there. Tip: to avoid right-clicking every time, right-click the file, choose **Properties**, open the **Compatibility** tab, tick **Run this program as an administrator**, then click **OK**.

1. Download **PCRemote.exe**, then run it with **right-click, Run as administrator** (click **Yes** on the UAC prompt). A black window shows a **QR code**.
2. If a Windows Firewall window appears, tick **Private networks** and click **Allow access**.
3. Make sure your phone and laptop are on the **same Wi-Fi or router**.
4. Scan the QR code with your phone camera and open the link in the browser.
5. When **Connected** (green dot) appears at the top of the page, you are ready to go.

Keep the black window open while using the remote. Closing it stops the server. The address and token change every time the server is restarted, so scan the QR code again after restarting.

## Guide and features

### Touchpad

| Gesture | Action |
|---|---|
| 1 finger swipe | Move the cursor |
| 1 finger tap | Left click |
| 1 finger press and hold, then swipe | Drag and drop |
| 2 finger tap | Right click |
| 2 finger swipe | Scroll (vertical and horizontal) |
| 2 finger pinch | Zoom (Ctrl + scroll) |
| 3 finger tap | Middle click |
| 3 finger swipe right / left | Alt+Tab / Alt+Shift+Tab |
| 3 finger swipe up / down | Task View / Show desktop |
| 4 finger tap | Show desktop (Win+D) |
| 4 finger swipe left / right | Switch virtual desktop |
| 4 finger swipe up / down | Task View / Show desktop |

### Keyboard

- Tap the text box, then type with your **phone's own keyboard**. The text appears on the laptop right away. **Enter** sends a new line and clears the box.
- Above the box are laptop keys: **Ctrl, Alt, Shift, Win** (tap to arm, released automatically after one use), **Esc, Tab, Start, Backspace, Del, Enter**, arrow keys, **Home, End, PgUp, PgDn, PrtSc**, and **F1 to F12** (swipe the F-key row sideways).
- Backspace, Del, the arrow keys, PgUp, and PgDn repeat automatically while held.
- Key combinations: arm a modifier, then press the next key. Example **Alt+Tab**: tap **Alt**, then **Tab**. Example **Ctrl+C**: tap **Ctrl**, then type the letter **c** on the phone keyboard.
- Only ASCII characters are supported (no emoji or accented letters).

### Controller

- The laptop sees your phone as a **Wireless Controller (DualShock 4)**. Requires the ViGEmBus driver.
- Full set of buttons: ✕ ○ □ △, L1/R1, L2/R2 (analog), L3/R3, Share, Options, PS, **Touchpad** (click only, like pressing the DualShock 4 touchpad; its touch surface is not active), and the D-pad.
- **Dynamic analog sticks**: touch an empty area on the left half of the screen for the left stick, or the right half for the right stick. The stick circle appears where you touch, like in mobile games. You can switch to fixed sticks.
- **L2/R2** are sent fully pressed. Slide your finger upward while holding to reduce the value.
- **Haptic feedback** on buttons can be adjusted in Settings.
- The screen automatically goes fullscreen and landscape when you open the Controller tab.

**Edit layout** (the button at the bottom of the Controller screen, labeled **Atur tata letak**):
- Drag buttons to where you want them.
- Touch a button until it is selected (blue outline), then use **Tombol +/-** (Button +/-) to resize only that button. **Semua +/-** (All +/-) resizes every button.
- **Presets**: save several layouts (Preset 1, Preset 2, and so on). **+ Preset** creates a new preset as a copy of the active one (up to 8). **Hapus preset** (Delete preset) deletes the active one.
- **Reset** restores the active preset to the default layout.
- **Analog: Dinamis/Tetap** (Dynamic/Fixed) switches the analog stick mode.

### System (tab **Sistem**)

- Volume and brightness use **sliders** like the Windows volume panel: an icon on the left, **-** and **+** buttons beside the slider (2% per tap, hold to repeat), and the percentage on the right.
- **Volume**: tap the **speaker icon** to Mute / Unmute. Volume is read and set through Windows Core Audio (run via PowerShell in the background). If that fails, the slider is disabled and the -/+ buttons use the standard Windows volume keys instead.
- **Screen brightness**: the same slider (5% to 100%). Works only on the laptop's built-in display. External monitors and desktop PCs are usually not supported.

### Settings (tab **Pengaturan**)

Cursor sensitivity, scroll speed, analog deadzone, size of all controller buttons, and haptic duration (0 = off). Everything is stored on the phone and kept between sessions.

### Two phones at once

- Up to 2 phones can be connected at the same time, both using the same QR code.
- Each phone gets its own virtual controller: **Player 1** and **Player 2** (shown in the status bar, for example `Connected · P2 · 12 ms`).
- The mouse and keyboard are shared. A third phone that connects replaces the one that has been connected the longest.

### Connection status

At the top of the page: **Connected** (green, with the latency in ms), **Reconnecting** (reconnects automatically if Wi-Fi drops briefly), or **Disconnected**.

## Connecting your phone

The phone and the laptop must be on the same local network. Pick one:

- **Same router** (most common). Prefer the **5 GHz** band.
- **Phone hotspot**: the laptop connects to your phone's hotspot. No mobile data needed. Set the hotspot to 5 GHz.
- **Windows Mobile Hotspot**: the phone connects to the laptop's hotspot.
- **USB debugging** (optional, no Wi-Fi): plug in the cable, enable USB debugging on the phone, run `adb reverse tcp:8765 tcp:8765` (needs Android Platform-Tools), then open `http://localhost:8765/?token=...` in the phone browser using the token printed by the server.

Bluetooth is not supported: a phone browser cannot act as a Bluetooth mouse, keyboard, or gamepad.

Security: every session uses a random token in the URL, and requests without the correct token are rejected. The program only runs on the local network and does not make connections to the internet.

## Troubleshooting

| Problem | Solution |
|---|---|
| The QR code will not open or the phone cannot connect | Make sure both are on the same network. Allow the app in Firewall (tick Private). Guest Wi-Fi often isolates devices, so use the main network or a hotspot. The server also prints alternative addresses in the black window. |
| Input does not work in a game, Task Manager, or another window | Make sure **PCRemote.exe is run as Administrator** (right-click, Run as administrator). No program can control a UAC prompt, so answer it directly on the laptop. Games with anti-cheat often block mouse and keyboard input, so use the Controller tab. |
| The controller is not detected | Install **ViGEmBus**, then restart PCRemote.exe. In Windows, open **Set up USB game controllers** and check that a Wireless Controller appears. |
| Occasional lag or delay | Watch the ms number at the top. Use 5 GHz, turn off battery saver on the phone, plug in the laptop charger, and avoid large downloads on the same network. |
| Brightness does not change | This only works on the laptop's built-in display. Make sure PCRemote.exe is run as Administrator. |
| Text does not appear | Only ASCII characters are supported. |

## For developers

The server uses Python (FastAPI, uvicorn, pyautogui, vgamepad) and the client is a single web page with no external dependencies.

| File | Purpose |
|---|---|
| `server.py` | WebSocket server, QR code, token, mouse/keyboard control, controller, volume, brightness |
| `index.html` | The control page shown on the phone |
| `requirements.txt` | Python dependencies |
| `.github/workflows/build.yml` | Builds `PCRemote.exe` with GitHub Actions |
| `README.md` / `README.en.md` | Documentation (Indonesian / English) |

**Run from source:** `pip install -r requirements.txt`, then `python server.py`. Optional environment variables: `PORT` (default 8765) and `HOST_IP` (forces the IP used in the QR code).

**Build and release:**
- Every push to `main` creates a build and stores it as an *artifact* in the Actions tab.
- To release a new version: open **Releases**, **Draft a new release**, create a new tag (for example `v1.1.0`), then **Publish release**. Within a few minutes `PCRemote.exe` is attached to that release automatically, and the **Download** link above points to the latest version.
- The workflow installs `vgamepad` by copying its package, because `pip install vgamepad` hangs on the GitHub build machine.

## Limitations

- Windows 10/11 (64-bit) and Android clients only.
- No screen streaming, no access over the internet, no rumble feedback from the game to the phone, and no gyro.
