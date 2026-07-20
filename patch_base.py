content = open('write_frontend.py', encoding='utf-8').read()

old = 'const BASE = "http://127.0.0.1:8080";'
new = 'const BASE = "";  // Same-origin: Flask serves both frontend and API'

if old in content:
    updated = content.replace(old, new)
    open('write_frontend.py', 'w', encoding='utf-8').write(updated)
    print('Patched write_frontend.py: BASE URL set to relative')
else:
    # Search for it
    idx = content.find('127.0.0.1')
    if idx >= 0:
        snippet = content[max(0,idx-40):idx+80]
        print('Found 127.0.0.1 context:', repr(snippet))
    else:
        print('Not found')
