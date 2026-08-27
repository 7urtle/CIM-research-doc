import csv, json, re, time, urllib.request
from pathlib import Path
import websocket

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "papers"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36"

def chrome_cookies():
    ver = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json/version"))
    ws = websocket.create_connection(ver["webSocketDebuggerUrl"], timeout=10, origin="http://127.0.0.1:9222")
    ws.send(json.dumps({"id": 1, "method": "Storage.getCookies"}))
    while True:
        x = json.loads(ws.recv())
        if x.get("id") == 1:
            ws.close()
            return x["result"]["cookies"]

def fetch(url, cookie_header):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*", "Cookie": cookie_header, "Referer": "https://ieeexplore.ieee.org/"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read(), r.geturl()

cookies = chrome_cookies()
ieee_cookie = "; ".join(f'{c["name"]}={c["value"]}' for c in cookies if "ieee" in c.get("domain", "") or "seamlessaccess" in c.get("domain", ""))
print(f"Chrome cookies available: {len(cookies)}, IEEE-related: {sum('ieee' in c.get('domain','') for c in cookies)}", flush=True)

manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8-sig"))
for r in manifest:
    if r.get("status") == "downloaded": continue
    urls = []
    candidates = r.get("candidate_urls", [])
    if candidates and isinstance(candidates[0], str): candidates = [candidates]
    for source, u in candidates:
        m = re.search(r"arnumber=(\d+)", u)
        if m:
            arn = m.group(1)
            urls.extend([
                f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={arn}",
                f"https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={arn}",
            ])
        if ".pdf" in u.lower(): urls.append(u)
    urls = list(dict.fromkeys(urls))
    dest = OUT / f'{r["index"]:02d}_{re.sub(r"[<>:\"/\\|?*]", "_", r["title"])[:150].rstrip(" .")}.pdf'
    print(f'[{r["index"]:02d}] {r["title"]}', flush=True)
    for u in urls:
        try:
            data, final = fetch(u, ieee_cookie)
            print(f"  {len(data)} bytes -> {final}", flush=True)
            if data.startswith(b"%PDF-"):
                dest.write_bytes(data)
                r.update(status="downloaded", file=dest.name, bytes=len(data), source="chrome-session", final_url=final)
                break
        except Exception as e: print(f"  FAIL {e}", flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(.4)

with (OUT / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["index", "status", "title", "doi", "matched_title", "match_score", "file"])
    w.writeheader()
    for r in manifest: w.writerow({k:r.get(k) for k in w.fieldnames})
print(f"Downloaded {sum(r['status']=='downloaded' for r in manifest)}/{len(manifest)}", flush=True)




