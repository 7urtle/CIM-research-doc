import pymupdf, os, glob
from PIL import Image
pdf = glob.glob(r'C:\Users\weiyu\Desktop\CIM研究\papers\17_*')[0]
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\17_JSSC2025_OneShot_FP_CIM_FineTune\assets\figs'
doc = pymupdf.open(pdf)
DPI = 200; scale = DPI/72.0

plan = [
 (2,'L', 40, 211, 'fig17_1_预对齐FP-CIM架构'),
 (3,'L', 40, 193, 'fig17_2_三大挑战'),
 (3,'L', 193, 415, 'fig17_3_CIM引擎架构'),
 (3,'R', 40, 359, 'fig17_4_一次计算方案对比'),
 (4,'L', 40, 293, 'fig17_5_ParMS并行最小选择器'),
 (5,'L', 40, 211, 'fig17_6_ParMS评估'),
 (5,'L', 211, 370, 'fig17_7_翻转率与一次计算评估'),
 (5,'R', 40, 305, 'fig17_8_输入权重范围与无损钳位'),
 (5,'R', 305, 413, 'fig17_9_离线权重预对齐'),
 (6,'L', 40, 194, 'fig17_10_在线输入权重协同对齐'),
 (6,'R', 40, 415, 'fig17_11_BF16与UBF16格式'),
 (6,'R', 415, 553, 'fig17_12_协同对齐评估'),
 (7,'L', 40, 240, 'fig17_13_片上微调轮次数据流'),
 (7,'R', 40, 383, 'fig17_14_微调训练算法'),
 (7,'R', 383, 629, 'fig17_15_保损失FP加法'),
 (8,'L', 40, 428, 'fig17_16_芯片照片与测试平台'),
 (8,'R', 40, 219, 'fig17_17_电压频率缩放'),
 (8,'R', 219, 370, 'fig17_18_改进分解'),
 (9,'L', 40, 265, 'fig17_19_能量面积分解'),
 (9,'R', 40, 234, 'fig17_20_部署流程与重训'),
 (9,'R', 234, 342, 'fig17_21_尾数移位分布'),
 (9,'R', 342, 484, 'fig17_22_逐层映射'),
 (10,'L', 40, 412, 'fig17_23_ODFC精度恢复'),
 (10,'L', 412, 531, 'fig17_24_MNIST-M训练损失与精度'),
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
