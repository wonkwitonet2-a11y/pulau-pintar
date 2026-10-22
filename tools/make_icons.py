# Menggambar ikon "Pulau Pintar" (pulau, pohon kelapa, kucing detektif berkumis).
# Butuh Pillow. Hanya dijalankan manual saat ikon ingin diubah:
#   pip install pillow && python3 tools/make_icons.py
# Hasilnya (PNG) disimpan di repo, jadi proses build tidak perlu menjalankannya.
import math, os
from PIL import Image, ImageDraw

K = 2                      # supersampling agar tepi halus
W = 1024
INK = (31, 42, 68)
SEA = (46, 156, 202)
SEA_LIGHT = (120, 205, 232)
SAND = (255, 217, 122)
SAND_DARK = (240, 190, 90)
LEAF = (61, 170, 107)
LEAF_DARK = (44, 138, 86)
TRUNK = (176, 120, 70)
CAT = (245, 166, 80)
CAT_LIGHT = (255, 226, 190)
PINK = (255, 138, 120)
SUN = (255, 205, 60)
OL = 14                    # tebal garis tepi (skala 1024)


def s(v):
    return v * K


def pts(points):
    return [(s(x), s(y)) for x, y in points]


def outline_poly(d, points, fill, width=OL):
    p = pts(points)
    d.polygon(p, fill=fill)
    d.line(p + [p[0]], fill=INK, width=s(width), joint="curve")


def outline_ellipse(d, box, fill, width=OL):
    d.ellipse([s(v) for v in box], fill=fill, outline=INK, width=s(width))


def bezier(p0, p1, p2, n=24):
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


def ribbon(center, w0, w1):
    left, right = [], []
    for i, (x, y) in enumerate(center):
        a = center[min(i + 1, len(center) - 1)]
        b = center[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        w = w0 + (w1 - w0) * i / (len(center) - 1)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def frond(d, base, angle, length, droop, width, fill):
    a = math.radians(angle)
    tip = (base[0] + math.cos(a) * length, base[1] + math.sin(a) * length + droop)
    mid = (base[0] + math.cos(a) * length * 0.55, base[1] + math.sin(a) * length * 0.55 - droop * 0.9)
    c = bezier(base, mid, tip)
    shape = ribbon(c, width, 2)
    # lebar daun membesar di tengah: kecilkan di pangkal dan ujung
    outline_poly(d, shape, fill)
    d.line(pts(c[2:-2]), fill=LEAF_DARK if fill == LEAF else LEAF, width=s(6))


def background():
    im = Image.new("RGB", (s(W), s(W)), SEA)
    d = ImageDraw.Draw(im)
    horizon = 600
    for y in range(horizon):                       # langit bergradasi
        t = y / horizon
        c = tuple(round(a + (b - a) * t) for a, b in zip((120, 208, 240), (214, 242, 250)))
        d.rectangle([0, s(y), s(W), s(y + 1)], fill=c)
    for y in range(horizon, W):                    # laut bergradasi
        t = (y - horizon) / (W - horizon)
        c = tuple(round(a + (b - a) * t) for a, b in zip((70, 178, 216), (36, 136, 186)))
        d.rectangle([0, s(y), s(W), s(y + 1)], fill=c)
    outline_ellipse(d, (640, 215, 800, 375), SUN, 12)   # matahari
    for cx, cy, sc in [(250, 250, 1.0), (330, 340, 0.7)]:   # awan
        for dx, dy, r in [(-50, 10, 38), (0, -8, 52), (55, 10, 40)]:
            x, y, rr = cx + dx * sc, cy + dy * sc, r * sc
            d.ellipse([s(x - rr), s(y - rr), s(x + rr), s(y + rr)], fill=(255, 255, 255))
        d.rectangle([s(cx - 90 * sc), s(cy + 10 * sc), s(cx + 95 * sc), s(cy + 48 * sc)], fill=(255, 255, 255))
    for x, y, w in [(130, 700, 120), (760, 740, 150), (230, 880, 140), (640, 900, 120)]:   # ombak
        d.arc([s(x), s(y), s(x + w / 2), s(y + 36)], 180, 360, fill=SEA_LIGHT, width=s(12))
        d.arc([s(x + w / 2), s(y), s(x + w), s(y + 36)], 180, 360, fill=SEA_LIGHT, width=s(12))
    return im


def foreground():
    im = Image.new("RGBA", (s(W), s(W)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # pulau
    outline_poly(d, [(215, 700), (260, 630), (360, 600), (520, 585), (680, 600), (770, 635), (815, 700),
                     (760, 735), (512, 750), (265, 735)], SAND)
    d.arc([s(300), s(640), s(720), s(730)], 20, 160, fill=SAND_DARK, width=s(10))
    # batang kelapa
    trunk = bezier((590, 610), (640, 470), (575, 330), 30)
    outline_poly(d, ribbon(trunk, 26, 15), TRUNK)
    for i in (6, 12, 18, 24):
        x, y = trunk[i]
        d.line([s(x - 20), s(y), s(x + 20), s(y - 6)], fill=INK, width=s(6))
    # daun
    top = trunk[-1]
    for ang, ln, dr, wd in [(200, 210, 70, 34), (-20, 210, 70, 34), (240, 170, 20, 30), (-60, 170, 20, 30)]:
        frond(d, top, ang, ln, dr, wd, LEAF_DARK)
    for ang, ln, dr, wd in [(160, 200, 60, 36), (20, 200, 60, 36), (270, 130, 0, 28)]:
        frond(d, top, ang, ln, dr, wd, LEAF)
    for dx in (-22, 18):
        outline_ellipse(d, (top[0] + dx - 20, top[1] + 4, top[0] + dx + 20, top[1] + 44), (140, 92, 56), 8)
    # kucing detektif
    cx, cy, r = 390, 575, 105
    outline_poly(d, [(cx - r + 10, cy - 30), (cx - r + 5, cy - r - 35), (cx - 20, cy - r + 15)], CAT)
    outline_poly(d, [(cx + r - 10, cy - 30), (cx + r - 5, cy - r - 35), (cx + 20, cy - r + 15)], CAT)
    outline_poly(d, [(cx - r + 30, cy - r + 5), (cx - r + 28, cy - r - 12), (cx - 38, cy - r + 15)], PINK, 1)
    outline_poly(d, [(cx + r - 30, cy - r + 5), (cx + r - 28, cy - r - 12), (cx + 38, cy - r + 15)], PINK, 1)
    outline_ellipse(d, (cx - r, cy - r + 10, cx + r, cy + r - 10), CAT)
    d.ellipse([s(cx - 62), s(cy + 5), s(cx + 62), s(cy + r - 15)], fill=CAT_LIGHT)
    for ex in (-42, 42):                                    # mata
        outline_ellipse(d, (cx + ex - 17, cy - 38, cx + ex + 17, cy + 8), INK, 1)
        d.ellipse([s(cx + ex - 3), s(cy - 30), s(cx + ex + 9), s(cy - 16)], fill=(255, 255, 255))
    outline_poly(d, [(cx - 12, cy + 12), (cx + 12, cy + 12), (cx, cy + 27)], PINK, 6)
    for sgn in (-1, 1):                                     # kumis melengkung
        curve = bezier((cx + sgn * 6, cy + 38), (cx + sgn * 60, cy + 25), (cx + sgn * 92, cy + 58), 16)
        outline_poly(d, ribbon(curve, 13, 5), INK, 1)
        curl = bezier((cx + sgn * 92, cy + 58), (cx + sgn * 108, cy + 75), (cx + sgn * 85, cy + 82), 10)
        d.line(pts(curl), fill=INK, width=s(9), joint="curve")
    return im


def save(im, path, size):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.resize((size, size), Image.LANCZOS).save(path)


def rounded(im, radius, circle=False):
    mask = Image.new("L", im.size, 0)
    m = ImageDraw.Draw(mask)
    box = [0, 0, im.size[0] - 1, im.size[1] - 1]
    if circle:
        m.ellipse(box, fill=255)
    else:
        m.rounded_rectangle(box, radius=int(im.size[0] * radius), fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


if __name__ == "__main__":
    bg, fg = background(), foreground()
    full = bg.convert("RGBA")
    full.alpha_composite(fg)

    # ikon web / PWA (persegi penuh, aman untuk "maskable")
    for n in (192, 512):
        save(full.convert("RGB"), "www/icon-%d.png" % n, n)

    # ikon Android: legacy (mipmap) + adaptif (latar & latar depan 108dp)
    res = "tools/android-res"
    for name, legacy, adaptive in [("mdpi", 48, 108), ("hdpi", 72, 162), ("xhdpi", 96, 216),
                                   ("xxhdpi", 144, 324), ("xxxhdpi", 192, 432)]:
        folder = "%s/mipmap-%s" % (res, name)
        save(rounded(full, 0.18), folder + "/ic_launcher.png", legacy)
        save(rounded(full, 0, circle=True), folder + "/ic_launcher_round.png", legacy)
        # ikon adaptif: gambar ditempatkan di zona aman (66dp dari 108dp)
        pad = Image.new("RGBA", full.size, (0, 0, 0, 0))
        scale = 0.80
        small = fg.resize((round(fg.size[0] * scale),) * 2, Image.LANCZOS)
        off = (fg.size[0] - small.size[0]) // 2
        pad.alpha_composite(small, (off, off))
        save(pad, folder + "/pulau_icon_foreground.png", adaptive)
        save(bg, folder + "/pulau_icon_background.png", adaptive)
    print("Ikon dibuat")
