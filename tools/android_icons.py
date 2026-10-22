# Mengganti ikon bawaan Capacitor dengan ikon Pulau Pintar (gambar ada di tools/android-res).
# Dijalankan setelah "npx cap add android".
import os, shutil

SRC = os.path.join(os.path.dirname(__file__), "android-res")
RES = "android/app/src/main/res"
if not os.path.isdir(RES):
    raise SystemExit("Folder android belum ada; jalankan setelah npx cap add android")
shutil.copytree(SRC, RES, dirs_exist_ok=True)
print("Ikon Android diganti")
