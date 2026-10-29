"""PC Remote Controller - server untuk Windows 10/11.  Jalankan: python server.py"""
import asyncio, ctypes, hmac, json, os, secrets, socket, sys
from pathlib import Path

import pyautogui, qrcode, uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, PlainTextResponse

try:
    import vgamepad as vg
except Exception:  # vgamepad / ViGEmBus belum terpasang
    vg = None

PORT = int(os.environ.get("PORT", 8765))
INVERT_STICK_Y = False  # ganti True bila sumbu Y analog terbalik di gamepad tester
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
DPAD = {"": "NONE", "n": "NORTH", "ne": "NORTHEAST", "e": "EAST", "se": "SOUTHEAST",
        "s": "SOUTH", "sw": "SOUTHWEST", "w": "WEST", "nw": "NORTHWEST"}
pad = None


def get_pad():
    global pad
    if vg is None:
        raise RuntimeError("vgamepad/ViGEmBus belum terpasang, controller tidak aktif")
    if pad is None:
        pad = vg.VDS4Gamepad()  # Windows mengenali sebagai Wireless Controller
    return pad


def clamp(v, lo=-1.0, hi=1.0):
    return max(lo, min(hi, float(v)))


def pad_event(m):
    g, t = get_pad(), m["t"]
    if t == "b":
        down = bool(m["d"])
        if m["n"] == "ps":
            sp = vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS
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


def reset_pad():
    if pad is not None:
        pad.reset()
        pad.update()


# ---------- dispatcher ----------
def handle(m):
    t = m.get("t")
    if t in ("b", "dpad", "st", "tr"):
        pad_event(m)
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
    elif t == "bs":
        pyautogui.press("backspace", presses=min(int(m["n"]), 200))


# ---------- web ----------
app = FastAPI()
active = None


def valid(token):
    return hmac.compare_digest(token.encode(), TOKEN.encode())


@app.get("/")
def index(token: str = ""):
    if not valid(token):
        return PlainTextResponse("Token tidak valid. Scan ulang QR dari server.", 403)
    return HTMLResponse((BASE / "index.html").read_text("utf-8"), headers={"Cache-Control": "no-store"})


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket, token: str = ""):
    global active
    await ws.accept()
    if not valid(token):
        await ws.close(1008)
        return
    if active is not None:  # last-one-wins: putus client lama
        try:
            await active.close(4000)
        except Exception:
            pass
    active = ws
    warned = False
    try:
        while active is ws:
            m = json.loads(await ws.receive_text())
            if not isinstance(m, dict):
                continue
            if m.get("t") == "ping":
                await ws.send_text('{"p":1}')
                continue
            try:
                handle(m)
            except Exception as e:
                if not warned:
                    warned = True
                    await ws.send_text(json.dumps({"err": f"Gagal: {e}"}))
    except (WebSocketDisconnect, RuntimeError, ValueError):
        pass
    finally:
        if active is ws:
            active = None
            reset_pad()


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
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ips = [os.environ["HOST_IP"]] if os.environ.get("HOST_IP") else lan_ips()
    url = f"http://{ips[0]}:{PORT}/?token={TOKEN}"
    q = qrcode.QRCode(border=1)
    q.add_data(url)
    q.print_ascii(invert=True)
    print(f"\nScan QR di atas dengan HP (satu Wi-Fi/router yang sama), atau buka:\n{url}\n")
    if len(ips) > 1:
        print("Jika QR tidak bisa dibuka, laptop punya jaringan lain. Coba alamat ini di HP:")
        for ip in ips[1:]:
            print(f"  http://{ip}:{PORT}/?token={TOKEN}")
        print()
    print("Jika HP tidak bisa terhubung, izinkan port di Firewall (CMD sebagai Administrator):")
    print(f'netsh advfirewall firewall add rule name="PC Remote" dir=in action=allow protocol=TCP localport={PORT} profile=private\n')
    if vg is None:
        print("Peringatan: vgamepad belum terpasang, modul Controller tidak aktif.\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
