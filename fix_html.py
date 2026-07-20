path = "frontend/index.html"
content = open(path, encoding="utf-8").read()

has_hardcoded = "http://127.0.0.1:8080" in content
print("Has hardcoded URL:", has_hardcoded)

for i, line in enumerate(content.split("\n"), 1):
    if "BASE" in line and ("127" in line or "const BASE" in line):
        print(f"Line {i}: {line.strip()}")

if has_hardcoded:
    # Patch in-place
    fixed = content.replace(
        'const BASE = "http://127.0.0.1:8080";',
        'const BASE = "";  // relative - same Flask server'
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(fixed)
    print("FIXED: Patched hardcoded URL to relative")
else:
    print("OK: No hardcoded URL found")
