"""PC Remote Controller - server untuk Windows 10/11.  Jalankan: python server.py"""
import asyncio, base64, ctypes, hmac, json, os, queue, secrets, socket, subprocess, sys, threading
from pathlib import Path

import pyautogui, qrcode, uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, PlainTextResponse

try:
    import vgamepad as vg
except Exception:  # vgamepad / ViGEmBus belum terpasang
    vg = None

PORT = int(os.environ.get("PORT", 8765))
INVERT_STICK_Y = True  # sumbu Y analog dibalik (sudah dites: tanpa ini maju terbaca mundur)
TOKEN = secrets.token_urlsafe(6)
BASE = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
U32 = ctypes.windll.user32

# ---------- mouse ----------
BTN = {"l": (0x2, 0x4), "r": (0x8, 0x10), "m": (0x20, 0x40)}  # (down, up)
rem = [0.0, 0.0]


def mouse(flags, data=0, dx=0, dy=0):
    U32.mouse_event(flags, dx, dy, data, 0)


def move(dx, dy):  # sisa pecahan piksel disimpan agar gerakan halus
    rem[0] += dx
    rem[1] += dy
    ix, iy = int(rem[0]), int(rem[1])
    rem[0] -= ix
    rem[1] -= iy
    if ix or iy:
        mouse(0x1, 0, ix, iy)


# ---------- keyboard ----------
KEYS = set(pyautogui.KEYBOARD_KEYS)


def combo(keys):
    keys = [k for k in keys if isinstance(k, str) and k in KEYS]
    if keys:
        pyautogui.hotkey(*keys)


def type_text(s):
    for i, part in enumerate(str(s).split("\n")):
        if i:
            pyautogui.press("enter")
        if part:
            pyautogui.write(part)  # hanya karakter ASCII


# ---------- DualShock 4 ----------
PAD_BTN = {"cross": "CROSS", "circle": "CIRCLE", "square": "SQUARE", "triangle": "TRIANGLE",
           "l1": "SHOULDER_LEFT", "r1": "SHOULDER_RIGHT", "l3": "THUMB_LEFT", "r3": "THUMB_RIGHT",
           "share": "SHARE", "options": "OPTIONS"}
SPECIAL = {"ps": "DS4_SPECIAL_BUTTON_PS", "touchpad": "DS4_SPECIAL_BUTTON_TOUCHPAD"}
DPAD = {"": "NONE", "n": "NORTH", "ne": "NORTHEAST", "e": "EAST", "se": "SOUTHEAST",
        "s": "SOUTH", "sw": "SOUTHWEST", "w": "WEST", "nw": "NORTHWEST"}
MAX_CLIENTS = 2
pads = [None] * MAX_CLIENTS  # satu DualShock 4 virtual per client (Player 1 dan 2)


def get_pad(slot):
    if vg is None:
        raise RuntimeError("vgamepad/ViGEmBus belum terpasang, controller tidak aktif")
    if pads[slot] is None:
        pads[slot] = vg.VDS4Gamepad()  # Windows mengenali sebagai Wireless Controller
    return pads[slot]


def clamp(v, lo=-1.0, hi=1.0):
    return max(lo, min(hi, float(v)))


def pad_event(m, slot):
    g, t = get_pad(slot), m["t"]
    if t == "b":
        down = bool(m["d"])
        if m["n"] in SPECIAL:
            sp = getattr(vg.DS4_SPECIAL_BUTTONS, SPECIAL[m["n"]])
            (g.press_special_button if down else g.release_special_button)(sp)
        else:
            btn = getattr(vg.DS4_BUTTONS, "DS4_BUTTON_" + PAD_BTN[m["n"]])
            (g.press_button if down else g.release_button)(btn)
    elif t == "dpad":
        g.directional_pad(getattr(vg.DS4_DPAD_DIRECTIONS, "DS4_BUTTON_DPAD_" + DPAD[m["v"]]))
    elif t == "st":
        x, y = clamp(m["x"]), clamp(m["y"])
        y = -y if INVERT_STICK_Y else y
        (g.left_joystick_float if m["s"] == "l" else g.right_joystick_float)(x, y)
    elif t == "tr":
        (g.left_trigger_float if m["s"] == "l" else g.right_trigger_float)(clamp(m["v"], 0, 1))
    g.update()


def reset_pad(slot):
    if pads[slot] is not None:
        pads[slot].reset()
        pads[slot].update()


# ---------- kecerahan (WMI, hanya layar bawaan laptop) ----------
_bright = {"want": None}
_bright_ev = threading.Event()


def ps(cmd, timeout=10):
    return subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                          capture_output=True, text=True, timeout=timeout, creationflags=0x08000000)


def get_brightness():
    """Kecerahan saat ini (0-100), atau None bila layar tidak mendukung."""
    try:
        r = ps("Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness | Select-Object -First 1 -ExpandProperty CurrentBrightness")
        out = r.stdout.strip()
        return int(out.splitlines()[0]) if r.returncode == 0 and out else None
    except Exception:
        return None


def _bright_loop():  # hanya nilai terbaru yang dikerjakan, supaya geseran slider tidak menumpuk perintah
    while True:
        _bright_ev.wait()
        _bright_ev.clear()
        try:
            ps("Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods | "
               f"Invoke-CimMethod -MethodName WmiSetBrightness -Arguments @{{Timeout=1;Brightness={int(_bright['want'])}}}")
        except Exception:
            pass


threading.Thread(target=_bright_loop, daemon=True).start()


def set_brightness(v):
    _bright["want"] = max(5, min(100, int(float(v))))  # minimal 5 agar layar tidak terlalu gelap
    _bright_ev.set()


# ---------- volume (Windows Core Audio lewat PowerShell yang tetap hidup) ----------
AUDIO_PS = r'''
$src = @'
using System;
using System.Runtime.InteropServices;
[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {
  int f(); int g(); int h(); int i();
  int SetMasterVolumeLevelScalar(float fLevel, Guid pguidEventContext);
  int j();
  int GetMasterVolumeLevelScalar(out float pfLevel);
  int k(); int l(); int m(); int n();
  int SetMute([MarshalAs(UnmanagedType.Bool)] bool bMute, Guid pguidEventContext);
  int GetMute([MarshalAs(UnmanagedType.Bool)] out bool pbMute);
}
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {
  int Activate(ref Guid id, int clsCtx, IntPtr activationParams, out IAudioEndpointVolume aev);
}
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {
  int f();
  int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
}
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorComObject { }
public class Audio {
  static IAudioEndpointVolume Vol() {
    var en = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
    IMMDevice dev = null;
    Marshal.ThrowExceptionForHR(en.GetDefaultAudioEndpoint(0, 1, out dev));
    IAudioEndpointVolume epv = null;
    var id = typeof(IAudioEndpointVolume).GUID;
    Marshal.ThrowExceptionForHR(dev.Activate(ref id, 23, IntPtr.Zero, out epv));
    return epv;
  }
  public static float Volume {
    get { float v = -1; Marshal.ThrowExceptionForHR(Vol().GetMasterVolumeLevelScalar(out v)); return v; }
    set { Marshal.ThrowExceptionForHR(Vol().SetMasterVolumeLevelScalar(value, Guid.Empty)); }
  }
  public static bool Mute {
    get { bool m; Marshal.ThrowExceptionForHR(Vol().GetMute(out m)); return m; }
    set { Marshal.ThrowExceptionForHR(Vol().SetMute(value, Guid.Empty)); }
  }
}
'@
Add-Type -TypeDefinition $src
while ($true) {
  $l = [Console]::In.ReadLine()
  if ($l -eq $null) { break }
  try {
    $p = $l.Trim().Split(' ')
    if ($p[0] -eq 'set') {
      [Audio]::Volume = [float]$p[1] / 100
      if (([float]$p[1] -gt 0) -and [Audio]::Mute) { [Audio]::Mute = $false }
    }
    elseif ($p[0] -eq 'toggle') { [Audio]::Mute = -not [Audio]::Mute }
    $v = [int][math]::Round([Audio]::Volume * 100)
    $m = 0
    if ([Audio]::Mute) { $m = 1 }
    [Console]::Out.WriteLine("OK $v $m")
  } catch { [Console]::Out.WriteLine('ERR') }
  [Console]::Out.Flush()
}
'''


class AudioHelper:
    """Proses PowerShell yang tetap hidup untuk membaca/mengatur volume master (dikompilasi sekali saja)."""

    def __init__(self):
        self.p = None
        self.q = None
        self.lock = threading.Lock()

    def _start(self):
        enc = base64.b64encode(AUDIO_PS.encode("utf-16-le")).decode()
        self.p = subprocess.Popen(
            ["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", enc],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, bufsize=1, creationflags=0x08000000)
        self.q = queue.Queue()
        threading.Thread(target=self._reader, args=(self.p, self.q), daemon=True).start()

    @staticmethod
    def _reader(p, q):
        for line in p.stdout:
            line = line.strip()
            if line.startswith(("OK", "ERR")):
                q.put(line)

    def ask(self, cmd):
        """cmd: get | set N | toggle. Hasil: {"v": 0-100, "m": mute} atau None bila gagal."""
        with self.lock:
            try:
                if self.p is None or self.p.poll() is not None:
                    self._start()
                self.p.stdin.write(cmd + "\n")
                self.p.stdin.flush()
                line = self.q.get(timeout=20)  # panggilan pertama lebih lama (kompilasi)
            except Exception:
                try:
                    self.p.kill()
                except Exception:
                    pass
                self.p = None
                return None
        if line.startswith("OK"):
            _, v, m = line.split()
            return {"v": int(v), "m": bool(int(m))}
        return None


audio = AudioHelper()
_tasks = set()


async def audio_dispatch(ws, m):
    try:
        if m["t"] == "vset":  # tanpa balasan; klien sudah menampilkan nilainya
            await asyncio.to_thread(audio.ask, f"set {max(0, min(100, int(float(m['v']))))}")
            return
        res = await asyncio.to_thread(audio.ask, "get" if m["t"] == "vget" else "toggle")
        await ws.send_text(json.dumps({"vol": res}))
    except Exception:
        pass


# ---------- dispatcher ----------
def handle(m, slot):
    t = m.get("t")
    if t in ("b", "dpad", "st", "tr"):
        pad_event(m, slot)
    elif t == "mv":
        move(float(m["dx"]), float(m["dy"]))
    elif t == "click":
        a, b = BTN[m["b"]]
        mouse(a)
        mouse(b)
    elif t in ("down", "up"):
        mouse(BTN[m["b"]][0 if t == "down" else 1])
    elif t == "scroll":
        if int(m.get("dy", 0)):
            mouse(0x800, int(m["dy"]))
        if int(m.get("dx", 0)):
            mouse(0x1000, int(m["dx"]))
    elif t == "zoom":
        pyautogui.keyDown("ctrl")
        mouse(0x800, int(m["d"]))
        pyautogui.keyUp("ctrl")
    elif t == "keys":
        combo(m["k"])
    elif t == "text":
        type_text(m["s"])
    elif t == "vol":  # n > 0 naik, n < 0 turun; tiap langkah sekitar 2%
        n = int(m["n"])
        if n:
            pyautogui.press("volumeup" if n > 0 else "volumedown", presses=min(abs(n), 25))
    elif t == "bset":
        set_brightness(m["v"])
    elif t == "bs":
        pyautogui.press("backspace", presses=min(int(m["n"]), 200))


# ---------- web ----------
app = FastAPI()
clients = {}  # ws -> nomor slot (0 atau 1), berurut dari yang paling lama


def valid(token):
    return hmac.compare_digest(token.encode(), TOKEN.encode())


@app.get("/")
def index(token: str = ""):
    if not valid(token):
        return PlainTextResponse("Token tidak valid. Scan ulang QR dari server.", 403)
    return HTMLResponse((BASE / "index.html").read_text("utf-8"), headers={"Cache-Control": "no-store"})


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket, token: str = ""):
    await ws.accept()
    if not valid(token):
        await ws.close(1008)
        return
    while len(clients) >= MAX_CLIENTS:  # penuh: putus client yang paling lama
        old = next(iter(clients))
        reset_pad(clients.pop(old))
        try:
            await old.close(4000)
        except Exception:
            pass
    slot = next(i for i in range(MAX_CLIENTS) if i not in clients.values())
    clients[ws] = slot
    warned = False
    try:
        await ws.send_text(json.dumps({"hello": 1, "slot": slot + 1}))
        while ws in clients:
            m = json.loads(await ws.receive_text())
            if not isinstance(m, dict):
                continue
            if m.get("t") == "ping":
                await ws.send_text('{"p":1}')
                continue
            if m.get("t") == "bget":
                await ws.send_text(json.dumps({"bright": await asyncio.to_thread(get_brightness)}))
                continue
            if m.get("t") in ("vget", "vset", "vmute"):
                task = asyncio.create_task(audio_dispatch(ws, m))
                _tasks.add(task)
                task.add_done_callback(_tasks.discard)
                continue
            try:
                handle(m, slot)
            except Exception as e:
                if not warned:
                    warned = True
                    await ws.send_text(json.dumps({"err": f"Gagal: {e}"}))
    except (WebSocketDisconnect, RuntimeError, ValueError):
        pass
    finally:
        if clients.pop(ws, None) is not None:
            reset_pad(slot)


def boost():
    """Kurangi lonjakan delay: prioritas lebih tinggi, matikan throttling daya, timer 1 ms."""
    try:
        k = ctypes.windll.kernel32
        h = k.GetCurrentProcess()
        k.SetPriorityClass(h, 0x00008000)  # ABOVE_NORMAL_PRIORITY_CLASS

        class Throttle(ctypes.Structure):
            _fields_ = [("Version", ctypes.c_ulong), ("ControlMask", ctypes.c_ulong), ("StateMask", ctypes.c_ulong)]

        st = Throttle(1, 1, 0)  # EXECUTION_SPEED dikontrol, state 0 = throttling mati
        k.SetProcessInformation(h, 4, ctypes.byref(st), ctypes.sizeof(st))  # ProcessPowerThrottling
        ctypes.windll.winmm.timeBeginPeriod(1)
    except Exception:
        pass  # tidak fatal; server tetap jalan


def lan_ips():
    """Semua alamat IPv4 laptop di jaringan lokal (router Wi-Fi, hotspot, dll)."""
    ips = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # UDP: tidak ada paket yang dikirim
        ips.append(s.getsockname()[0])
    except OSError:
        pass
    finally:
        s.close()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if ip not in ips and not ip.startswith(("127.", "169.254.")):
                ips.append(ip)
    except OSError:
        pass
    return ips or ["127.0.0.1"]


if __name__ == "__main__":
    boost()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ips = [os.environ["HOST_IP"]] if os.environ.get("HOST_IP") else lan_ips()
    url = f"http://{ips[0]}:{PORT}/?token={TOKEN}"
    q = qrcode.QRCode(border=1)
    q.add_data(url)
    q.print_ascii(invert=True)
    print(f"\nScan QR di atas dengan HP (satu Wi-Fi/router yang sama, maksimal 2 HP), atau buka:\n{url}\n")
    if len(ips) > 1:
        print("Jika QR tidak bisa dibuka, laptop punya jaringan lain. Coba alamat ini di HP:")
        for ip in ips[1:]:
            print(f"  http://{ip}:{PORT}/?token={TOKEN}")
        print()
    print("Jika HP tidak bisa terhubung, izinkan port di Firewall (CMD sebagai Administrator):")
    print(f'netsh advfirewall firewall add rule name="PC Remote" dir=in action=allow protocol=TCP localport={PORT} profile=private\n')
    if vg is None:
        print("Peringatan: driver ViGEmBus belum terpasang (atau vgamepad gagal dimuat), modul Controller tidak aktif.")
        print("Touchpad dan keyboard tetap berfungsi. Pasang ViGEmBus lalu jalankan ulang untuk Controller.\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
