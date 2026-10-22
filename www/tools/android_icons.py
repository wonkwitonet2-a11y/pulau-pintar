# Mengganti ikon bawaan aplikasi Android dengan ikon balok Pulau Pintar.
# Dijalankan setelah "npx cap add android".
import os, glob, zlib, struct

def png(path, n, px):
    raw = bytearray()
    for y in range(n):
        raw.append(0)
        for x in range(n):
            raw += bytes(px(x / n, y / n))
    def ch(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 2, 0, 0, 0)) \
        + ch(b"IDAT", zlib.compress(bytes(raw), 9)) + ch(b"IEND", b"")
    open(path, "wb").write(data)

BG = (46, 156, 202)
INK = (31, 42, 68)
BR = [(0.18, 0.60, 0.82, 0.76, (232, 80, 74)),
      (0.18, 0.44, 0.50, 0.60, (242, 182, 50)),
      (0.50, 0.44, 0.82, 0.60, (61, 170, 107)),
      (0.34, 0.28, 0.66, 0.44, (139, 111, 214))]
STUDS = []
for (x0, y0, x1, y1, c) in BR:
    k = max(1, round((x1 - x0) / 0.16))
    w = (x1 - x0) / k
    for i in range(k):
        STUDS.append((x0 + w * (i + 0.5), y0 - 0.03, 0.045, c))

def px(x, y):
    for (cx, cy, r, c) in STUDS:
        if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
            return c
    for (x0, y0, x1, y1, c) in BR:
        if x0 <= x <= x1 and y0 <= y <= y1:
            e = 0.012
            if x < x0 + e or x > x1 - e or y < y0 + e or y > y1 - e:
                return INK
            return c
    return BG

res = "android/app/src/main/res"
if not os.path.isdir(res):
    raise SystemExit("Folder android belum ada; jalankan setelah npx cap add android")
for d, n in [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)]:
    folder = os.path.join(res, "mipmap-" + d)
    os.makedirs(folder, exist_ok=True)
    for name in ("ic_launcher.png", "ic_launcher_round.png"):
        png(os.path.join(folder, name), n, px)
# ikon adaptif bawaan menimpa PNG di Android 8+, jadi dihapus
for f in glob.glob(os.path.join(res, "mipmap-anydpi*", "ic_launcher*.xml")):
    os.remove(f)
print("Ikon Android diganti")
