import pymupdf, os, glob
from PIL import Image
pdf = glob.glob(r'C:\Users\weiyu\Desktop\CIM研究\papers\15_*')[0]
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\15_JSSC2025_POSIT_CIM\assets\figs'
doc = pymupdf.open(pdf)
DPI = 200; scale = DPI/72.0

plan = [
 (2,'L', 40, 219, 'fig15_1_相对误差对比'),
 (2,'R', 40, 271, 'fig15_2_POSIT原理与性能'),
 (4,'L', 40, 266, 'fig15_3_三大挑战'),
 (4,'L', 266, 485, 'fig15_4_总体架构'),
 (4,'R', 40, 485, 'fig15_5_移位OR regime处理'),
 (5,'L', 40, 273, 'fig15_6_双向小R移位机制'),
 (6,'L', 40, 233, 'fig15_7_BRPU架构'),
 (6,'L', 233, 612, 'fig15_8_CPCS机制原理'),
 (6,'R', 40, 540, 'fig15_9_2-4b关联与3b优先分区'),
 (7,'R', 40, 282, 'fig15_10_CPCS阵列架构与时序'),
 (8,'L', 40, 363, 'fig15_11_OR累加'),
 (8,'R', 40, 301, 'fig15_12_循环交替调度OR累加'),
 (8,'R', 301, 616, 'fig15_13_CASU架构与控制流'),
 (9,'R', 40, 241, 'fig15_14_芯片照片与总结'),
 (9,'R', 241, 370, 'fig15_15_功耗面积分解'),
 (10,'L', 40, 275, 'fig15_16_验证系统'),
 (11,'L', 40, 211, 'fig15_17_三特性性能评估'),
 (11,'L', 211, 386, 'fig15_18_组合评估能效提升'),
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
