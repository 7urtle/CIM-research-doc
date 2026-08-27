# -*- coding: utf-8 -*-
"""论文15演示视频：v01 POSIT格式 / v02 CPCS双位MAC / v03 CASU OR累加"""
import os, subprocess
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

# ================= v01 POSIT format =================
def v01(d, i, n):
    t = i / n
    title(d, "POSIT 数据格式：动态位分配（S / R / E / M）")
    # a POSIT(8,1) example: value bits changing over time to show dynamic M width
    examples = [
        ("0 11 0 101", "R=+1(2b), E=0, M=101(3b) → 大尾数", 8),
        ("0 11110 1 01", "R=+4(5b), E=1, M=01(1b) → 大范围", 8),
        ("0 1 0 1011", "R=0(1b), E=0, M=1011(4b) → 最大尾数", 8),
        ("0 0001 1 01", "R=-3(4b), E=1, M=01(1b) → 负大范围", 8),
    ]
    k = (i // 40) % 4
    bits, desc, mw = examples[k]
    panel(d, 40, 80, 880, 120, (20, 34, 52), (90, 170, 220))
    txt(d, "POSIT(8,1) 示例：位分配随数据分布动态变化", 480, 100, 16, fill=(200, 220, 245), anchor="mm")
    # bit cells
    bx, by, bs = 120, 128, 80
    segs = [("S", bits[0], (230, 120, 110)), ("R", bits[2:7].strip(), (240, 180, 70)), ("E", bits[8], (80, 190, 140)), ("M", bits[10:], (170, 120, 220))]
    x = bx
    for name, val, col in segs:
        if not val: continue
        wpx = len(val) * bs
        d.rectangle([x, by, x + wpx, by + 64], fill=(30, 46, 66), outline=col, width=2)
        txt(d, name, x + wpx // 2, by + 22, 13, fill=col, anchor="mm")
        txt(d, val.replace(" ", ""), x + wpx // 2, by + 46, 18, fill=(255, 255, 255), anchor="mm")
        x += wpx + 6
    txt(d, desc, 480, by + 92, 14, fill=(200, 230, 210), anchor="mm")
    # dynamic width bars
    panel(d, 40, 230, 880, 150, (16, 30, 28), (70, 190, 130))
    txt(d, "动态位宽 vs 固定 FP8：(1,5,2) 指数范围 [−14,15]", 480, 252, 14, fill=(170, 240, 200), anchor="mm")
    # range coverage
    panel(d, 80, 272, 380, 70, (26, 40, 30), (70, 190, 130), r=8)
    txt(d, "ViT-B 数据指数范围：", 120, 292, 13, fill=(190, 230, 210), anchor="lm")
    txt(d, "梯度 [−66,−10] · 激活 [−16,4] · 权重 [−16,2]", 120, 316, 12, fill=(220, 240, 230), anchor="lm")
    panel(d, 500, 272, 380, 70, (30, 26, 44), (170, 120, 220), r=8)
    txt(d, "FP8 覆盖不了梯度（69.3% 变 0）→ 掉精度", 540, 292, 13, fill=(210, 190, 240), anchor="lm")
    txt(d, "POSIT8 动态分配 → ≈FP16 精度", 540, 316, 13, fill=(190, 170, 225), anchor="lm")
    # bottom
    d.rectangle([40, 410, W - 40, 416], fill=(40, 60, 85))
    d.rectangle([40, 410, 40 + (W - 80) * t, 416], fill=(70, 190, 140))
    txt(d, "值 = (−1)ˢ × (2^es)ᴿ × 2ᴱ × 1.M · R 是温度计码（连续 0/1）→ 前导检测自动分段", W // 2, 440, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "ResNet18 分类：POSIT8 精度差 <0.4% vs FP16/BF16，能耗省 6.25×", W // 2, 468, 13, fill=(180, 220, 200), anchor="mm")
    txt(d, "代价：regime 动态处理能耗 +2.62× · CIM 单元欠利用 41.3% · 加法树浪费 62.5% → 本论文三招", W // 2, 496, 13, fill=(255, 200, 190), anchor="mm")

# ================= v02 CPCS dual-bit MAC =================
def v02(d, i, n):
    t = i / n
    title(d, "CPCS：关键位预计算存储 → 每周期双位 MAC")
    # store 3-bit weight W in 4-bit CIM unit; W = 101
    Wbits = [1, 0, 1]
    # precompute critical bit S[1] = W[1] & (W[0]&W[2]) -> 0 & (1&1)=0
    crit = Wbits[1] & (Wbits[0] & Wbits[2])
    panel(d, 40, 80, 440, 330, (20, 34, 52), (90, 170, 220))
    txt(d, "4-bit CIM 单元存 3-bit 尾数 W=101", 260, 102, 14, fill=(200, 220, 245), anchor="mm")
    # cells
    bs = 80; bx = 90; by = 122
    for k in range(3):
        d.rectangle([bx + k * bs, by, bx + k * bs + bs - 6, by + 54], fill=(24, 46, 70), outline=(140, 200, 255), width=2)
        txt(d, "W[%d]=%d" % (k, Wbits[k]), bx + k * bs + (bs - 6) // 2, by + 27, 16, fill=(255, 255, 255), anchor="mm")
    # spare cell with critical bit
    d.rectangle([bx + 3 * bs, by, bx + 3 * bs + bs - 6, by + 54], fill=(44, 30, 24), outline=(240, 180, 70), width=2)
    txt(d, "关键位 S[1]=%d" % crit, bx + 3 * bs + (bs - 6) // 2, by + 27, 14, fill=(255, 210, 130), anchor="mm")
    txt(d, "预计算：S[1] = W[1]∧(W[0]&W[2])", 260, by + 80, 13, fill=(200, 220, 245), anchor="mm")
    txt(d, "加载时算好存进空闲单元 → 运行时直接用", 260, by + 104, 13, fill=(190, 215, 240), anchor="mm")
    txt(d, "→ 单元利用率 +63% · 吞吐 +38.2%", 260, by + 140, 14, fill=(120, 230, 180), anchor="mm")

    # dual-bit MAC
    panel(d, 500, 80, 420, 330, (16, 30, 28), (70, 190, 130))
    txt(d, "每周期双位 MAC：O = W×A[n] + W×A[n+2]", 710, 102, 14, fill=(170, 240, 200), anchor="mm")
    k = i % 40
    an = (k // 10) % 4  # A[n+2]/A[n] combos: 00,01,10,11
    a0 = an & 1; a2 = (an >> 1) & 1
    P = Wbits[0] & a0  # W×A[n] partial (bit0)
    if an == 0 or an == 1:
        O = "P[2:0]"
        oline = "A[n+2]/A[n]=%d%d → O = P[2:0]（无移位）" % (a2, a0)
    elif an == 2:
        O = "P[2:0]≪2"
        oline = "A[n+2]/A[n]=10 → O = P[2:0]≪2（左移 2 位）"
    else:
        O = "S[3:0]‖P[1:0]"
        oline = "A[n+2]/A[n]=11 → O = P[2:0]+P[2:0]≪2 = S[3:0]‖P[1:0]（关键位 S[1] 参与）"
    panel(d, 530, 140, 360, 60, (22, 42, 34), (70, 190, 130), r=8)
    txt(d, "A[n+2]|A[n] = %d%d" % (a2, a0), 710, 158, 14, fill=(200, 240, 220), anchor="mm")
    txt(d, "部分积 P = W×A[n] = %d" % P, 710, 182, 13, fill=(190, 230, 210), anchor="mm")
    txt(d, oline, 710, 230, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "← 关键位 S[1] 已存好 → 无需运行时计算", 710, 258, 13, fill=(255, 210, 130), anchor="mm")
    txt(d, "2–4b 关联：4b 尾数(LSB=0)借 2b 单元空闲位 → +24.7%", 710, 300, 12.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "3b 优先分区：POSIT16 长尾数切 3 段全双位 → +1.34×", 710, 324, 12.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "负载/预计算/3:8 译码器开销仅 1.6%（只在加载时工作）", 710, 356, 12, fill=(160, 200, 180), anchor="mm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "设计思想：把「存不满」的空闲位变成「预计算的算力」→ 固定结构也拿到动态位宽的好处", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "vs 传统位串行：每周期多算一位 → 吞吐 1.31×（对 SOTA 加速的贡献之一）", W // 2, 490, 13, fill=(180, 220, 200), anchor="mm")

# ================= v03 CASU OR accumulation =================
def v03(d, i, n):
    t = i / n
    title(d, "CASU：无重叠位用 OR 替代加法（循环交替调度）")
    # two operands aligned: A=1011000, B=0000101 (no overlap)
    A = "1011000"; B = "0000101"
    k = i % 50
    phase = k // 10  # 0: OR idea, 1: early detect, 2: cyclical, 3: summary
    # panel 1: OR idea
    panel(d, 40, 80, 440, 180, (16, 32, 26), (70, 190, 130))
    txt(d, "无重叠位：X+0 = X = X|0", 260, 102, 15, fill=(170, 240, 200), anchor="mm")
    bx, by = 80, 120
    for c in range(7):
        d.rectangle([bx + c * 46, by, bx + c * 46 + 40, by + 30], fill=(24, 46, 70), outline=(140, 200, 255))
        txt(d, A[c], bx + c * 46 + 20, by + 15, 13, fill=(255, 255, 255), anchor="mm")
    by2 = by + 42
    for c in range(7):
        d.rectangle([bx + c * 46, by2, bx + c * 46 + 40, by2 + 30], fill=(44, 30, 24), outline=(240, 180, 70))
        txt(d, B[c], bx + c * 46 + 20, by2 + 15, 13, fill=(255, 255, 255), anchor="mm")
    txt(d, "加法：每位 X+0（冗余翻转） vs OR：直接逐位或", 260, by2 + 60, 13, fill=(190, 230, 210), anchor="mm")
    txt(d, "16b 加法器 174.38 nW vs 16b OR 29.75 nW → 省 82.9%", 260, by2 + 86, 13, fill=(120, 230, 180), anchor="mm")
    txt(d, "POSIT8 中 28.4% 的对齐结果无重叠位", 260, by2 + 112, 12, fill=(190, 230, 210), anchor="mm")

    # panel 2: early detection
    panel(d, 500, 80, 420, 180, (24, 22, 40), (170, 120, 220))
    txt(d, "提前检测：重叠位不同时为 1 也能用 OR", 710, 102, 14, fill=(210, 190, 240), anchor="mm")
    txt(d, "A[1]/B[3]、A[0]/B[2] 两个重叠位：", 540, 130, 12.5, fill=(200, 185, 230), anchor="lm")
    txt(d, "若不同时 1 → A[1]+B[3]=A[1]|B[3] → 可替代", 540, 154, 12.5, fill=(200, 185, 230), anchor="lm")
    txt(d, "单重叠位满足概率 3/4；n 位全满足 (3/4)ⁿ", 540, 178, 12.5, fill=(200, 185, 230), anchor="lm")
    txt(d, "n=4 时仅 23.7% → 检测 4 位最优 → 省 36.1% 加法器", 540, 202, 12.5, fill=(170, 240, 200), anchor="lm")
    txt(d, "检测开销随位数线性增长 → 不贪多", 540, 226, 12, fill=(190, 175, 220), anchor="lm")
    txt(d, "若重叠位全为 1 → 进入循环交替调度（下图）", 540, 254, 12.5, fill=(255, 210, 130), anchor="lm")

    # panel 3: cyclical scheduling
    panel(d, 40, 280, 880, 150, (22, 26, 44), (120, 140, 200))
    txt(d, "循环交替调度：把位串行计算的顺序错开 → 制造无重叠", 480, 302, 14, fill=(200, 210, 240), anchor="mm")
    txt(d, "同步：A0[i] 与 A1[i] 每位都重叠 → n 个加法器", 90, 330, 12.5, fill=(230, 170, 160), anchor="lm")
    txt(d, "循环移位 A0：A0[1],A0[2],…,A0[n],A0[0]", 90, 356, 12.5, fill=(200, 210, 240), anchor="lm")
    txt(d, "→ W0×A0[i+1] 与 W1×A1[i] 无重叠（i<n）→ (n−1) 个 OR + 1 个加法器", 90, 382, 12.5, fill=(120, 230, 180), anchor="lm")
    txt(d, "无重叠率 +36.4% · 计算功率再省 31.3% · 加法树功耗占比 23.4%→12.3%", 90, 408, 12.5, fill=(170, 240, 200), anchor="lm")

    d.rectangle([40, 450, W - 40, 456], fill=(40, 60, 85))
    d.rectangle([40, 450, 40 + (W - 80) * t, 456], fill=(70, 190, 140))
    txt(d, "CASU 三档：n−|ΔR|≤0 → 纯 OR；0~4 → 查替代条件；>4 → 循环调度加法", W // 2, 482, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "面积开销仅 2.3%（几个 OR 门）→ POSIT16 系统能效 → 27.61 TFLOPS/W（2.08×）", W // 2, 510, 13, fill=(180, 220, 200), anchor="mm")

def main():
    jobs = [("v01", v01, 180), ("v02", v02, 200), ("v03", v03, 200)]
    for name, fn, nf in jobs:
        fd = os.path.join(ROOT, "_work_vid15", name)
        make_frames(fn, nf, fd)
        encode(fd, os.path.join(VDIR, name + ".mp4"))
        print(name, "done", os.path.getsize(os.path.join(VDIR, name + ".mp4")))

if __name__ == "__main__":
    main()
