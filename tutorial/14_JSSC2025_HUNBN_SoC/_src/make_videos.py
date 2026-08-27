# -*- coding: utf-8 -*-
"""论文14演示视频：v01 PE vs DIMC / v02 宏级1bitx2bit MAC / v03 数据搬移"""
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

# ================= v01 PE vs DIMC =================
def v01(d, i, n):
    t = i / n
    title(d, "数字 PE 阵列 vs DIMC：权重搬运 vs 权重就地")
    k = int(t * 10) % 2  # 0=PE, 1=DIMC
    # left: PE
    panel(d, 40, 80, 430, 330, (26, 18, 18), (210, 110, 100))
    txt(d, "传统数字 PE 阵列", 255, 104, 16, fill=(255, 190, 180), anchor="mm")
    # weight SRAM
    panel(d, 70, 130, 160, 60, (45, 25, 22), (210, 110, 100), r=8)
    txt(d, "权重 SRAM（片外/大容量）", 150, 160, 13, fill=(255, 210, 200), anchor="mm")
    # PE
    panel(d, 280, 130, 160, 60, (30, 30, 38), (140, 150, 170), r=8)
    txt(d, "PE 计算单元", 360, 160, 13, fill=(210, 220, 235), anchor="mm")
    # arrows (animation: weight moves back and forth)
    ax = 150 + (i % 30) * 3
    d.line([235, 160, 276, 160], fill=(255, 140, 120), width=3)
    d.polygon([(276, 154), (288, 160), (276, 166)], fill=(255, 140, 120))
    d.line([360, 190, 360, 230, 150, 230, 150, 195], fill=(255, 140, 120), width=2)
    d.polygon([(144, 195), (150, 183), (156, 195)], fill=(255, 140, 120))
    txt(d, "权重反复搬运（高能耗）", 255, 260, 14, fill=(255, 180, 165), anchor="mm")
    txt(d, "瓶颈：SRAM 访问能耗高 + 寄存器爆炸", 255, 290, 13, fill=(230, 190, 180), anchor="mm")
    txt(d, "← 数据搬移能耗 ≫ 计算能耗（Horowitz）", 255, 330, 13, fill=(255, 220, 210), anchor="mm")
    txt(d, "每周期都搬 → 能效被访存卡死", 255, 360, 13, fill=(255, 220, 210), anchor="mm")

    # right: DIMC
    panel(d, 500, 80, 420, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "DIMC（本论文）", 710, 104, 16, fill=(170, 240, 200), anchor="mm")
    panel(d, 530, 130, 180, 60, (22, 48, 38), (70, 190, 130), r=8)
    txt(d, "6T SRAM（存权重）", 620, 150, 13, fill=(180, 240, 210), anchor="mm")
    txt(d, "256×96 pushed-rule 6T", 620, 172, 11, fill=(150, 210, 185), anchor="mm")
    panel(d, 740, 130, 150, 60, (22, 48, 38), (70, 190, 130), r=8)
    txt(d, "本地 MAC 单元", 815, 150, 13, fill=(180, 240, 210), anchor="mm")
    txt(d, "就地乘加", 815, 172, 11, fill=(150, 210, 185), anchor="mm")
    d.line([714, 160, 736, 160], fill=(90, 220, 160), width=3)
    d.polygon([(736, 154), (748, 160), (736, 166)], fill=(90, 220, 160))
    txt(d, "权重就地存储 → 不搬移", 710, 230, 14, fill=(170, 240, 200), anchor="mm")
    txt(d, "直接省 28% 功耗 [23]", 710, 260, 13, fill=(190, 230, 210), anchor="mm")
    txt(d, "但要：模型能全部装进 DIMC", 710, 300, 13, fill=(210, 240, 225), anchor="mm")
    txt(d, "→ HUNBN：508 kB/mm² 高密度", 710, 330, 13, fill=(120, 230, 180), anchor="mm")
    txt(d, "→ 整个边缘 CNN 装片上，权重加载零成本", 710, 360, 13, fill=(210, 240, 225), anchor="mm")

    # progress
    d.rectangle([40, 440, W - 40, 446], fill=(40, 60, 85))
    d.rectangle([40, 440, 40 + (W - 80) * t, 446], fill=(70, 190, 140))
    txt(d, "结论：DIMC 省搬移的前提是「容量够大」→ 高存储密度 = 系统级能效的第一把钥匙", W // 2, 468, 14, fill=(210, 225, 240), anchor="mm")
    txt(d, "系统级能效 = 宏级能效 × 宏级面积效率 × 阵列利用率（三层都要抓）", W // 2, 496, 13, fill=(180, 200, 220), anchor="mm")

# ================= v02 macro 1bitx2bit MAC =================
def v02(d, i, n):
    t = i / n
    title(d, "DIMC 宏：1-bit×2-bit 乘法 + 同步读计算")
    # weights bits panel
    panel(d, 40, 80, 440, 320, (16, 28, 40), (60, 140, 190))
    txt(d, "每周期：24 个 4b 权重读出（同权位分组）", 260, 104, 14, fill=(190, 220, 245), anchor="mm")
    # 4 groups of weight bits
    for g in range(4):
        gx = 70 + g * 100
        panel(d, gx, 120, 88, 70, (20, 40, 58), (90, 170, 220), r=8)
        txt(d, "组%d (权位%d)" % (g, g), gx + 44, 138, 11, fill=(140, 200, 255), anchor="mm")
        # 3 of 24 bits
        for b in range(4):
            v = (g + b) % 2
            d.rectangle([gx + 8 + b * 19, 158, gx + 8 + b * 19 + 15, 176], fill=(40, 90, 130) if v else (18, 40, 62))
            txt(d, str(v), gx + 8 + b * 19 + 7, 167, 10, fill=(255, 255, 255), anchor="mm")
    txt(d, "24 位同权位 → 1 个 2-bit 激活位做乘法", 260, 210, 12.5, fill=(190, 220, 245), anchor="mm")
    # activation bits
    panel(d, 70, 232, 380, 60, (24, 40, 30), (90, 190, 130), r=8)
    txt(d, "2-bit 输入激活 I[1:0]", 260, 250, 12.5, fill=(170, 240, 200), anchor="mm")
    txt(d, "BL 承载 bit0（权重原值）、BLB 承载 bit1（权重反相）", 260, 274, 11.5, fill=(190, 230, 210), anchor="mm")
    # multiplication detail
    txt(d, "1b×2b 乘法：W_bit × {I1, I0} = 两个部分积（BL/BLB 各一个）", 260, 320, 12.5, fill=(200, 230, 210), anchor="mm")
    txt(d, "重复 2 周期（2-bit 串行）→ 4b×4b MAC 完成", 260, 348, 13.5, fill=(120, 230, 180), anchor="mm")
    txt(d, "比传统位串行快 2 倍", 260, 376, 12, fill=(190, 230, 210), anchor="mm")

    # timing panel
    panel(d, 500, 80, 420, 320, (20, 20, 34), (150, 120, 200))
    txt(d, "同步读/计算时序（论文 Fig.6）", 710, 104, 14, fill=(220, 200, 240), anchor="mm")
    # waveform
    x0, x1, y0 = 540, 880, 130
    # pe pulse
    txt(d, "pe (预充)", 525, 150, 11, fill=(170, 200, 220), anchor="rm")
    d.line([540, 150, 570, 150, 570, 142, 610, 142, 610, 150, 880, 150], fill=(150, 200, 255), width=2)
    txt(d, "Φ 脉冲（周期 A）", 700, 170, 11, fill=(150, 200, 255), anchor="mm")
    # re pulse
    txt(d, "re (读)", 525, 200, 11, fill=(170, 200, 220), anchor="rm")
    d.line([540, 200, 600, 200, 600, 192, 650, 192, 650, 200, 880, 200], fill=(255, 210, 130), width=2)
    txt(d, "WL 脉冲（周期 B）→ 不同周期 → 无破坏性读", 700, 220, 11, fill=(255, 210, 130), anchor="mm")
    # compute
    txt(d, "计算", 525, 258, 11, fill=(170, 200, 220), anchor="rm")
    d.line([540, 258, 580, 258, 580, 250, 630, 250, 630, 258, 680, 258, 680, 250, 730, 250, 730, 258, 780, 258, 780, 250, 830, 250, 830, 258, 880, 258], fill=(180, 230, 170), width=2)
    txt(d, "一次读 → 多次计算（SUM=BL×不同输入 I）", 700, 278, 11, fill=(180, 230, 170), anchor="mm")
    # refresh
    txt(d, "刷新", 525, 306, 11, fill=(170, 200, 220), anchor="rm")
    d.line([540, 306, 700, 306, 700, 298, 740, 298, 740, 306, 800, 306, 800, 298, 840, 298], fill=(120, 200, 160), width=2)
    txt(d, "WL 插刷新脉冲恢复 BL 全摆幅（ce 保持高→不影响吞吐）", 700, 326, 11, fill=(120, 200, 160), anchor="mm")
    txt(d, "免延迟线：Φ/WL 摊两个周期 → 临界路径缩短", 710, 356, 12.5, fill=(200, 230, 210), anchor="mm")
    txt(d, "MAC 逻辑不在临界路径 → 供电电压可降 → 更省能", 710, 382, 12, fill=(180, 220, 200), anchor="mm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "宏级能效关键：BL/BLB 双线乘法 + 同步操作 + split MAC（定制乘法/早期加法树，面积 −20%）", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "低电压域加法树 + 静态电平移位器（面积 +2%）→ 宏级 126.3 TOPS/W", W // 2, 490, 13, fill=(180, 220, 200), anchor="mm")

# ================= v03 data movement =================
def v03(d, i, n):
    t = i / n
    title(d, "数据搬移优化：滑动窗口 + 转置卷积数据前瞻")
    k = int(t * 12) % 2
    # ---- normal conv ----
    panel(d, 40, 80, 430, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "正常卷积（3×3）· 滑动窗口", 255, 104, 15, fill=(170, 240, 200), anchor="mm")
    # feature map grid
    ox, oy, cs = 90, 130, 52
    for r in range(4):
        for c in range(4):
            v = (r + c) % 2
            d.rectangle([ox + c * cs, oy + r * cs, ox + c * cs + cs - 4, oy + r * cs + cs - 4],
                        fill=(30, 70, 55) if v else (16, 40, 32))
    # sliding window position
    wx = (i // 6) % 2
    d.rectangle([ox + wx * cs - 3, oy - 3, ox + wx * cs + cs * 3 - 1, oy + cs * 3 - 1], outline=(255, 200, 90), width=3)
    txt(d, "3×3 窗口滑动（每步只移 1 列）", ox + cs * 1.5, oy + cs * 4 + 16, 12, fill=(255, 210, 130), anchor="mm")
    # three-deep register
    panel(d, 70, 350, 370, 44, (24, 46, 38), (90, 190, 130), r=8)
    txt(d, "三深度寄存器缓存 3 行 PixelPack → 窗口数据复用", 255, 372, 12, fill=(180, 240, 210), anchor="mm")
    txt(d, "相邻输出共享输入 → 搬移最小化", 255, 396, 12, fill=(210, 240, 225), anchor="mm")
    # bank no-conflict
    txt(d, "RowList 按 mod-3 分布 3 bank → 无访问冲突", 255, 330, 11.5, fill=(150, 210, 185), anchor="mm")

    # ---- transposed conv ----
    panel(d, 500, 80, 420, 330, (22, 20, 36), (150, 120, 200))
    txt(d, "转置卷积（4×4）· 零插入 + 数据前瞻", 710, 104, 15, fill=(220, 200, 240), anchor="mm")
    # zero-inserted feature map
    ox2, oy2, cs2 = 560, 130, 34
    for r in range(4):
        for c in range(4):
            if r % 2 == 1 or c % 2 == 1:
                d.rectangle([ox2 + c * cs2, oy2 + r * cs2, ox2 + c * cs2 + cs2 - 2, oy2 + r * cs2 + cs2 - 2], fill=(40, 34, 20))
                txt(d, "0", ox2 + c * cs2 + cs2 // 2, oy2 + r * cs2 + cs2 // 2, 9, fill=(255, 210, 130), anchor="mm")
            else:
                d.rectangle([ox2 + c * cs2, oy2 + r * cs2, ox2 + c * cs2 + cs2 - 2, oy2 + r * cs2 + cs2 - 2], fill=(34, 30, 60))
    txt(d, "输入插零上采样（黄色=零）", 760, 300, 12, fill=(220, 200, 240), anchor="mm")
    txt(d, "插零 → 新输入请求频率减半", 760, 324, 12, fill=(200, 180, 225), anchor="mm")
    # look-ahead
    panel(d, 540, 340, 360, 54, (34, 28, 50), (150, 120, 200), r=8)
    txt(d, "t=n 预取 PixelPack1（通道 0–17）→ t=n+1 取 PixelPack2（18–35）", 720, 358, 11.5, fill=(220, 200, 240), anchor="mm")
    txt(d, "16 种细粒度取数模式 → 全速执行转置卷积", 720, 380, 11.5, fill=(190, 170, 220), anchor="mm")

    # bottom
    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "四级数据结构（PixelPack→RowList→ColList→MapList）配合滑动窗口 → 输入搬移最小化", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "部分和 12-bit 扩展 PixelPack（3 bank 合并）；输出 4-bit 单 PixelPack；P2/P3 双缓冲", W // 2, 490, 13, fill=(180, 200, 220), anchor="mm")

def main():
    jobs = [("v01", v01, 180), ("v02", v02, 210), ("v03", v03, 210)]
    for name, fn, nf in jobs:
        fd = os.path.join(ROOT, "_work_vid14", name)
        make_frames(fn, nf, fd)
        encode(fd, os.path.join(VDIR, name + ".mp4"))
        print(name, "done", os.path.getsize(os.path.join(VDIR, name + ".mp4")))

if __name__ == "__main__":
    main()
