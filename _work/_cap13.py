import pymupdf
import re
doc = pymupdf.open(r'C:\Users\weiyu\Desktop\CIM研究\papers\13_JSSC 2025 — A Multiply-Less Approximate SRAM Compute-In-Memory Macro for Neural-Network Inference.pdf')
for pno in range(len(doc)):
    page = doc[pno]
    d = page.get_text('dict')
    for b in d['blocks']:
        if b['type']!=0: continue
        txt = ' '.join(s['text'] for l in b['lines'] for s in l['spans'])
        if re.match(r'^(Fig\.|TABLE)', txt.strip()):
            bb = b['bbox']
            print('p%d y=%.0f-%.0f x=%.0f :: %s' % (pno+1, bb[1], bb[3], bb[0], txt[:90]))
