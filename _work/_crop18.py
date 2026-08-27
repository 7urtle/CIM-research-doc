import pymupdf, os, glob
from PIL import Image
pdf = glob.glob(r'C:\Users\weiyu\Desktop\CIM研究\papers\18_*')[0]
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\18_JSSC2025_Stochastic_CIM_CNN\assets\figs'
doc = pymupdf.open(pdf)
DPI = 200; scale = DPI/72.0

plan = [
 (2,'L', 40, 297, 'fig18_1_SCIM宏与模拟CIM对比'),
 (2,'R', 40, 278, 'fig18_2_SC数表示与基础积木'),
 (3,'L', 40, 248, 'fig18_3_SCIM加速器架构'),
 (3,'R', 40, 437, 'fig18_4_split-unipolar表示与位并行映射'),
 (4,'L', 40, 280, 'fig18_5_SNG电路'),
 (5,'L', 40, 345, 'fig18_6_激活复用与SNG能耗'),
 (5,'R', 40, 461, 'fig18_7_SCIM位单元阵列'),
 (6,'L', 40, 235, 'fig18_8_平均池化计算跳算'),
 (7,'L', 40, 345, 'fig18_9_能耗对比'),
 (7,'R', 40, 348, 'fig18_10_近内存部分二进制累加'),
 (8,'L', 40, 454, 'fig18_11_卷积数据流与乒乓FIFO'),
 (9,'L', 40, 353, 'fig18_12_随机转二进制并行计数器'),
 (9,'R', 40, 372, 'fig18_13_OR累加与训练建模'),
 (10,'L', 40, 186, 'fig18_14_芯片显微照片'),
 (10,'L', 186, 323, 'fig18_15_时钟频率电压'),
 (10,'R', 40, 184, 'fig18_16_面积分解'),
 (11,'L', 40, 448, 'fig18_17_能效电压'),
 (11,'L', 448, 585, 'fig18_18_能耗分解'),
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
