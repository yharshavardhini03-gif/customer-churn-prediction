import os, re
from pathlib import Path

ROOT = Path(".")
FRONTEND_DIR = str(ROOT / "frontend")
idx = os.path.join(FRONTEND_DIR, "index.html")

print("Frontend dir :", FRONTEND_DIR)
print("index.html   :", "EXISTS" if os.path.exists(idx) else "MISSING")
if os.path.exists(idx):
    sz = os.path.getsize(idx)
    print("Size         :", sz, "bytes")
    content = open(idx, encoding="utf-8").read()
    if "http://127.0.0.1:8080" in content:
        print("BASE URL     : WARNING - still hardcoded!")
    else:
        print("BASE URL     : OK (relative paths)")

print()
print("Routes in api.py:")
src = open("api.py").read()
routes = re.findall(r'@app\.route\("([^"]+)"', src)
for r in routes:
    print(" ", r)
