import pymupdf, re
pdf = r'C:\Users\weiyu\Desktop\CIM研究\papers\14_JSSC 2025 — HUNBN, a 16-nm Digital In-Memory-Compute SoC for Edge CNN Application Achieving 24 TOPs_W (4b) at System Level.pdf'
doc = pymupdf.open(pdf)
for pno in range(len(doc)):
    page = doc[pno]
    d = page.get_text('dict')
    caps = []
    for b in d['blocks']:
        if b['type']!=0: continue
        txt = ' '.join(s['text'] for l in b['lines'] for s in l['spans'])
        if re.match(r'^(Fig\.|TABLE)', txt.strip()):
            bb = b['bbox']
            caps.append((bb[0], bb[1], bb[3], txt[:70].replace('\n',' ')))
    if caps:
        print('=== page', pno+1, '===')
        for c in caps:
            print('  x=%.0f y=%.0f-%.0f :: %s' % c)
