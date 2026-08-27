import csv
import json
import re
import time
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "Digital_CIM_papers.csv"
OUT = ROOT / "papers"
OUT.mkdir(exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CIM-paper-downloader/1.0"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def norm(s):
    s = re.sub(r"^(ISSCC|JSSC(?: Early Access)?)\s+20\d\d(?:\s+\d+\.\d+)?\s*[—-]\s*", "", s, flags=re.I)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def safe_name(s, limit=150):
    s = re.sub(r'[<>:"/\\|?*]', "_", s).strip(" .")
    return s[:limit].rstrip(" .")


def lookup(title):
    q = urllib.parse.quote(title)
    candidates = []
    try:
        data = get_json(f"https://api.crossref.org/works?query.title={q}&rows=5")
        for x in data["message"]["items"]:
            ct = (x.get("title") or [""])[0]
            candidates.append((SequenceMatcher(None, norm(title), norm(ct)).ratio(), "crossref", x, ct))
    except Exception as e:
        candidates.append((0, "crossref_error", {"error": str(e)}, ""))
    try:
        data = get_json(f"https://api.openalex.org/works?search={q}&per-page=10")
        for x in data.get("results", []):
            ct = x.get("title") or ""
            candidates.append((SequenceMatcher(None, norm(title), norm(ct)).ratio(), "openalex", x, ct))
    except Exception as e:
        candidates.append((0, "openalex_error", {"error": str(e)}, ""))
    candidates.sort(key=lambda z: z[0], reverse=True)
    return candidates


def urls_from(best):
    urls, doi = [], None
    for score, source, x, _ in best:
        if score < 0.72:
            continue
        if source == "crossref":
            doi = doi or x.get("DOI")
            for link in x.get("link") or []:
                u = link.get("URL", "")
                if ".pdf" in u.lower():
                    urls.append(("crossref-pdf", u.replace("http://xplorestaging.ieee.org/", "https://ieeexplore.ieee.org/")))
            primary = ((x.get("resource") or {}).get("primary") or {}).get("URL", "")
            m = re.search(r"/document/(\d+)", primary)
            if m:
                urls.append(("ieee", f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={m.group(1)}"))
        elif source == "openalex":
            doi = doi or x.get("doi", "").removeprefix("https://doi.org/") or None
            for loc in [x.get("best_oa_location"), x.get("primary_location"), *(x.get("locations") or [])]:
                if loc and loc.get("pdf_url"):
                    urls.append(("openalex", loc["pdf_url"]))
    if doi and doi.upper().startswith("10.1109/") and not any(s == "ieee" for s, _ in urls):
        m = re.search(r"\.(\d+)$", doi)
        if m:
            arn = m.group(1)
            urls.append(("ieee", f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={arn}"))
    return doi, list(dict.fromkeys(urls))


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        final_url = r.geturl()
    if not data.startswith(b"%PDF-"):
        raise ValueError(f"not PDF ({len(data)} bytes, final={final_url})")
    dest.write_bytes(data)
    return len(data), final_url


with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
    titles = [row[0].strip() for row in csv.reader(f) if row and row[0].strip() and row[0].strip() != "论文"]

records = []
for i, title in enumerate(titles, 1):
    print(f"[{i:02d}/{len(titles)}] {title}", flush=True)
    best = lookup(title)
    doi, urls = urls_from(best)
    rec = {"index": i, "title": title, "doi": doi, "matched_title": best[0][3] if best else None,
           "match_score": round(best[0][0], 3) if best else 0, "candidate_urls": urls,
           "status": "missing", "file": None, "errors": []}
    dest = OUT / f"{i:02d}_{safe_name(title)}.pdf"
    if dest.exists() and dest.read_bytes()[:5] == b"%PDF-":
        rec.update(status="downloaded", file=dest.name, bytes=dest.stat().st_size)
    else:
        for source, url in urls:
            try:
                size, final_url = download(url, dest)
                rec.update(status="downloaded", file=dest.name, bytes=size, source=source, final_url=final_url)
                print(f"  OK {size} bytes from {source}", flush=True)
                break
            except Exception as e:
                rec["errors"].append({"source": source, "url": url, "error": str(e)})
                print(f"  FAIL {source}: {e}", flush=True)
    records.append(rec)
    (OUT / "manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.3)

with (OUT / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["index", "status", "title", "doi", "matched_title", "match_score", "file"])
    w.writeheader()
    for r in records:
        w.writerow({k: r.get(k) for k in w.fieldnames})

print(f"Done: {sum(r['status']=='downloaded' for r in records)}/{len(records)} downloaded")

