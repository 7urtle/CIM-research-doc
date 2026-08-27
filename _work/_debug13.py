import pymupdf
pdf = r'C:\Users\weiyu\Desktop\CIM研究\papers\13_JSSC 2025 — A Multiply-Less Approximate SRAM Compute-In-Memory Macro for Neural-Network Inference.pdf'
doc = pymupdf.open(pdf)
for pno in [3,4,5,6,8]:
    page = doc[pno-1]
    print('=== page', pno, '===')
    d = page.get_text('dict')
    for b in d['blocks']:
        if b['type']!=0: continue
        bb = b['bbox']
        txt = ' '.join(s['text'] for l in b['lines'] for s in l['spans'])[:40]
        print('  x0=%.0f y0=%.0f y1=%.0f :: %s' % (bb[0], bb[1], bb[3], txt))
