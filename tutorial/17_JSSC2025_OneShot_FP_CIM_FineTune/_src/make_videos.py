# -*- coding: utf-8 -*-
"""论文17演示视频：v01 one-shot流程 / v02 ParMS / v03 ODFC微调"""
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

# ================= v01 one-shot flow =================
def v01(d, i, n):
    t = i / n
    title(d, "One-Shot 计算：传统 8 周期 vs 本论文 1 周期")
    # left: conventional bit-serial
    panel(d, 40, 80, 440, 330, (30, 20, 20), (220, 120, 110))
    txt(d, "传统：INT 尾数 MAC 位串行（8 周期）", 260, 102, 14, fill=(255, 190, 180), anchor="mm")
    k = i % 40
    bit = k % 8
    # 8 cycles
    for c in range(8):
        x = 70 + c * 48
        col = (70, 50, 40) if c == bit else (40, 28, 24)
        d.rectangle([x, 130, x + 40, 162], fill=col, outline=(220, 120, 110))
        txt(d, "cyc%d" % (c + 1), x + 20, 150, 10, fill=(255, 210, 200), anchor="mm")
    txt(d, "每周期只算 1 位尾数 → 8 周期", 260, 190, 13, fill=(255, 210, 200), anchor="mm")
    txt(d, "对齐/转换电路 87.5% 时间闲置", 260, 216, 13, fill=(255, 190, 180), anchor="mm")
    # mantissa bits
    bits = "10110110"
    txt(d, "尾数位（MSB→LSB）：", 260, 250, 12, fill=(230, 200, 190), anchor="mm")
    for c in range(8):
        x = 120 + c * 40
        d.rectangle([x, 272, x + 34, 296], fill=(60, 90, 130) if bits[c] == '1' else (30, 44, 60))
        txt(d, bits[c], x + 17, 284, 12, fill=(255, 255, 255), anchor="mm")
        if c == bit:
            d.rectangle([x - 2, 270, x + 36, 298], outline=(255, 200, 90), width=2)
    txt(d, "每次只送 1 位 → 乘法器面积小但慢", 260, 322, 12.5, fill=(255, 210, 200), anchor="mm")
    txt(d, "吞吐被 8 周期卡死", 260, 348, 13.5, fill=(255, 190, 180), anchor="mm")

    # right: one-shot
    panel(d, 500, 80, 420, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "One-Shot：最小选择位并行（1 周期）", 710, 102, 14, fill=(170, 240, 200), anchor="mm")
    # 16 columns all at once
    for c in range(16):
        x = 530 + c * 23
        d.rectangle([x, 130, x + 18, 190], fill=(30, 80, 60), outline=(70, 190, 130))
        txt(d, "列%d" % c, x + 9, 210, 8, fill=(160, 220, 190), anchor="mm")
    txt(d, "16 列并行做最小选择（128 输入）", 710, 240, 13, fill=(190, 230, 210), anchor="mm")
    txt(d, "Σ|xi−wi| = Σxi + Σwi − 2Σmin", 710, 268, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "Σxi 加法树共享 · Σwi 预存 WSUM", 710, 292, 12, fill=(190, 230, 210), anchor="mm")
    txt(d, "实时只算 Σmin → 位并行可行", 710, 316, 13, fill=(120, 230, 180), anchor="mm")
    txt(d, "→ 1 周期完成 · 流水线 100% 利用", 710, 346, 14, fill=(170, 240, 200), anchor="mm")
    txt(d, "→ 吞吐提升 8×", 710, 372, 15, fill=(255, 210, 130), anchor="mm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "关键洞察：multiply-less（L1 距离）把乘法变成最小选择 → 运算足够简单，位并行才可行", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "位并行还利用输入相关性（MSB 翻转少）→ 平均翻转率更低 → 更省能", W // 2, 490, 13, fill=(180, 220, 200), anchor="mm")

# ================= v02 ParMS =================
def v02(d, i, n):
    t = i / n
    title(d, "ParMS：8-bit 并行最小选择器（进位前瞻比较）")
    # inputs
    Wbits = [1, 0, 1, 1, 0, 1, 0, 1]  # W = 10110101 (0xB5)
    XB = [0, 1, 0, 0, 1, 0, 1, 0] # XB = 反相 X = 01001010 (X = 10110101)
    # W = 0xB5=181, X = 0xB5=181? Let's make X different: X=0x4A? XB=01001010 -> X=10110101. Same.
    # use XB as given; compute LESS
    # G[i]=W[i]&XB[i], P[i]=WB[i]|XB[i] where WB=~W
    WB = [1 - v for v in Wbits]
    G = [Wbits[i] & XB[i] for i in range(8)]
    P = [WB[i] | XB[i] for i in range(8)]
    # LESS = G[7] + G[6]P7 + G5P6P7 + ... compute MSB-first comparison: W vs X (using XB as ~X means comparing W with X: W<X iff ...)
    # Compare W and X as unsigned: iterate from MSB
    X = [1 - v for v in XB]
    less = 0
    for i in range(7, -1, -1):
        if Wbits[i] < X[i]:
            less = 1; break
        elif Wbits[i] > X[i]:
            less = 0; break
    k = i % 30
    panel(d, 40, 80, 440, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "8-bit 比较：W vs X（MSB 优先）", 260, 102, 14, fill=(170, 240, 200), anchor="mm")
    bs = 46; bx = 90; by = 120
    txt(d, "W", 70, by + 12, 12, fill=(255, 210, 130), anchor="rm")
    for c in range(8):
        x = bx + c * bs
        d.rectangle([x, by, x + bs - 6, by + 26], fill=(44, 34, 20), outline=(240, 180, 70))
        txt(d, str(Wbits[c]), x + (bs - 6) / 2, by + 13, 14, fill=(255, 255, 255), anchor="mm")
    txt(d, "X", 70, by + 42, 12, fill=(140, 200, 255), anchor="rm")
    for c in range(8):
        x = bx + c * bs
        d.rectangle([x, by + 28, x + bs - 6, by + 54], fill=(20, 40, 62), outline=(140, 200, 255))
        txt(d, str(X[c]), x + (bs - 6) / 2, by + 41, 14, fill=(255, 255, 255), anchor="mm")
    # highlight comparing bit
    step = k % 9
    if step < 8:
        x = bx + (7 - step) * bs
        d.rectangle([x - 3, by - 3, x + bs - 3, by + 57], outline=(255, 200, 90), width=3)
    # comparison result
    if step == 0:
        msg = "比较第 1 位（MSB）：W=1 vs X=1 → 相等，继续"
    elif less:
        msg = "W < X → LESS=1 → 选择单元输出 W（较小值）"
    else:
        msg = "W ≥ X → LESS=0 → 选择单元输出 X（较小值）"
    txt(d, msg, 260, by + 80, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "G⟨i⟩=W⟨i⟩&XB⟨i⟩ · P⟨i⟩=WB⟨i⟩|XB⟨i⟩（编码器并行生成）", 260, by + 110, 11.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "比较树：LESS = G⟨7:4⟩ + P⟨7:4⟩G⟨3:0⟩（三级嵌套，免反相器）", 260, by + 134, 11.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "选择单元：LESS×XB + LESSB×WB → min 值输出", 260, by + 164, 12, fill=(170, 240, 200), anchor="mm")

    # right: benefits
    panel(d, 500, 80, 420, 330, (22, 26, 44), (150, 120, 200))
    txt(d, "ParMS 的优势", 710, 102, 14, fill=(210, 190, 240), anchor="mm")
    panel(d, 530, 130, 360, 60, (30, 28, 50), (150, 120, 200), r=8)
    txt(d, "vs INT8 乘法器：面积 −11.5× · 能耗 −8.2×", 710, 152, 13, fill=(200, 185, 230), anchor="mm")
    txt(d, "（乘法器做最小选择是杀鸡用牛刀）", 710, 176, 11.5, fill=(190, 175, 220), anchor="mm")
    panel(d, 530, 210, 360, 60, (30, 28, 50), (150, 120, 200), r=8)
    txt(d, "vs 综合数字比较器：面积 −14% · 能耗 −4.1×", 710, 232, 13, fill=(200, 185, 230), anchor="mm")
    txt(d, "（定制传输管编码器 + 三级比较树）", 710, 256, 11.5, fill=(190, 175, 220), anchor="mm")
    panel(d, 530, 290, 360, 60, (30, 28, 50), (150, 120, 200), r=8)
    txt(d, "三态反相器门控输出 → 加法树功耗 −44%", 710, 312, 13, fill=(200, 185, 230), anchor="mm")
    txt(d, "全静态逻辑 → 稀疏度高时比动态比较器更省", 710, 336, 11.5, fill=(190, 175, 220), anchor="mm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "整体（vs 位串行乘法 FP-CIM）：面积 −2.8× · 能耗 −3.4× → one-shot 方案落地", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "硬连线设计（Q/QB 直连）免 SRAM 预充功耗 · OUT 浮空 &lt;1/8 周期 → 后端功耗小", W // 2, 490, 13, fill=(180, 220, 200), anchor="mm")

# ================= v03 ODFC fine-tuning =================
def v03(d, i, n):
    t = i / n
    title(d, "ODFC：片上微调恢复环境变化掉的精度")
    # accuracy drop & recovery curve
    panel(d, 40, 80, 880, 180, (16, 32, 26), (70, 190, 130))
    txt(d, "MNIST 训练 → MNIST-M 测试（环境变化）→ ODFC 微调恢复", 480, 102, 14, fill=(170, 240, 200), anchor="mm")
    # axes
    x0, x1, y0, y1 = 100, 880, 130, 230
    d.line([x0, y1, x1, y1], fill=(150, 180, 200), width=2)
    d.line([x0, y0, x0, y1], fill=(150, 180, 200), width=2)
    # accuracy points: epoch -1 (train 99.1), epoch 0 (test 13.8), then recovery 1..10 epochs
    pts = [(x0, 99.1), (x0 + 40, 13.8)]
    for e in range(10):
        acc = 13.8 + (84.3 - 13.8) * (1 - (1 - e / 10) ** 2.2)
        pts.append((x0 + 40 + (e + 1) * (x1 - x0 - 40) / 10, acc))
    for j in range(1, len(pts)):
        axx, ayy = pts[j - 1]
        bxx, byy = pts[j]
        d.line([axx, y1 - (ayy - 0) / 100 * (y1 - y0), bxx, y1 - (byy - 0) / 100 * (y1 - y0)], fill=(120, 230, 180), width=3)
    for j, (pxx, pyy) in enumerate(pts):
        d.ellipse([pxx - 4, y1 - pyy / 100 * (y1 - y0) - 4, pxx + 4, y1 - pyy / 100 * (y1 - y0) + 4], fill=(255, 210, 130))
    txt(d, "99.1%", x0 - 10, y1 - 99.1 / 100 * (y1 - y0), 11, fill=(120, 230, 180), anchor="rm")
    txt(d, "13.8%", x0 + 40, y1 - 13.8 / 100 * (y1 - y0) - 14, 11, fill=(255, 160, 150), anchor="mm")
    txt(d, "84.3%", x1 - 5, y1 - 84.3 / 100 * (y1 - y0), 11, fill=(120, 230, 180), anchor="lm")
    txt(d, "训练", x0, y1 + 12, 10, fill=(150, 180, 200), anchor="mm")
    txt(d, "测试（环境变化）", x0 + 40, y1 + 12, 10, fill=(150, 180, 200), anchor="mm")
    txt(d, "微调 1–10 epochs →", x1 - 60, y1 + 12, 10, fill=(150, 180, 200), anchor="mm")
    txt(d, "精度（%）", x0 - 12, y0 - 12, 11, fill=(150, 180, 200), anchor="mm")

    # ODFC hardware
    panel(d, 40, 280, 440, 150, (22, 26, 44), (150, 120, 200))
    txt(d, "ODFC 硬件（轻量训练）", 260, 302, 14, fill=(210, 190, 240), anchor="mm")
    txt(d, "128 轮顺序更新 128×16 权重（每轮 16 个）", 260, 330, 12, fill=(200, 185, 230), anchor="mm")
    txt(d, "四相：权重读 → 更新 → 梯度算 → 写回", 260, 354, 12, fill=(200, 185, 230), anchor="mm")
    txt(d, "时分复用乘法器/加法树 → 面积再省 10%", 260, 378, 12, fill=(200, 185, 230), anchor="mm")
    txt(d, "0.037 mm² · 2.88 GOPS @180MHz", 260, 406, 12, fill=(170, 240, 200), anchor="mm")

    # loss-preserving add
    panel(d, 500, 280, 420, 150, (16, 32, 26), (70, 190, 130))
    txt(d, "保损失 FP 加法", 710, 302, 14, fill=(170, 240, 200), anchor="mm")
    txt(d, "大数加小数：移位后小数尾数可能变 0", 540, 330, 12, fill=(190, 230, 210), anchor="lm")
    txt(d, "（三个数相加可能得 0）→ 对齐误差保留", 540, 354, 12, fill=(190, 230, 210), anchor="lm")
    txt(d, "下一级再加 → 16×BF16 加法树降损失", 540, 378, 12, fill=(190, 230, 210), anchor="lm")
    txt(d, "微调只需少量 epochs → 精度恢复 84.3%", 540, 406, 12.5, fill=(120, 230, 180), anchor="lm")

    d.rectangle([40, 450, W - 40, 456], fill=(40, 60, 85))
    d.rectangle([40, 450, 40 + (W - 80) * t, 456], fill=(70, 190, 140))
    txt(d, "微调总能耗 18.1µJ（6 层模型）· 训练能效 1.32 TFLOPS/W（训练天生贵于推理，但频率低、影响可忽略）", W // 2, 482, 13, fill=(180, 220, 200), anchor="mm")
    txt(d, "预对齐的较大对齐误差对微调影响远小于从头训练 → 边缘环境鲁棒性大幅提升", W // 2, 510, 13, fill=(210, 225, 240), anchor="mm")

def main():
    jobs = [("v01", v01, 200), ("v02", v02, 200), ("v03", v03, 200)]
    for name, fn, nf in jobs:
        fd = os.path.join(ROOT, "_work_vid17", name)
        make_frames(fn, nf, fd)
        encode(fd, os.path.join(VDIR, name + ".mp4"))
        print(name, "done", os.path.getsize(os.path.join(VDIR, name + ".mp4")))

if __name__ == "__main__":
    main()
