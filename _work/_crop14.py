import pymupdf, os
from PIL import Image
pdf = None
import glob
pdf = glob.glob(r'C:\Users\weiyu\Desktop\CIM研究\papers\14_*')[0]
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\14_JSSC2025_HUNBN_SoC\assets\figs'
doc = pymupdf.open(pdf)
DPI = 200; scale = DPI/72.0

# (page, col, region_top, caption_bottom, fname)
plan = [
 (2,'L', 40, 387, 'fig14_1_PE阵列与DIMC对比'),
 (3,'L', 40, 355, 'fig14_2_SoC架构'),
 (4,'L', 40, 210, 'fig14_3_DIMC宏存储器电路'),
 (4,'R', 40, 604, 'fig14_4_格雷码译码器'),
 (5,'L', 40, 203, 'fig14_5_DIMC宏逻辑'),
 (5,'R', 40, 213, 'fig14_6_同步时序图'),
 (6,'L', 40, 324, 'fig14_7_分离MAC流程对比'),
 (6,'R', 40, 251, 'fig14_8_CNN层计算'),
 (7,'L', 40, 382, 'fig14_9_空间映射四种情形'),
 (7,'R', 40, 592, 'fig14_10_特征图内存表示'),
 (8,'L', 40, 189, 'fig14_11_SRAM分区配置'),
 (9,'L', 40, 321, 'fig14_12_正常卷积数据搬移'),
 (9,'L', 321, 626, 'fig14_13_转置卷积数据搬移'),
 (9,'R', 40, 437, 'fig14_14_部分和精度控制'),
 (9,'R', 437, 565, 'fig14_15_测试平台与芯片照片'),
 (10,'L', 40, 255, 'fig14_16_Shmoo图'),
 (10,'L', 255, 563, 'fig14_17_能效频率图'),
 (10,'R', 40, 208, 'fig14_18_能效特征图尺寸'),
 (10,'R', 208, 381, 'fig14_19_能效通道核尺寸'),
 (10,'R', 381, 523, 'fig14_20_FC层替换'),
 (11,'L', 40, 589, 'fig14_21_四种模型性能'),
 (12,'L', 40, 207, 'fig14_22_深度自编码器性能'),
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
