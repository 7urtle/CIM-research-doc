import pymupdf, os
pdf = r'C:\Users\weiyu\Desktop\CIM研究\papers\13_JSSC 2025 — A Multiply-Less Approximate SRAM Compute-In-Memory Macro for Neural-Network Inference.pdf'
out = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\13_JSSC2025_MultiplyLess_Approx_CIM\assets\figs'
doc = pymupdf.open(pdf)
DPI = 150

# (page, fig_label, caption_bbox_y0,y1,x0, filename)
plan = [
 (1,  'Fig.1',  343,351,312, 'fig13_1_VonNeumann与CIM对比'),
 (3,  'Fig.2',  214,231,49,  'fig13_2_三大挑战'),
 (3,  'Fig.3',  361,378,49,  'fig13_3_AdderNet核示例'),
 (3,  'Fig.4',  383,391,312, 'fig13_4_CNN与AdderNet相似性'),
 (4,  'Fig.5',  278,286,49,  'fig13_5_总体架构'),
 (4,  'Fig.6',  394,411,49,  'fig13_6_L1计算方案'),
 (4,  'Fig.7',  192,200,312, 'fig13_7_权重稀疏度提升'),
 (5,  'Fig.8',  293,301,49,  'fig13_8_L1计算单元电路'),
 (5,  'Fig.9',  185,193,312, 'fig13_9_SRAM读端口'),
 (5,  'Fig.10', 345,362,312, 'fig13_10_早期停止机制'),
 (6,  'Fig.11', 309,326,49,  'fig13_11_改进比较器'),
 (6,  'Fig.12', 195,212,312, 'fig13_12_比较器面积能效对比'),
 (6,  'Fig.13', 456,473,312, 'fig13_13_比较误差'),
 (7,  'Fig.14', 435,443,49,  'fig13_14_芯片照片与测试平台'),
 (7,  'Fig.15', 525,542,312, 'fig13_15_电压频率缩放'),
 (8,  'Fig.16', 227,235,49,  'fig13_16_能量面积分解'),
 (8,  'Fig.17', 389,406,49,  'fig13_17_比较器误差率'),
 (8,  'Fig.18', 299,307,312, 'fig13_18_部署流程与映射'),
]

for pno, label, cy0, cy1, cx0, fname in plan:
    page = doc[pno-1]
    col = 'R' if cx0 > 300 else 'L'
    imgs = [im['bbox'] for im in page.get_image_info()]
    cands = [c for c in imgs if c[1] < cy1+2 and (c[0] > 300) == (col=='R')]
    if cands:
        x0 = min(c[0] for c in cands)-15; y0 = min(c[1] for c in cands)-15
        x1 = max(c[2] for c in cands)+15; y1 = cy1+6
    else:
        # vector figure: previous text block bottom in column, else page top
        d = page.get_text('dict')
        tops = [b['bbox'][3] for b in d['blocks'] if b['type']==0 and (b['bbox'][0]>300)==(col=='R') and b['bbox'][1] < cy0-2]
        y0 = max(tops) if tops else 40
        x0, x1 = (35, 305) if col=='L' else (310, 578)
        y1 = cy1+6
    clip = pymupdf.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(clip=clip, dpi=DPI)
    pix.save(os.path.join(out, fname+'.png'))
    print(pno, label, col, 'clip=(%.0f,%.0f,%.0f,%.0f)' % (x0,y0,x1,y1), pix.width, pix.height)
