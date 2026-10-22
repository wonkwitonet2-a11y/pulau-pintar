# Membuat ikon app (balok warna-warni) tanpa pustaka tambahan.
import zlib, struct

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
# balok: (x0, y0, x1, y1, warna) dalam skala 0..1, area aman di tengah
BR = [(0.22, 0.58, 0.78, 0.72, (232, 80, 74)),
      (0.22, 0.44, 0.50, 0.58, (242, 182, 50)),
      (0.50, 0.44, 0.78, 0.58, (61, 170, 107)),
      (0.36, 0.30, 0.64, 0.44, (139, 111, 214))]
STUDS = []
for (x0, y0, x1, y1, c) in BR:
    k = max(1, round((x1 - x0) / 0.14))
    w = (x1 - x0) / k
    for i in range(k):
        STUDS.append((x0 + w * (i + 0.5), y0 - 0.025, 0.04, c))

def px(x, y):
    for (cx, cy, r, c) in STUDS:
        if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
            return c
    for (x0, y0, x1, y1, c) in BR:
        if x0 <= x <= x1 and y0 <= y <= y1:
            e = 0.008
            if x < x0 + e or x > x1 - e or y < y0 + e or y > y1 - e:
                return INK
            return c
    return BG

png("www/icon-192.png", 192, px)
png("www/icon-512.png", 512, px)
print("Ikon dibuat")
