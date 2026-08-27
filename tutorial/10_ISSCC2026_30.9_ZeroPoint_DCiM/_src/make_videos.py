# -*- coding: utf-8 -*-
"""生成教学演示视频（PIL 逐帧绘制 + ffmpeg H.264 编码）

v01_booth.mp4        : Radix-4 Booth 编码乘法教学动画
v02_datapath.mp4     : DCiM 数据流流水线工作流程动画（主演示）
v03_double_buffer.mp4: 双缓冲权重更新与计算并行动画
"""
import os, subprocess, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\10_ISSCC2026_30.9_ZeroPoint_DCiM\assets\videos"
os.makedirs(OUT, exist_ok=True)

FONTS = {
    "title": ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 40),
    "big":   ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 30),
    "med":   ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 24),
    "text":  ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22),
    "small": ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 18),
    "mono":  ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 22),
}

INK   = (26, 35, 50, 255)
GRAY  = (107, 122, 147, 255)
BLUE  = (14, 90, 138, 255)
BLUE2 = (15, 124, 182, 255)
GREEN = (29, 138, 95, 255)
ORANGE= (232, 163, 61, 255)
RED   = (194, 94, 46, 255)
PURPLE= (107, 63, 160, 255)
BG    = (10, 17, 25, 255)
PANEL = (18, 30, 46, 255)
LINE  = (60, 82, 110, 255)
WHITE = (255, 255, 255, 255)

def draw_panel(d, box, title=None, fill=PANEL, outline=LINE):
    d.rounded_rectangle(box, radius=16, fill=fill, outline=outline, width=2)
    if title:
        d.text((box[0] + 18, box[1] + 10), title, font=FONTS["med"], fill=WHITE)

def progress_bar(d, x, y, w, frac, color=GREEN, h=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(40, 60, 84, 255))
    if frac > 0:
        d.rounded_rectangle([x, y, x + w * frac, y + h], radius=8, fill=color)

def center_text(d, cx, cy, s, font, fill=WHITE):
    bb = d.textbbox((0, 0), s, font=font)
    d.text((cx - (bb[2]-bb[0])/2, cy - (bb[3]-bb[1])/2), s, font=font, fill=fill)

def ease(t):
    return 1 - (1 - t) ** 3

def new_frame():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)

def write_video(frames, name):
    path = os.path.join(OUT, name)
    tmpdir = os.path.join(OUT, "_frames_" + name.replace(".mp4", ""))
    os.makedirs(tmpdir, exist_ok=True)
    for i, f in enumerate(frames):
        f.save(os.path.join(tmpdir, f"f{i:05d}.png"))
    ff = r"C:\Users\weiyu\Desktop\CIM研究\_ffmpeg\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
    cmd = [ff, "-y", "-framerate", str(FPS), "-i", os.path.join(tmpdir, "f%05d.png"),
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", path]
    subprocess.run(cmd, check=True, capture_output=True)
    for f in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, f))
    os.rmdir(tmpdir)
    print("wrote", name, len(frames), "frames ->", os.path.getsize(path), "bytes")

def slide(d, t, s, n=5):
    """分段文字滑入：0..n 段依次进入"""
    seg = min(int(t * n), n)
    out = ""
    for i in range(seg):
        out += s[i] + "\n"
    return out

# =====================================================================
# v01: Booth 编码乘法动画
# =====================================================================
def booth_demo():
    X = 85; Y = 42
    groups = [("(y1 y0 y-1) = (1 0 0)", "−2X", -2*X, 0),
              ("(y3 y2 y1) = (1 0 1)", "−X",  -X, 2),
              ("(y5 y4 y3) = (1 0 1)", "−X",  -X, 4),
              ("(y7 y6 y5) = (0 0 1)", "+X",  X, 6)]
    total = sum(g[2] * (2 ** g[3]) for g in groups)
    assert total == X * Y, (total, X*Y)

    frames = []
    # 阶段 1：介绍算式
    for i in range(FPS * 4):
        im, d = new_frame()
        t = (i % FPS) / FPS
        center_text(d, W//2, 150, "Radix-4 Booth 编码：把乘法拆成“错位的部分积相加”", FONTS["title"], WHITE)
        draw_panel(d, [340, 260, 940, 430])
        center_text(d, W//2, 320, f"乘数 X（被乘数）= {X}", FONTS["big"], WHITE)
        center_text(d, W//2, 368, f"乘数 Y（被 Booth 编码）= {Y} = 00101010₂", FONTS["big"], WHITE)
        center_text(d, W//2, 416, f"目标：X × Y = {X*Y}", FONTS["big"], ORANGE)
        if t > 0.5:
            center_text(d, W//2, 560, "Y 每 2 位一组（重叠 1 位），共 4 组 → 4 个部分积", FONTS["text"], GRAY)
        frames.append(im)

    # 阶段 2：逐组编码
    for gi in range(4):
        for i in range(FPS * 3):
            im, d = new_frame()
            t = (i % FPS) / FPS
            center_text(d, W//2, 100, "第 %d 组：%s → %s" % (gi+1, groups[gi][0], groups[gi][1]), FONTS["big"], ORANGE)
            # 表格
            draw_panel(d, [90, 150, 1190, 640])
            d.text((120, 180), "Y 的二进制：", font=FONTS["text"], fill=WHITE)
            d.text((330, 180), "0 0 1 0 1 0 1 0", font=FONTS["mono"], fill=WHITE)
            y_vis = ["y7", "y6", "y5", "y4", "y3", "y2", "y1", "y0"]
            for j, lbl in enumerate(y_vis):
                d.text((350 + j*56, 220), lbl, font=FONTS["small"], fill=GRAY)
            d.text((120, 270), f"操作 = {groups[gi][1]}   →   部分积 PP{gi} = {groups[gi][2]}，移位 {groups[gi][3]} 位",
                   font=FONTS["text"], fill=WHITE)
            d.text((120, 320), f"PP{gi} 的实际数值 = {groups[gi][2]} × 2^{groups[gi][3]} = {groups[gi][2] * (2**groups[gi][3])}",
                   font=FONTS["text"], fill=ORANGE)
            # 已生成的部分积
            for k in range(gi + 1):
                g = groups[k]
                d.text((120, 380 + k*48), f"PP{k}（移位 {g[3]}）: {g[2]} × 2^{g[3]} = {g[2]*(2**g[3])}",
                       font=FONTS["mono"], fill=(200, 215, 235, 255))
            if t > 0.6 and gi < 3:
                center_text(d, W//2, 660, "下一组 →", FONTS["text"], GRAY)
            frames.append(im)

    # 阶段 3：求和
    for i in range(FPS * 4):
        im, d = new_frame()
        t = (i % FPS) / FPS
        center_text(d, W//2, 100, "把 4 个错位的部分积相加", FONTS["title"], WHITE)
        draw_panel(d, [90, 160, 1190, 560])
        acc = 0
        for k in range(4):
            g = groups[k]
            acc += g[2] * (2 ** g[3])
            d.text((120, 200 + k*62), f"PP{k}（移位 {g[3]}）: {g[2]} × 2^{g[3]} = {g[2]*(2**g[3])}",
                   font=FONTS["mono"], fill=(200, 215, 235, 255))
        d.line([120, 460, 1000, 460], fill=ORANGE, width=3)
        center_text(d, W//2, 500, f"X × Y = {X} × {Y} = {acc}", FONTS["big"], ORANGE)
        if t > 0.5:
            center_text(d, W//2, 610, "若直接 9b×9b：需要 5 个部分积、每个 10b 宽 → 本论文通过映射压回 8b×8b：4 个部分积、每个 9b 宽",
                        FONTS["small"], GRAY)
        frames.append(im)
    return frames

# =====================================================================
# v02: 数据流流水线动画
# =====================================================================
def datapath_demo():
    stages = [
        ("第 1 级：无符号→有符号转换", "128 个激活并行\nMSB 条件取反 + 零点偏置", BLUE),
        ("第 2 级：部分积生成 + 32 路 CSA", "128 乘法 → 512 部分积\n先跨乘数相加", PURPLE),
        ("第 3 级：移位合并", "4 个错位部分积和相加\n每个 bank 完成 32 路点积", PURPLE),
        ("第 4 级：bank 求和 + 零点修正", "Σ 4 个 bank = 128 路 MAC\n+ 三个修正项", ORANGE),
    ]
    frames = []
    NCYC = 14  # 演示 14 个周期
    for cyc in range(NCYC):
        for i in range(FPS):
            im, d = new_frame()
            # 标题
            center_text(d, W//2, 56, "DCiM 数据流流水线：一个周期内完成 4096 个 MAC", FONTS["title"], WHITE)
            # 时钟
            d.text((1050, 24), f"周期 {cyc+1}/{NCYC}", font=FONTS["med"], fill=ORANGE)

            # 输入
            draw_panel(d, [40, 120, 270, 240], "输入")
            center_text(d, 155, 160, "128 个激活", FONTS["text"], WHITE)
            center_text(d, 155, 196, "8b 零点量化", FONTS["small"], GRAY)
            # 输入脉冲
            p = (i % 12) / 12
            d.rectangle([70, 212, 70 + 160 * p, 228], fill=ORANGE)
            if i % 12 < 3:
                d.rectangle([40, 120, 270, 240], outline=RED, width=3)

            # 阶段 1
            draw_panel(d, [320, 120, 620, 240], "第 1 级")
            center_text(d, 470, 160, "无符号→有符号", FONTS["text"], WHITE)
            center_text(d, 470, 196, "MSB 取反 + 零点偏置", FONTS["small"], GRAY)
            d.rectangle([350, 212, 350 + 220 * p, 228], fill=BLUE2)

            # 广播
            if 0.25 < p < 0.9:
                d.line([620, 180, 940, 180], fill=BLUE2, width=4)

            # 列 1..4（示意 32 列）
            for c, cx in enumerate([660, 780, 900, 1020]):
                draw_panel(d, [cx, 280, cx + 110, 600], f"列 {c+1}")
                # 权重
                d.rounded_rectangle([cx+10, 300, cx+100, 380], radius=8, fill=(24, 44, 68, 255), outline=GREEN, width=2)
                center_text(d, cx+55, 322, "权重", FONTS["small"], WHITE)
                center_text(d, cx+55, 350, "12T 锁存", FONTS["small"], GRAY)
                # bank
                for b in range(3):
                    d.rounded_rectangle([cx+10, 400+b*46, cx+100, 436+b*46], radius=6, fill=(28, 40, 66, 255), outline=PURPLE, width=2)
                center_text(d, cx+55, 560, "4 bank", FONTS["small"], GRAY)
                # 输出脉冲
                if p > 0.55:
                    d.rounded_rectangle([cx+10, 572, cx+100, 588], radius=6, fill=ORANGE)

            # 阶段标签（底部）
            draw_panel(d, [40, 300, 600, 600], "流水线阶段")
            for s, (t, sub, col) in enumerate(stages):
                yy = 330 + s * 68
                d.rounded_rectangle([70, yy, 120, yy + 40], radius=6, fill=col)
                d.text((135, yy + 4), t, font=FONTS["text"], fill=WHITE)
                d.text((135, yy + 30), sub.replace("\n", " "), font=FONTS["small"], fill=GRAY)
                # 数据块流动
                if 0.15 < p < 0.85:
                    fx = 70 + (p - 0.15) / 0.7 * 430
                    d.ellipse([fx - 10, yy + 10, fx + 10, yy + 30], fill=ORANGE)

            # 每周期完成的 MAC
            center_text(d, 660, 645, "每列每周期 128 路 MAC × 32 列 = 4096 MAC/周期 → @2.62GHz = 21.5 TOPS",
                        FONTS["small"], GRAY)
            frames.append(im)
    return frames

# =====================================================================
# v03: 双缓冲动画
# =====================================================================
def double_buffer_demo():
    frames = []
    NCYC = 96
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center_text(d, W//2, 60, "双缓冲：计算与权重更新并行", FONTS["title"], WHITE)

            active = "A" if (cyc % 64) < 32 else "B"
            writing = "B" if active == "A" else "A"

            # 权重组 A
            draw_panel(d, [80, 140, 600, 300], "权重组 A（12T 锁存）")
            if active == "A":
                d.rounded_rectangle([100, 200, 560, 260], radius=10, fill=(24, 60, 44, 255), outline=GREEN, width=3)
                center_text(d, 330, 230, "参与计算（128 路 MAC 持续进行）", FONTS["text"], WHITE)
                # 激活脉冲流入
                if t < 0.8:
                    for k in range(6):
                        x = 110 + ((t + k/6) % 1) * 440
                        d.ellipse([x, 180, x+14, 194], fill=ORANGE)
            else:
                d.rounded_rectangle([100, 200, 560, 260], radius=10, fill=(40, 48, 66, 255), outline=LINE, width=2)
                center_text(d, 330, 230, "空闲（等待切换）", FONTS["text"], GRAY)

            # 权重组 B
            draw_panel(d, [680, 140, 1200, 300], "权重组 B（12T 锁存）")
            if writing == "B":
                d.rounded_rectangle([700, 200, 1160, 260], radius=10, fill=(54, 44, 24, 255), outline=ORANGE, width=3)
                center_text(d, 930, 230, "后台写入新权重…", FONTS["text"], WHITE)
                frac = ((cyc % 64) + t) / 32
                if frac <= 1:
                    progress_bar(d, 700, 280, 460, frac, ORANGE)
                    center_text(d, 930, 308, f"写入进度 {min(frac*100,100):.0f}%  （32 周期写完 128 个权重）", FONTS["small"], GRAY)
                else:
                    center_text(d, 930, 290, "写入完成，等待切换", FONTS["small"], GRAY)
            else:
                d.rounded_rectangle([700, 200, 1160, 260], radius=10, fill=(24, 44, 68, 255), outline=GREEN, width=3)
                center_text(d, 930, 230, "参与计算（切换后）", FONTS["text"], WHITE)
                if t < 0.8:
                    for k in range(6):
                        x = 710 + ((t + k/6) % 1) * 440
                        d.ellipse([x, 180, x+14, 194], fill=ORANGE)

            # 时间轴
            draw_panel(d, [80, 360, 1200, 640], "时间轴（每个小格 = 8 周期）")
            for k in range(12):
                x0 = 110 + k * 96
                x1 = x0 + 88
                cA = GREEN if (k < 4) else LINE
                cB = LINE if (k < 4) else GREEN
                d.rectangle([x0, 420, x1, 450], fill=(24, 44, 68, 255), outline=cA, width=2)
                d.rectangle([x0, 470, x1, 500], fill=(54, 44, 24, 255) if (k < 4) else (24, 60, 44, 255), outline=cB, width=2)
            d.text((110, 400), "权重组 A", font=FONTS["small"], fill=GREEN)
            d.text((110, 508), "权重组 B", font=FONTS["small"], fill=ORANGE)
            d.text((110, 556), "0", font=FONTS["small"], fill=GRAY)
            d.text((600, 556), "32", font=FONTS["small"], fill=GRAY)
            d.text((1100, 556), "64", font=FONTS["small"], fill=GRAY)
            d.text((110, 590), "A 计算 / B 写入 ───────── 32 周期后切换 ───────── B 计算 / A 写入",
                   font=FONTS["small"], fill=GRAY)
            # 当前指针
            pos = 110 + (cyc % 96) / 96 * 1056
            d.polygon([(pos, 440), (pos-8, 452), (pos+8, 452)], fill=RED)
            center_text(d, 640, 628, "要点：计算从不因更新权重而停顿；写功耗占比可降到 1%，能效达到峰值",
                        FONTS["small"], GRAY)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(booth_demo(), "v01_booth.mp4")
    write_video(datapath_demo(), "v02_datapath.mp4")
    write_video(double_buffer_demo(), "v03_double_buffer.mp4")
    print("ALL VIDEOS DONE")
