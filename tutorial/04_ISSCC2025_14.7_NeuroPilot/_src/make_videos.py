# -*- coding: utf-8 -*-
"""论文04演示视频：波前传播 / DDS / TsCFP"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\04_ISSCC2025_14.7_NeuroPilot\assets\videos"
os.makedirs(OUT, exist_ok=True)
FONTS = {
    "title": ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 38),
    "med":   ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 24),
    "text":  ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 21),
    "small": ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 17),
}
BG = (10, 17, 25); PANEL = (18, 30, 46); LINE = (60, 82, 110)
GRAY = (127, 147, 173); WHITE = (240, 244, 250)
BLUE = (30, 144, 220); GREEN = (60, 190, 140); ORANGE = (240, 180, 70)
PURPLE = (170, 120, 220); RED = (230, 110, 90)

def new_frame():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)

def center(d, cx, cy, s, font, fill=WHITE):
    bb = d.textbbox((0, 0), s, font=font)
    d.text((cx - (bb[2]-bb[0])/2, cy - (bb[3]-bb[1])/2), s, font=font, fill=fill)

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
    print("wrote", name, len(frames), "frames")

# ============ v01 波前传播 ============
def wavefront_demo():
    frames = []
    NCYC = 30
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "波前传播：信号从 START 像水波一样扩散", FONTS["title"], WHITE)
            # 12x10 网格
            gx, gy = 150, 130
            cell = 52
            for r in range(10):
                for c in range(12):
                    x = gx + c * cell; y = gy + r * cell
                    dist = abs(r - 8) + abs(c - 2)
                    reached = dist <= cyc
                    obstacle = (r == 4 and 4 <= c <= 8)
                    d.rectangle([x, y, x + cell - 4, y + cell - 4],
                                fill=(50, 40, 40, 255) if obstacle else (24, 44, 70, 255) if reached else (16, 24, 36, 255),
                                outline=GREEN if reached and not obstacle else (GRAY if not obstacle else RED), width=2 if reached else 1)
            # START/END
            d.ellipse([gx + 2 * cell + 8, gy + 8 * cell + 8, gx + 2 * cell + 30, gy + 8 * cell + 30], fill=GREEN)
            center(d, gx + 2 * cell + 19, gy + 8 * cell + 19, "S", FONTS["small"], BG)
            d.ellipse([gx + 9 * cell + 8, gy + 1 * cell + 8, gx + 9 * cell + 30, gy + 1 * cell + 30], fill=RED)
            center(d, gx + 9 * cell + 19, gy + 1 * cell + 19, "E", FONTS["small"], BG)
            center(d, 640, 660, "每个 PE 记住方向 → 波前到达 END 后回溯出路径（此图为传播演示）", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v02 DDS ============
def dds_demo():
    frames = []
    NCYC = 22
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "DDS 双向搜索：START 与 END 同时出发", FONTS["title"], WHITE)
            gx, gy = 200, 130
            cell = 52
            for r in range(10):
                for c in range(12):
                    x = gx + c * cell; y = gy + r * cell
                    ds = abs(r - 8) + abs(c - 2)
                    de = abs(r - 1) + abs(c - 9)
                    reached_s = ds <= cyc
                    reached_e = de <= cyc
                    obstacle = (r == 4 and 4 <= c <= 8)
                    fill = (50, 40, 40, 255) if obstacle else \
                           (26, 60, 44, 255) if reached_s and not reached_e else \
                           (60, 40, 30, 255) if reached_e and not reached_s else \
                           (30, 50, 40, 255) if reached_s and reached_e else (16, 24, 36, 255)
                    outline = GREEN if reached_s and not reached_e else RED if reached_e and not reached_s else ORANGE if reached_s and reached_e else GRAY
                    d.rectangle([x, y, x + cell - 4, y + cell - 4], fill=fill, outline=outline, width=2 if reached_s or reached_e else 1)
            d.ellipse([gx + 2 * cell + 8, gy + 8 * cell + 8, gx + 2 * cell + 30, gy + 8 * cell + 30], fill=GREEN)
            center(d, gx + 2 * cell + 19, gy + 8 * cell + 19, "S", FONTS["small"], BG)
            d.ellipse([gx + 9 * cell + 8, gy + 1 * cell + 8, gx + 9 * cell + 30, gy + 1 * cell + 30], fill=RED)
            center(d, gx + 9 * cell + 19, gy + 1 * cell + 19, "E", FONTS["small"], BG)
            center(d, 640, 660, "绿=来自 START 的波前 · 红=来自 END 的波前 · 橙=交汇 → 时间 −2.1×、功耗 −1.13×", FONTS["small"], ORANGE)
            frames.append(im)
    return frames

# ============ v03 TsCFP ============
def tscfp_demo():
    frames = []
    NCYC = 24
    steps = [
        ("① 生成最小清晰粗图", "迭代分辨率 + 路径比打分", BLUE),
        ("② 粗图最短路径（走廊）", "32×32 段逐段导引（SDS/DDS）", PURPLE),
        ("③ 沿走廊求细路径", "原图切条带逐段精算", GREEN),
    ]
    for si in range(3):
        for i in range(FPS * 3):
            im, d = new_frame()
            t = i / FPS
            center(d, W//2, 56, "TsCFP 三步粗/细路径：" + steps[si][0], FONTS["title"], steps[si][2])
            # 大图示意
            d.rounded_rectangle([80, 140, 1200, 560], radius=10, fill=PANEL, outline=steps[si][2], width=2)
            if si == 0:
                for r in range(14):
                    for c in range(28):
                        x = 100 + c * 39; y = 160 + r * 28
                        d.rectangle([x, y, x + 37, y + 26], fill=(26, 40, 60, 255), outline=LINE, width=1)
                center(d, 640, 620, "1024×1024 大图 → 迭代降低分辨率 → 最小清晰粗图（绿色区域为可通行）", FONTS["text"], WHITE)
            elif si == 1:
                for k in range(10):
                    x0 = 100 + k * 110
                    d.rounded_rectangle([x0, 200, x0 + 100, 300], radius=8, fill=(36, 30, 46, 255), outline=PURPLE, width=2)
                    center(d, x0 + 50, 250, f"段 {k}", FONTS["small"], PURPLE)
                d.line([105, 350, 1150, 350], fill=ORANGE, width=6)
                center(d, 640, 400, "粗路径 = 走廊（橙色粗线）", FONTS["text"], ORANGE)
                center(d, 640, 620, "每段由上一段 END + 原图方向决定起点 → 走廊贯穿大图", FONTS["text"], WHITE)
            else:
                for k in range(6):
                    x0 = 100 + k * 190
                    d.rounded_rectangle([x0, 200, x0 + 180, 460], radius=8, fill=(26, 44, 70, 255), outline=GREEN, width=2)
                    center(d, x0 + 90, 240, f"细条带 {k}", FONTS["small"], GREEN)
                    d.line([x0 + 20, 350, x0 + 160, 350], fill=GREEN, width=4)
                center(d, 640, 620, "沿粗路径走廊切细条带 → 逐段求最短路径 → 拼接最终路径（旧金山例：373.82ns / 512.5pJ / 1279.8L）", FONTS["text"], WHITE)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(wavefront_demo(), "v01_wavefront.mp4")
    write_video(dds_demo(), "v02_dds.mp4")
    write_video(tscfp_demo(), "v03_tscfp.mp4")
    print("PAPER04 VIDEOS DONE")
