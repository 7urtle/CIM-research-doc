# -*- coding: utf-8 -*-
"""构建 index.html：内联 CSS/JS，拼接所有分片"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

css = open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8").read()
js = open(os.path.join(ROOT, "assets", "app.js"), encoding="utf-8").read()

head = open(os.path.join(BASE, "head.html"), encoding="utf-8").read().replace("__CSS__", css)
tail = open(os.path.join(BASE, "tail.html"), encoding="utf-8").read().replace("__JS__", js)

parts = []
for i in range(10):
    p = os.path.join(BASE, "part%02d.html" % i)
    parts.append(open(p, encoding="utf-8").read())

html = head + "\n".join(parts) + tail
out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print("index.html written:", os.path.getsize(out), "bytes")
