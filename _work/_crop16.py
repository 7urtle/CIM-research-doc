import pymupdf, os, glob
from PIL import Image
pdf = glob.glob(r'C:\Users\weiyu\Desktop\CIM研究\papers\16_*')[0]
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\16_JSSC2025_Secure_Digital_IMC\assets\figs'
doc = pymupdf.open(pdf)
DPI = 200; scale = DPI/72.0

plan = [
 (3,'L', 40, 275, 'fig16_1_安全宏框图'),
 (3,'R', 40, 432, 'fig16_2_AND与XNOR乘法对比'),
 (5,'L', 40, 373, 'fig16_3_进位保存加法器'),
 (5,'R', 40, 162, 'fig16_4_共享均匀性概率'),
 (6,'L', 40, 161, 'fig16_5_MSB累加特殊方法'),
 (6,'R', 40, 210, 'fig16_6_ASCON密码实现'),
 (6,'R', 210, 329, 'fig16_7_SRAM作PUF'),
 (7,'R', 40, 197, 'fig16_8_芯片照片与测试平台'),
 (8,'L', 40, 314, 'fig16_9_CPA保护结果'),
 (8,'L', 314, 415, 'fig16_10_CPA未保护结果'),
 (8,'L', 415, 495, 'fig16_11_DPA结果'),
 (9,'L', 40, 153, 'fig16_12_密钥汉明距离'),
 (9,'R', 40, 189, 'fig16_13_功耗面积分解'),
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
