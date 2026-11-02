#!/usr/bin/env python3
"""Пересборка AVIF/WebP/JPG из оригиналов: python3 tools/optimize_images.py src_img/photo.jpg имя [ширины...]
Нужен Pillow (pip install pillow pillow-avif-plugin)."""
import sys
from PIL import Image
try:
    import pillow_avif  # noqa
except Exception:
    pass
src, name = sys.argv[1], sys.argv[2]
widths = [int(w) for w in sys.argv[3:]] or [480, 800, 1200]
im = Image.open(src).convert("RGB")
for w in widths:
    if w > im.width: continue
    r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    base = f"site/assets/img/{name}-{w}"
    r.save(base + ".jpg", quality=80, optimize=True, progressive=True)
    r.save(base + ".webp", quality=76, method=6)
    try: r.save(base + ".avif", quality=55)
    except Exception as e: print("avif пропущен:", e)
    print("ok", base)
