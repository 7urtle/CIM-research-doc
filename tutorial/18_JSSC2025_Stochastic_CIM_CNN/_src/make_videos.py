# -*- coding: utf-8 -*-
"""论文18演示视频：v01 SC基础 / v02 SCIM计算 / v03 池化跳算"""
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

# ================= v01 SC basics =================
def v01(d, i, n):
    t = i / n
    title(d, "随机计算基础：比特流表示 + AND 乘法 + OR 加法")
    # stream example
    panel(d, 40, 80, 440, 330, (20, 34, 52), (90, 170, 220))
    txt(d, "数 = 流中 1 的比例", 260, 102, 15, fill=(200, 220, 245), anchor="mm")
    stream = [0, 1, 0, 0, 0, 0, 0, 1]
    k = i % 30
    # two streams for AND multiply: A = 2/8, B = 4/8
    A = [0, 1, 0, 0, 0, 0, 0, 1]
    B = [1, 0, 0, 1, 0, 0, 1, 0]
    bs = 46; bx = 90; by = 130
    txt(d, "A (2/8)", 70, by + 14, 12, fill=(140, 200, 255), anchor="rm")
    for c in range(8):
        x = bx + c * bs
        d.rectangle([x, by, x + bs - 6, by + 30], fill=(24, 46, 70) if A[c] else (16, 30, 48), outline=(140, 200, 255))
        txt(d, str(A[c]), x + (bs - 6) / 2, by + 15, 13, fill=(255, 255, 255), anchor="mm")
    txt(d, "B (4/8)", 70, by + 44, 12, fill=(255, 210, 130), anchor="rm")
    for c in range(8):
        x = bx + c * bs
        d.rectangle([x, by + 28, x + bs - 6, by + 58], fill=(44, 34, 20) if B[c] else (30, 24, 16), outline=(240, 180, 70))
        txt(d, str(B[c]), x + (bs - 6) / 2, by + 43, 13, fill=(255, 255, 255), anchor="mm")
    # AND result
    txt(d, "A AND B (1/8)", 70, by + 74, 12, fill=(120, 230, 180), anchor="rm")
    for c in range(8):
        x = bx + c * bs
        v = A[c] & B[c]
        d.rectangle([x, by + 58, x + bs - 6, by + 88], fill=(22, 44, 34) if v else (16, 30, 26), outline=(70, 190, 130))
        txt(d, str(v), x + (bs - 6) / 2, by + 73, 13, fill=(255, 255, 255), anchor="mm")
    # highlight current bit
    x = bx + k * bs
    d.rectangle([x - 3, by - 3, x + bs - 3, by + 91], outline=(255, 200, 90), width=2)
    txt(d, "AND：Prob(A∩B)=Prob(A)×Prob(B) = (2/8)(4/8)=1/8 ✓", 260, by + 104, 13.5, fill=(170, 240, 200), anchor="mm")
    txt(d, "概率乘法 → 与门硬件 → 微小逻辑！", 260, by + 132, 13, fill=(200, 220, 245), anchor="mm")

    # right: OR accumulation
    panel(d, 500, 80, 420, 330, (22, 26, 44), (150, 120, 200))
    txt(d, "OR ≈ 加法（近似）", 710, 102, 15, fill=(210, 190, 240), anchor="mm")
    txt(d, "Prob(A∪B) = a + b − ab ≈ a + b", 710, 132, 13, fill=(200, 185, 230), anchor="mm")
    txt(d, "两输入 OR：a+b−ab；多输入 ≈ 1−e^(−s)", 710, 160, 13, fill=(200, 185, 230), anchor="mm")
    txt(d, "小输入近线性；大输入在 1 饱和（非线性）", 710, 188, 12.5, fill=(190, 175, 220), anchor="mm")
    txt(d, "MUX：随机选输入的缩放加法（平均）", 710, 216, 12.5, fill=(200, 185, 230), anchor="mm")
    txt(d, "→ 平均池化就用 MUX 实现", 710, 240, 12.5, fill=(170, 240, 200), anchor="mm")
    panel(d, 540, 268, 360, 80, (34, 28, 50), (150, 120, 200), r=8)
    txt(d, "SNG：LFSR + 级联 MUX 转随机流", 590, 292, 12.5, fill=(210, 190, 240), anchor="lm")
    txt(d, "训练时建模 OR 非线性 → 精度 ≈ INT8", 590, 316, 12.5, fill=(190, 170, 225), anchor="lm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "SC 的优势：乘法=AND、累加=OR（1-bit 逻辑）→ 单元仅 +4 晶体管 → 免 ADC/DAC", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "SC 的代价：8-bit 需 2⁸=256 位流（指数）· SNG 能耗 25× MAC → 需复用+跳算", W // 2, 490, 13, fill=(180, 220, 200), anchor="mm")

# ================= v02 SCIM computation =================
def v02(d, i, n):
    t = i / n
    title(d, "SCIM 宏：10T 单元 + wired-OR 累加（无 ADC）")
    # left: cell
    panel(d, 40, 80, 440, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "10T 位单元（6T SRAM + 4T AND）", 260, 102, 14, fill=(170, 240, 200), anchor="mm")
    k = i % 40
    a = (k // 20) % 2      # stored activation bit
    wp = (k // 5) % 2      # weight positive bit
    wn = (k // 2) % 2      # weight negative bit
    # SRAM
    panel(d, 80, 130, 150, 60, (22, 44, 34), (70, 190, 130), r=8)
    txt(d, "6T SRAM", 155, 148, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "存激活位 a = %d" % a, 155, 172, 12, fill=(190, 230, 210), anchor="mm")
    # AND multipliers
    panel(d, 260, 130, 180, 60, (30, 40, 26), (240, 200, 90), r=8)
    txt(d, "级联 nMOS AND", 350, 148, 12, fill=(255, 220, 140), anchor="mm")
    txt(d, "a&wp = %d · a&wn = %d" % (a & wp, a & wn), 350, 172, 12, fill=(240, 210, 130), anchor="mm")
    # wired OR
    panel(d, 80, 210, 360, 80, (22, 40, 30), (90, 190, 130), r=8)
    txt(d, "wired-OR（伪 nMOS 预充）：", 260, 230, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "任一单元导通 → 计算端口放电（结果=1）", 260, 254, 12, fill=(190, 230, 210), anchor="mm")
    txt(d, "全不导通 → 仅漏电（最差 12 mV 跌落）", 260, 276, 12, fill=(190, 230, 210), anchor="mm")
    txt(d, "CPP/CPN 共享计算端口跨 256 单元 → OR 累加", 260, 306, 12, fill=(170, 240, 200), anchor="mm")
    txt(d, "→ 1-bit 逻辑输出 → 无需 ADC！", 260, 334, 13.5, fill=(255, 210, 130), anchor="mm")

    # right: bit-parallel
    panel(d, 500, 80, 420, 330, (20, 34, 52), (90, 170, 220))
    txt(d, "位并行：N 个宏同时算 N 位流", 710, 102, 14, fill=(200, 220, 245), anchor="mm")
    # macros
    for m in range(8):
        x = 530 + m * 46
        col = (24, 46, 70) if (i // 5) % 8 == m else (18, 36, 56)
        d.rectangle([x, 130, x + 40, 170], fill=col, outline=(140, 200, 255))
        txt(d, "宏%d" % (m + 1), x + 20, 156, 9, fill=(200, 220, 245), anchor="mm")
    txt(d, "宏 m 存激活向量第 m 位（a1_tm…ak_tm）", 710, 196, 12, fill=(200, 220, 245), anchor="mm")
    txt(d, "权重第 m 位施加到宏 m 的 CPWL", 710, 220, 12, fill=(200, 220, 245), anchor="mm")
    txt(d, "全部宏并行 → 所有输出位 1 周期可得", 710, 252, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "（传统位串 SC 要 N 周期逐位处理）", 710, 276, 12, fill=(190, 215, 240), anchor="mm")
    txt(d, "32 行 × 256 列宏 · 每行两个 256 长点积", 710, 308, 12, fill=(200, 220, 245), anchor="mm")
    txt(d, "每宏 16.4k MAC 单元 · 感放仅占 2% 面积", 710, 332, 12, fill=(190, 215, 240), anchor="mm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "数字 CIM 每存储位 ~20 额外晶体管 vs SCIM 仅 +4 → 密度 130 kB/mm²（65nm）/ 860 kB/mm²（14nm）", W // 2, 462, 13, fill=(180, 220, 200), anchor="mm")
    txt(d, "SNG 复用 &gt;32×（激活存内存复用 + 滤波器 32 行共享）→ 摊薄 25× 的 SNG 能耗", W // 2, 490, 13, fill=(210, 225, 240), anchor="mm")

# ================= v03 avg pooling skip =================
def v03(d, i, n):
    t = i / n
    title(d, "计算跳算：平均池化把流长缩短 4×")
    k = i % 40
    # left: 4-input avg pooling via MUX
    panel(d, 40, 80, 440, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "平均池化 = K²:1 MUX（随机选输入）", 260, 102, 14, fill=(170, 240, 200), anchor="mm")
    # 4 inputs streams (8 bits each)
    streams = [
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1],
    ]
    sel = k % 4
    bs = 40; bx = 90; by = 130
    for r in range(4):
        txt(d, "in%d" % r, 70, by + r * 40 + 14, 11, fill=(140, 200, 255), anchor="rm")
        for c in range(8):
            x = bx + c * bs
            active = (c == k % 8)
            v = streams[r][c]
            col = (44, 34, 20) if v else (30, 24, 16)
            if r == sel and active: col = (60, 80, 30)
            d.rectangle([x, by + r * 40, x + bs - 4, by + r * 40 + 30], fill=col, outline=(240, 180, 70) if (r == sel and active) else (90, 70, 40))
            txt(d, str(v), x + (bs - 4) / 2, by + r * 40 + 15, 10, fill=(255, 255, 255), anchor="mm")
    # MUX output
    txt(d, "MUX 选中 in%d（控制位随机）" % sel, 260, by + 4 * 40 + 16, 12.5, fill=(255, 210, 130), anchor="mm")
    txt(d, "每输入被选 1/4 的序列长度 → 平均", 260, by + 4 * 40 + 42, 12, fill=(190, 230, 210), anchor="mm")

    # right: skipping
    panel(d, 500, 80, 420, 330, (22, 26, 44), (150, 120, 200))
    txt(d, "跳算：未选中的位不计算", 710, 102, 14, fill=(210, 190, 240), anchor="mm")
    # show selected bits pattern per input (每输入 1/4)
    for r in range(4):
        y = 130 + r * 52
        txt(d, "in%d" % r, 540, y + 10, 11, fill=(200, 185, 230), anchor="rm")
        for c in range(8):
            x = 560 + c * 40
            chosen = ((c + r) % 4 == 0)  # each input contributes 2 of 8 bits
            d.rectangle([x, y, x + 34, y + 24], fill=(40, 90, 130) if chosen else (30, 30, 44), outline=(140, 200, 255) if chosen else (90, 90, 110))
            txt(d, str(streams[r][c]) if chosen else "·", x + 17, y + 12, 10, fill=(255, 255, 255) if chosen else (120, 130, 150), anchor="mm")
    txt(d, "每输入只需算 N/4 位（原 N 位流）", 710, 360, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "→ 流长缩短 4× · 能耗×4 优势", 710, 388, 13.5, fill=(255, 210, 130), anchor="mm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "8-bit 无池化：SCIM vs 模拟 CIM 仅 1.6×（256 vs 64 次）→ 带池化跳算：6.4×", W // 2, 462, 13, fill=(180, 220, 200), anchor="mm")
    txt(d, "14nm 宏：8-bit 35 TOPS/W → 带平均池化 140 TOPS/W（4× 提升）", W // 2, 490, 13.5, fill=(210, 225, 240), anchor="mm")

def main():
    jobs = [("v01", v01, 200), ("v02", v02, 200), ("v03", v03, 200)]
    for name, fn, nf in jobs:
        fd = os.path.join(ROOT, "_work_vid18", name)
        make_frames(fn, nf, fd)
        encode(fd, os.path.join(VDIR, name + ".mp4"))
        print(name, "done", os.path.getsize(os.path.join(VDIR, name + ".mp4")))

if __name__ == "__main__":
    main()
