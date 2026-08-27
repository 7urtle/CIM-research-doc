# -*- coding: utf-8 -*-
"""论文01演示视频：串行对齐 / N2CMAC 流程 / 广播数据流"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\01_ISSCC2025_14.3_B-A-N2CMAC_FP-CIM\assets\videos"
os.makedirs(OUT, exist_ok=True)
FONTS = {
    "title": ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 38),
    "big":   ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 30),
    "med":   ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 24),
    "text":  ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 21),
    "small": ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 17),
    "mono":  ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 20),
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

# ============ v01 串行对齐 ============
def align_demo():
    frames = []
    NCYC = 60
    # 三个输入的对齐差距：LC0 差0, LC1 差2, LC2 差4
    gaps = [0, 2, 4]
    names = ["LC0 (差0)", "LC1 (差2)", "LC2 (差4)"]
    colors = [GREEN, PURPLE, RED]
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "2b 串行对齐：SDT 倒计时，各 LC 按差距 存→移", FONTS["title"], WHITE)
            # SDT 行
            d.text((80, 110), "SDT（从最大值每周期 -1）", font=FONTS["text"], fill=ORANGE)
            maxv = 6
            for cy in range(8):
                v = maxv - cy
                x0 = 80 + cy * 140
                d.rounded_rectangle([x0, 140, x0 + 110, 180], radius=6, fill=(40, 34, 26, 255), outline=ORANGE, width=2)
                center(d, x0 + 55, 160, f"周期{cy}: SDT={v}", FONTS["small"], ORANGE)
                if cy == cyc % 8:
                    d.rounded_rectangle([x0, 140, x0 + 110, 180], radius=6, fill=(60, 50, 30, 255), outline=WHITE, width=3)
            # LC 行为
            for li, (gap, name, col) in enumerate(zip(gaps, names, colors)):
                y = 230 + li * 130
                d.rounded_rectangle([80, y, 1160, y + 110], radius=10, fill=PANEL, outline=LINE)
                d.text((100, y + 12), name, font=FONTS["med"], fill=col)
                # 状态条
                for cy in range(8):
                    x0 = 100 + cy * 130
                    c = cyc % 8
                    is_store = cy <= c
                    state = "存" if (cy < gap) else "移"
                    if cyc % 8 >= gap:
                        state = "移"
                    else:
                        state = "存"
                    if cy == c:
                        pass
                    d.rounded_rectangle([x0, y + 50, x0 + 100, y + 84], radius=6,
                                         fill=(30, 60, 44, 255) if state == "存" else (60, 44, 30, 255),
                                         outline=col, width=2)
                    center(d, x0 + 50, y + 67, f"周期{cy}·{state}", FONTS["small"], col)
                center(d, 640, y + 102, f"存 = 尾数进入寄存器链；移 = 每周期输出 2b（对齐后）", FONTS["small"], GRAY)
            center(d, W//2, 660, "对齐电路只需倒计时器+比较器+寄存器链 → 面积比桶形移位器省 36.23%", FONTS["text"], GREEN)
            frames.append(im)
    return frames

# ============ v02 N2CMAC 流程 ============
def n2cmac_demo():
    frames = []
    NCYC = 8
    steps = [
        ("① 层次缓冲 → GIN", "8b 并行指数 EIN + 2b 串行尾数 MIN，广播到 16 个 TS-A", BLUE),
        ("② LC 串行转换", "BF16：串行对齐；INT8/BF16：符号处理 {~LIN[m-1], LIN[m-2:0]}", PURPLE),
        ("③ DMU 乘 |MW|", "按尾数权重符号取反 LIN → 无符号乘法 → 加法树累加", GREEN),
        ("④ CA&Q 补偿累加", "多周期累加 + 预置符号补偿 → MACV（BF16A:23b）", ORANGE),
    ]
    for si in range(4):
        for i in range(FPS * 3):
            im, d = new_frame()
            t = i / FPS
            center(d, W//2, 60, "格式混合 N2CMAC 四步计算流程", FONTS["title"], WHITE)
            # 4 个步骤框（已完成的亮起）
            for k, (name, sub, col) in enumerate(steps):
                x0 = 60 + k * 300
                active = k <= si
                d.rounded_rectangle([x0, 140, x0 + 270, 260], radius=12,
                                     fill=(26, 44, 70, 255) if active else PANEL,
                                     outline=col if active else LINE, width=2 if active else 1)
                center(d, x0 + 135, 180, name, FONTS["med"], col if active else GRAY)
                # 子说明
                y = 280
                d.rounded_rectangle([x0, y, x0 + 270, y + 130], radius=10, fill=PANEL, outline=LINE)
                center(d, x0 + 135, y + 40, sub[:18], FONTS["small"], WHITE)
                center(d, x0 + 135, y + 65, sub[18:] if len(sub) > 18 else "", FONTS["small"], GRAY)
            # 高亮当前
            if si < 3:
                center(d, 640, 660, "下一步 →", FONTS["text"], ORANGE)
            else:
                center(d, 640, 660, "有符号 MAC = 无符号 MAC + 符号补偿（补偿跨多周期共享）", FONTS["text"], GREEN)
            frames.append(im)
    return frames

# ============ v03 广播数据流 ============
def bcast_demo():
    frames = []
    NCYC = 30
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "广播数据流：一份 GIN 喂 16 个 TS-A", FONTS["title"], WHITE)
            # 输入
            d.rounded_rectangle([80, 130, 300, 220], radius=10, fill=PANEL, outline=PURPLE, width=2)
            center(d, 190, 155, "层次输入缓冲", FONTS["med"], PURPLE)
            center(d, 190, 190, "GIN：EIN(8b) + MIN(2b)", FONTS["small"], WHITE)
            # 广播线
            d.line([300, 175, 340, 175], fill=PURPLE, width=3)
            for k in range(4):
                d.line([340, 175, 340 + k * 120, 175], fill=PURPLE, width=2)
                d.line([340 + k * 120, 175, 340 + k * 120, 260], fill=PURPLE, width=2)
            # 4 个 TS-A（示意 16 个）
            for k in range(4):
                x0 = 320 + k * 130
                d.rounded_rectangle([x0, 260, x0 + 110, 430], radius=10, fill=PANEL, outline=BLUE, width=2)
                center(d, x0 + 55, 285, f"TS-A {k}", FONTS["small"], BLUE)
                d.rounded_rectangle([x0 + 8, 300, x0 + 102, 350], radius=6, fill=(40, 34, 26, 255), outline=ORANGE, width=2)
                center(d, x0 + 55, 325, "ESICU", FONTS["small"], ORANGE)
                d.rounded_rectangle([x0 + 8, 360, x0 + 102, 410], radius=6, fill=(24, 44, 68, 255), outline=GREEN, width=2)
                center(d, x0 + 55, 385, "N2CMACU", FONTS["small"], GREEN)
                # 数据块脉冲
                if 0.15 < t < 0.85:
                    p = (t - 0.15) / 0.7
                    y = 175 + p * 90
                    d.ellipse([x0 + 55 - 6, y - 6, x0 + 55 + 6, y + 6], fill=ORANGE)
            # 说明
            center(d, 640, 480, "前作：每个阵列单独准备浮点输入 → 利用率低；本文：16 阵列共享一份 GIN → 利用率最大化", FONTS["small"], GRAY)
            center(d, 640, 520, "每个 TS-A 算 1 个输出通道 → 每周期 16 个通道并行", FONTS["small"], GRAY)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(align_demo(), "v01_serial_align.mp4")
    write_video(n2cmac_demo(), "v02_n2cmac.mp4")
    write_video(bcast_demo(), "v03_bcast.mp4")
    print("PAPER01 VIDEOS DONE")
