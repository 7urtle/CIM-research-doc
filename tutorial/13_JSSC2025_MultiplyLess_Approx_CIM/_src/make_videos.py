# -*- coding: utf-8 -*-
"""论文13演示视频：v01 L1vs点积 / v02 预计算L1数据流 / v03 动态比较器波形"""
import os, subprocess, math
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
VDIR = os.path.join(ROOT, "assets", "videos")
os.makedirs(VDIR, exist_ok=True)
FFMPEG = r"C:\Users\weiyu\Desktop\CIM研究\_ffmpeg\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

FONT = r"C:\Windows\Fonts\msyh.ttc"
def font(sz): return ImageFont.truetype(FONT, sz)

W, H, FPS = 960, 540, 30

def make_frames(render, nframes, outdir):
    os.makedirs(outdir, exist_ok=True)
    for i in range(nframes):
        img = Image.new("RGB", (W, H), (10, 17, 25))
        d = ImageDraw.Draw(img)
        render(d, i, nframes)
        img.save(os.path.join(outdir, "f%04d.png" % i))

def encode(frames_dir, out_path):
    cmd = [FFMPEG, "-y", "-framerate", str(FPS), "-i", os.path.join(frames_dir, "f%04d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22", "-movflags", "+faststart", out_path]
    subprocess.run(cmd, check=True, capture_output=True)

def panel(d, x, y, w, h, fill, outline, r=10):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)

def txt(d, s, x, y, size, fill=(240, 244, 250), anchor="lm", fnt=None):
    d.text((x, y), s, font=fnt or font(size), fill=fill, anchor=anchor)

def title(d, s, y=28):
    d.rounded_rectangle([20, 10, W - 20, 56], radius=10, fill=(15, 27, 45))
    txt(d, s, W // 2, y, 19, fill=(255, 255, 255), anchor="mm")

# ================= v01 L1 vs dot product =================
def v01(d, i, n):
    t = i / n
    title(d, "CNN 点积 vs AdderNet L1 距离：卷积核滑动计算")
    # two feature maps (left), kernels (middle), outputs (right)
    # input window values
    xv = [0, 1, 0, 1, 1, 1, 0, 1, 0]   # 3x3 patch
    wv = [1, -1, 1, -1, 1, -1, 1, -1, 1]  # diagonal edge detector (normalized)
    # dot product & L1
    dot = sum(x * w for x, w in zip(xv, wv))
    l1 = -sum(abs(x - w) for x, w in zip(xv, wv))
    # animate: kernel slides horizontally over a small image
    # draw input image 4x4
    img = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
    kpos = int(t * 3) % 3  # 0..2
    panel(d, 40, 80, 300, 380, (20, 34, 52), (60, 100, 140))
    txt(d, "输入特征图（4×4 二值）", 190, 100, 14, anchor="mm", fill=(200, 214, 232))
    cs = 70
    ox, oy = 70, 130
    for r in range(4):
        for c in range(4):
            col = (120, 170, 220) if img[r][c] else (25, 45, 70)
            d.rectangle([ox + c * cs, oy + r * cs, ox + c * cs + cs - 4, oy + r * cs + cs - 4], fill=col)
            txt(d, str(img[r][c]), ox + c * cs + cs // 2, oy + r * cs + cs // 2, 18, fill=(255, 255, 255), anchor="mm")
    # kernel window
    kw = 3
    d.rectangle([ox + kpos * cs - 3, oy - 3, ox + kpos * cs + kw * cs - 1, oy + kw * cs - 1],
                outline=(240, 180, 60), width=3)
    txt(d, "3×3 窗口", ox + kpos * cs + kw * cs // 2, oy + kw * cs + 24, 13, anchor="mm", fill=(240, 180, 60))

    # kernel panel
    panel(d, 380, 80, 240, 380, (26, 24, 40), (120, 90, 180))
    txt(d, "卷积核（对角边缘检测）", 500, 100, 14, anchor="mm", fill=(210, 190, 240))
    ks = 58
    kx, ky = 400, 130
    for r in range(3):
        for c in range(3):
            v = wv[r * 3 + c]
            col = (90, 160, 220) if v > 0 else (230, 140, 120)
            d.rectangle([kx + c * ks, ky + r * ks, kx + c * ks + ks - 4, ky + r * ks + ks - 4], fill=col)
            txt(d, str(v), kx + c * ks + ks // 2, ky + r * ks + ks // 2, 16, fill=(255, 255, 255), anchor="mm")

    # computation text
    panel(d, 660, 80, 260, 380, (15, 30, 28), (40, 140, 90))
    txt(d, "窗口内计算", 790, 100, 14, anchor="mm", fill=(160, 220, 190))
    win = [img[r][c] for r in range(3) for c in range(3)]
    lines = ["x = " + " ".join(map(str, win)),
             "w = " + " ".join(map(str, wv)),
             "",
             "点积  Σ x·w  = %+d" % dot,
             "（需要 9 次乘法）",
             "",
             "L1   −Σ|x−w| = %+d" % l1,
             "（只有减法+绝对值）"]
    yy = 140
    for ln in lines:
        col = (170, 225, 195) if ln.startswith(("点积", "L1")) else (215, 225, 235)
        txt(d, ln, 790, yy, 15 if ln.startswith(("点积", "L1")) else 13, fill=col, anchor="mm")
        yy += 34

    # progress
    d.rectangle([40, 500, W - 40, 506], fill=(40, 60, 85))
    d.rectangle([40, 500, 40 + (W - 80) * t, 506], fill=(70, 190, 140))
    txt(d, "核心结论：两者都能检测对角边缘 → L1 可替代点积（本论文立足点）", W // 2, 524, 13,
        fill=(210, 225, 240), anchor="mm")

# ================= v02 precomputed L1 datapath =================
def v02(d, i, n):
    t = i / n
    title(d, "预计算 L1 数据流：Σx + Σw − 2·Σmin(x,w)（位串行比较）")
    # data
    x_bits = [1, 0, 1, 0]   # x = 10 (MSB first)
    w_bits = [0, 1, 1, 0]   # w = 6
    # comparison result: MSB differs at bit0: x>w -> min = w
    phase = int(t * 12)  # 12 sub-steps
    bit = min(phase, 3)
    decided = phase >= 0  # decided at bit0
    panel(d, 40, 80, 440, 300, (20, 34, 52), (60, 100, 140))
    txt(d, "位串行比较（MSB 优先）：x=1010(10) vs w=0110(6)", 260, 100, 14, anchor="mm", fill=(200, 214, 232))
    bx, by, bs = 90, 140, 80
    for k in range(4):
        d.rectangle([bx + k * bs, by, bx + k * bs + bs - 6, by + 56], fill=(25, 45, 70))
        txt(d, str(x_bits[k]), bx + k * bs + bs // 2, by + 28, 24, fill=(140, 200, 255), anchor="mm")
        d.rectangle([bx + k * bs, by + 70, bx + k * bs + bs - 6, by + 126], fill=(40, 34, 20))
        txt(d, str(w_bits[k]), bx + k * bs + bs // 2, by + 98, 24, fill=(255, 200, 110), anchor="mm")
        if k < 4:
            txt(d, "x bit%d" % k, bx + k * bs + bs // 2, by + 40, 10, fill=(140, 200, 255), anchor="mm")
            txt(d, "w bit%d" % k, bx + k * bs + bs // 2, by + 112, 10, fill=(255, 200, 110), anchor="mm")
    # highlight compared bits
    for k in range(bit + 1):
        d.rectangle([bx + k * bs - 3, by - 3, bx + k * bs + bs - 3, by + 126 + 3], outline=(240, 180, 60), width=3)
    # comparator status
    if bit == 0:
        status = "第1位 1 vs 0 → x > w 已判定 → min = w（提前停止）"
    elif decided:
        status = "比较已锁定：min(x,w) = w = 0110（后续位直接输出 w）"
    else:
        status = "正在比较第 %d 位" % (bit + 1)
    txt(d, status, 260, 330, 14, anchor="mm", fill=(240, 220, 140))

    # right: datapath
    panel(d, 510, 80, 410, 300, (15, 30, 28), (40, 140, 90))
    txt(d, "L1 计算单元数据流", 715, 100, 14, anchor="mm", fill=(160, 220, 190))
    y0 = 130
    # ActACCU
    panel(d, 540, y0, 180, 52, (18, 45, 60), (80, 160, 200), r=8)
    txt(d, "ActACCU：Σx = 10", 630, y0 + 26, 14, anchor="mm", fill=(150, 210, 255))
    panel(d, 740, y0, 160, 52, (40, 30, 18), (220, 170, 80), r=8)
    txt(d, "WSUM：Σw = 6", 820, y0 + 26, 14, anchor="mm", fill=(255, 210, 130))
    # MinACCU
    panel(d, 540, y0 + 74, 180, 52, (30, 24, 45), (150, 110, 200), r=8)
    txt(d, "MinACCU：Σmin = 6", 630, y0 + 100, 14, anchor="mm", fill=(210, 180, 250))
    panel(d, 740, y0 + 74, 160, 52, (24, 40, 30), (90, 180, 120), r=8)
    txt(d, "2·Σmin = 12", 820, y0 + 100, 14, anchor="mm", fill=(160, 230, 180))
    # ABS-ASM
    panel(d, 540, y0 + 148, 360, 56, (40, 20, 24), (220, 100, 110), r=8)
    txt(d, "ABS-ASM：Σx + Σw − 2Σmin = 10+6−12 = 4", 720, y0 + 176, 15, anchor="mm", fill=(255, 200, 200))
    txt(d, "= Σ|xi−wi| = |10−6| = 4  ✓", 720, y0 + 210, 13, anchor="mm", fill=(160, 230, 180))

    # bottom progress
    d.rectangle([40, 420, W - 40, 426], fill=(40, 60, 85))
    d.rectangle([40, 420, 40 + (W - 80) * t, 426], fill=(70, 190, 140))
    txt(d, "关键：Σw 编译期预存（15 个 SRAM 单元/列），Σx 共享，实时只需比较 → 面积 −1.5×",
        W // 2, 448, 13, fill=(210, 225, 240), anchor="mm")
    txt(d, "权重截断后连续 0 增多 → 位线保持预充 → 读端口省电；激活被选后提前停止读权重位（1.8×）",
        W // 2, 474, 13, fill=(210, 225, 240), anchor="mm")
    txt(d, "推理演示：输入激活经正则化（≤5 个 1）后送入比较器 → 比较误差被抑制",
        W // 2, 500, 13, fill=(210, 225, 240), anchor="mm")

# ================= v03 dynamic comparator waveform =================
def v03(d, i, n):
    t = i / n
    title(d, "改进动态比较器：OUT/OUTB 预充、比较、电荷共享误差")
    # waveform area
    x0, x1, y0, y1 = 60, 900, 90, 330
    d.rectangle([x0, y0, x1, y1], fill=(13, 22, 33), outline=(50, 80, 110))
    # grid
    for gx in range(0, 9):
        gxx = x0 + (x1 - x0) * gx / 8
        d.line([gxx, y0, gxx, y1], fill=(30, 48, 66))
    txt(d, "RESETB", x0 + 10, y0 + 24, 12, fill=(200, 214, 232))
    txt(d, "OUT", x0 + 10, y0 + 88, 12, fill=(140, 200, 255))
    txt(d, "OUTB", x0 + 10, y0 + 148, 12, fill=(255, 160, 150))
    txt(d, "CLK", x0 + 10, y0 + 208, 12, fill=(180, 220, 170))
    # time axis
    tstep = 0.1  # each comparison = 0.1 of total
    # RESETB: low at start, then high
    def yv(v, lo, hi): return y1 - (v - lo) / (hi - lo) * (y1 - y0 - 40) - 20
    # draw per-cycle waveforms; up to 6 comparisons, decided at cycle 2
    ncyc = 6
    cw = (x1 - x0 - 40) / ncyc
    # RESETB
    pts = [(x0 + 20, yv(1, 0, 1.2))]
    pts.append((x0 + 20 + cw * 0.5, yv(1, 0, 1.2)))
    pts.append((x0 + 20 + cw * 0.5, yv(0, 0, 1.2)))
    pts.append((x0 + 20 + cw * 0.5 + 6, yv(0, 0, 1.2)))
    pts.append((x0 + 20 + cw * 0.5 + 6, yv(1, 0, 1.2)))
    pts.append((x1 - 20, yv(1, 0, 1.2)))
    d.line(pts, fill=(220, 230, 240), width=2)
    # OUT / OUTB
    # precharge VDD=1.2, decision at cycle 2 (t=2/6..)
    # OUT: stays high until cycle2 then discharges to 0 (x>w? use x<w example: OUT discharges when w smaller -> actually min=w when w smaller => OUT=VDD? )
    # From paper: OUT discharged to VSS when weight is smaller; OUTB discharged when activation smaller.
    # Use example x=10, w=6: w smaller -> OUT->0 (VSS), OUTB pinned VDD.
    outv = [(x0 + 20, 1.1), (x0 + 20 + cw * 2, 1.1)]
    outv.append((x0 + 20 + cw * 2 + cw * 0.4, 0.1))
    outv.append((x1 - 20, 0.1))
    outbv = [(x0 + 20, 1.1), (x0 + 20 + cw * 2, 1.1)]
    outbv.append((x1 - 20, 1.1))
    # add small ripple due to charge sharing (error depiction) on OUTB? keep clean
    d.line([(px, yv(pv, 0, 1.2)) for px, pv in outv], fill=(140, 200, 255), width=3)
    d.line([(px, yv(pv, 0, 1.2)) for px, pv in outbv], fill=(255, 160, 150), width=3)
    # cycle markers
    for c in range(ncyc):
        cx = x0 + 20 + cw * c
        d.line([cx, y1, cx, y1 + 8], fill=(120, 150, 180))
        txt(d, "b%d" % (c + 1), cx, y1 + 20, 10, fill=(150, 170, 195), anchor="mm")
    # annotation
    d.rounded_rectangle([x0 + 20 + cw * 2 - 6, y1 - 130, x0 + 20 + cw * 2 + cw * 2, y1 - 96], radius=6,
                        fill=(30, 46, 40), outline=(70, 170, 110))
    txt(d, "第2位比较断言：OUT 放电到 VSS、OUTB 被 P4 钳位到 VDD", x0 + 20 + cw * 3, y1 - 113, 12,
        fill=(160, 230, 180), anchor="mm")
    # charge sharing note
    d.rounded_rectangle([x0 + 20 + cw * 2 - 6, y0 + 30, x0 + 20 + cw * 2 + cw * 2, y0 + 64], radius=6,
                        fill=(44, 30, 30), outline=(210, 110, 100))
    txt(d, "高-高位对 → C1/C2 与 OUT 电荷共享 → 电压跌落（改进设计减半）", x0 + 20 + cw * 3, y0 + 47, 12,
        fill=(255, 190, 180), anchor="mm")

    # bottom: comparison vs static
    panel(d, 40, 360, 440, 150, (20, 34, 52), (60, 100, 140))
    txt(d, "改进比较器 vs 静态逻辑比较器", 260, 384, 15, anchor="mm", fill=(200, 214, 232))
    txt(d, "面积：−1.7×", 260, 416, 15, anchor="mm", fill=(140, 230, 180))
    txt(d, "功耗：−4.1×", 260, 446, 15, anchor="mm", fill=(140, 230, 180))
    txt(d, "（post-layout 对比，论文 Fig.12）", 260, 478, 12, anchor="mm", fill=(160, 180, 200))
    panel(d, 500, 360, 420, 150, (26, 24, 40), (120, 90, 180))
    txt(d, "误差抑制：正则化激活「1」个数 ≤5（[19] 为 ≤3）", 710, 390, 14, anchor="mm", fill=(210, 190, 240))
    txt(d, "ResNet-20 仅 0.9% 激活需正则化（[19] 需 15%）", 710, 418, 14, anchor="mm", fill=(210, 190, 240))
    txt(d, "→ 精度 91.71% ≈ 浮点（损失 <0.1%）", 710, 446, 14, anchor="mm", fill=(170, 240, 200))
    txt(d, "0.54V 下 6 次高-高比较后才出错；0.65V 以上无错", 710, 478, 12, anchor="mm", fill=(160, 180, 200))

def main():
    jobs = [
        ("v01", v01, 180),
        ("v02", v02, 210),
        ("v03", v03, 210),
    ]
    for name, fn, nf in jobs:
        fd = os.path.join(ROOT, "_work_vid13", name)
        make_frames(fn, nf, fd)
        encode(fd, os.path.join(VDIR, name + ".mp4"))
        print(name, "done", os.path.getsize(os.path.join(VDIR, name + ".mp4")))

if __name__ == "__main__":
    main()
