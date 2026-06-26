import re

with open('compute.py', 'r', encoding='utf-8') as f:
    compute_code = f.read()

cache_busting_code = """
    # ---- Cache Busting ----
    # Обновляем версию файлов в index.html, чтобы сбросить кэш у пользователей
    import time
    version = str(int(time.time()))
    index_path = DOCS / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Обновляем CSS
        html = re.sub(r'href="style\.css(\?v=\d+)?"', f'href="style.css?v={version}"', html)
        # Обновляем data.js
        html = re.sub(r'src="data\.js(\?v=\d+)?"', f'src="data.js?v={version}"', html)
        # Обновляем app.js
        html = re.sub(r'src="app\.js(\?v=\d+)?"', f'src="app.js?v={version}"', html)
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[INFO] Cache busted in index.html (version {version})")
"""

if "# ---- Cache Busting ----" not in compute_code:
    compute_code = compute_code.replace('print(f"\\n[INFO] Web dashboard data exported to {DOCS / \'data.js\'}")', 'print(f"\\n[INFO] Web dashboard data exported to {DOCS / \'data.js\'}")\n' + cache_busting_code)
    
    with open('compute.py', 'w', encoding='utf-8') as f:
        f.write(compute_code)
    print("compute.py updated with cache busting.")
