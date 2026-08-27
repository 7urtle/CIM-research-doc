import pymupdf, os
from PIL import Image
pdf = r'C:\Users\weiyu\Desktop\CIM研究\papers\13_JSSC 2025 — A Multiply-Less Approximate SRAM Compute-In-Memory Macro for Neural-Network Inference.pdf'
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\13_JSSC2025_MultiplyLess_Approx_CIM\assets\figs'
doc = pymupdf.open(pdf)
DPI = 200; scale = DPI/72.0

# (page, col, region_top, caption_bottom, fname)  region_top = previous anchor bottom or 40
plan = [
 (1,'R', 40,351, 'fig13_1_VonNeumann与CIM对比'),
 (3,'L', 40,231, 'fig13_2_三大挑战'),
 (3,'L', 231,378, 'fig13_3_AdderNet核示例'),
 (3,'R', 40,391, 'fig13_4_CNN与AdderNet相似性'),
 (4,'L', 40,286, 'fig13_5_总体架构'),
 (4,'L', 286,411, 'fig13_6_L1计算方案'),
 (4,'R', 40,200, 'fig13_7_权重稀疏度提升'),
 (5,'L', 40,301, 'fig13_8_L1计算单元电路'),
 (5,'R', 40,193, 'fig13_9_SRAM读端口'),
 (5,'R', 193,362, 'fig13_10_早期停止机制'),
 (6,'L', 40,326, 'fig13_11_改进比较器'),
 (6,'R', 40,212, 'fig13_12_比较器面积能效对比'),
 (6,'R', 212,473, 'fig13_13_比较误差'),
 (7,'L', 40,443, 'fig13_14_芯片照片与测试平台'),
 (7,'R', 40,542, 'fig13_15_电压频率缩放'),
 (8,'L', 40,235, 'fig13_16_能量面积分解'),
 (8,'L', 235,406, 'fig13_17_比较器误差率'),
 (8,'R', 40,307, 'fig13_18_部署流程与映射'),
]

def ink_bbox(page, col, top, bot):
    x0, x1 = (35, 305) if col=='L' else (308, 578)
    clip = pymupdf.Rect(x0, top-2, x1, bot+2)
    pix = page.get_pixmap(clip=clip, dpi=DPI, colorspace=pymupdf.csGRAY)
    img = Image.frombytes('L', (pix.width, pix.height), pix.samples)
    px = img.load(); W,H = pix.width, pix.height
    rows = [sum(1 for x in range(0,W,2) if px[x,y] < 235) for y in range(H)]
    cols = [sum(1 for y in range(0,H,2) if px[x,y] < 235) for x in range(W)]
    ink_rows = [y for y in range(H) if rows[y] > 3]
    if not ink_rows: return None
    yt, yb = min(ink_rows), max(ink_rows)
    cx0 = next(i for i in range(W) if cols[i] > 2)
    cx1 = next(i for i in range(W-1,-1,-1) if cols[i] > 2)
    return (x0+cx0/scale, top-2+yt/scale, x0+cx1/scale, top-2+yb/scale)

for pno, col, rtop, rbot, fname in plan:
    page = doc[pno-1]
    bb = ink_bbox(page, col, rtop, rbot)
    if bb is None:
        print(pno, fname, 'NO CONTENT'); continue
    x0,y0,x1,y1 = bb
    x0-=3; y0-=3; x1+=3; y1+=3
    clip = pymupdf.Rect(max(35,x0), max(35,y0), min(578,x1), min(580,y1))
    pix = page.get_pixmap(clip=clip, dpi=150)
    pix.save(os.path.join(out, fname+'.png'))
    print(pno, fname, col, 'clip=(%.1f,%.1f,%.1f,%.1f)' % (clip.x0,clip.y0,clip.x1,clip.y1), pix.width, pix.height)
