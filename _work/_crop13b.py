import pymupdf, os
from PIL import Image
import io
pdf = r'C:\Users\weiyu\Desktop\CIM研究\papers\13_JSSC 2025 — A Multiply-Less Approximate SRAM Compute-In-Memory Macro for Neural-Network Inference.pdf'
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\13_JSSC2025_MultiplyLess_Approx_CIM\assets\figs'
doc = pymupdf.open(pdf)
DPI = 200; scale = DPI/72.0

# (page, caption_y0,y1,x0, filename, has_embedded_or_manual_clip)
plan = [
 (1,  343,351,312, 'fig13_1_VonNeumann与CIM对比'),
 (3,  214,231,49,  'fig13_2_三大挑战'),
 (3,  361,378,49,  'fig13_3_AdderNet核示例'),
 (3,  383,391,312, 'fig13_4_CNN与AdderNet相似性'),
 (4,  278,286,49,  'fig13_5_总体架构'),
 (4,  394,411,49,  'fig13_6_L1计算方案'),
 (4,  192,200,312, 'fig13_7_权重稀疏度提升'),
 (5,  293,301,49,  'fig13_8_L1计算单元电路'),
 (5,  185,193,312, 'fig13_9_SRAM读端口'),
 (5,  345,362,312, 'fig13_10_早期停止机制'),
 (6,  309,326,49,  'fig13_11_改进比较器'),
 (6,  195,212,312, 'fig13_12_比较器面积能效对比'),
 (6,  456,473,312, 'fig13_13_比较误差'),
 (7,  435,443,49,  'fig13_14_芯片照片与测试平台'),
 (7,  525,542,312, 'fig13_15_电压频率缩放'),
 (8,  227,235,49,  'fig13_16_能量面积分解'),
 (8,  389,406,49,  'fig13_17_比较器误差率'),
 (8,  299,307,312, 'fig13_18_部署流程与映射'),
]

def find_content_bbox(page, col, cap_top, cap_bottom):
    """render column strip above caption, find non-white bbox"""
    x0, x1 = (35, 305) if col=='L' else (310, 578)
    # render from page top to caption bottom at DPI
    clip = pymupdf.Rect(x0, 35, x1, cap_bottom+4)
    pix = page.get_pixmap(clip=clip, dpi=DPI, colorspace=pymupdf.csGRAY)
    img = Image.frombytes('L', (pix.width, pix.height), pix.samples)
    px = img.load()
    W,H = pix.width, pix.height
    # find rows/cols with non-white pixels
    rows = []
    for y in range(H):
        non = sum(1 for x in range(0,W,2) if px[x,y] < 235)
        rows.append(non)
    cols_non = [sum(1 for y in range(0,H,2) if px[x,y] < 235) for x in range(W)]
    # content rows: those with significant ink, above caption region
    ink_rows = [y for y in range(H) if rows[y] > 3]
    if not ink_rows: return None
    y_px_top, y_px_bot = min(ink_rows), max(ink_rows)
    # restrict bottom to caption area
    cap_px_bot = int((cap_bottom+2-35)*scale)
    y_px_bot = min(y_px_bot, cap_px_bot)
    # column of content: trim leading/trailing low-ink cols
    cx0 = next(i for i in range(W) if cols_non[i] > 2)
    cx1 = next(i for i in range(W-1,-1,-1) if cols_non[i] > 2)
    # convert back to pdf pts
    return (x0 + cx0/scale, 35 + y_px_top/scale, x0 + cx1/scale, 35 + y_px_bot/scale)

for pno, cy0, cy1, cx0, fname in plan:
    page = doc[pno-1]
    col = 'R' if cx0 > 300 else 'L'
    bb = find_content_bbox(page, col, cy0, cy1)
    if bb is None:
        print(pno, fname, 'NO CONTENT'); continue
    # add small margin
    x0,y0,x1,y1 = bb
    x0-=4; y0-=4; x1+=4; y1+=4
    x0 = max(35, x0); y0 = max(35, y0)
    x1 = min(578, x1); y1 = min(578, y1)
    clip = pymupdf.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(clip=clip, dpi=150)
    pix.save(os.path.join(out, fname+'.png'))
    print(pno, fname, col, 'clip=(%.1f,%.1f,%.1f,%.1f)' % (x0,y0,x1,y1), pix.width, pix.height)
