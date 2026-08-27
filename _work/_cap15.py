import pymupdf, re
pdf = globals().get('pdf')
import glob
pdf = glob.glob(r'C:\Users\weiyu\Desktop\CIM研究\papers\15_*')[0]
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
            caps.append((bb[0], bb[1], bb[3], txt[:70]))
    if caps:
        print('=== page', pno+1, '===')
        for c in caps: print('  x=%.0f y=%.0f-%.0f :: %s' % c)
