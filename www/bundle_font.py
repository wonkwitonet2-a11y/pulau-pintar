# Mengunduh font Baloo 2 saat build dan memasangnya ke dalam app (agar offline).
# Jika gagal, game tetap memakai tautan Google Fonts (tidak merusak build).
import re, os, sys, urllib.request

URL = "https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&display=swap"
UA = "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read()

def rewrite(css, fetch, outdir):
    n = [0]
    def sub(m):
        n[0] += 1
        name = "baloo%d.woff2" % n[0]
        with open(os.path.join(outdir, name), "wb") as f:
            f.write(fetch(m.group(1)))
        return "url(fonts/%s)" % name
    return re.sub(r"url\((https://[^)]+)\)", sub, css), n[0]

def main():
    try:
        os.makedirs("www/fonts", exist_ok=True)
        css, n = rewrite(get(URL).decode("utf-8"), get, "www/fonts")
        if n == 0:
            raise RuntimeError("tidak ada file font")
        css = css.replace("url(fonts/", "url(fonts/")
        with open("www/fonts.css", "w", encoding="utf-8") as f:
            f.write(css)
        p = "www/index.html"
        h = open(p, encoding="utf-8").read()
        h2 = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>', '<link rel="stylesheet" href="fonts.css">', h)
        if h2 == h:
            raise RuntimeError("tautan font tidak ditemukan di index.html")
        open(p, "w", encoding="utf-8").write(h2)
        print("Font dibundel: %d file" % n)
    except Exception as e:
        print("Font TIDAK dibundel (pakai tautan online):", e)

if __name__ == "__main__":
    main()
