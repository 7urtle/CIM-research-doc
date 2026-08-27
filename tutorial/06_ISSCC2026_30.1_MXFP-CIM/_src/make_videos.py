# -*- coding: utf-8 -*-
"""论文06演示视频：SDBS 滑动 / MXFP 映射 / 数据流"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\06_ISSCC2026_30.1_MXFP-CIM\assets\videos"
os.makedirs(OUT, exist_ok=True)
FONTS = {
    "title": ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 38),
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

# ============ v01 SDBS 滑动 ============
def sdbs_demo():
    frames = []
    NCYC = 10
    mw = "101101"   # 权重尾数
    mn = "101001"   # 输入尾数
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "SDBS 串行双位滑动：MIN 每周期滑 2b，垂直截断", FONTS["title"], WHITE)
            # MW 固定
            d.text((80, 130), "权重 MW（固定）:", font=FONTS["text"], fill=GREEN)
            for k, ch in enumerate(mw):
                d.rounded_rectangle([330 + k*44, 118, 330 + k*44 + 36, 152], radius=5, fill=(24, 60, 44, 255), outline=GREEN, width=2)
                center(d, 330 + k*44 + 18, 135, ch, FONTS["mono"], WHITE)
            # MIN 滑动
            d.text((80, 200), "输入 MIN（滑动）:", font=FONTS["text"], fill=BLUE)
            shift = min(cyc, 6)
            for k in range(8):
                x0 = 330 + k*44
                has = k >= shift and (k - shift) < 6
                ch = mn[k - shift] if has else ""
                d.rounded_rectangle([x0, 188, x0 + 36, 222], radius=5,
                                     fill=(24, 44, 70, 255) if has else (30, 40, 56, 255),
                                     outline=BLUE if has else LINE, width=2)
                if has:
                    center(d, x0 + 18, 205, ch, FONTS["mono"], WHITE)
            center(d, 640, 260, f"周期 {cyc}：MIN 已右滑 {shift*2} bit（每周期 2b）", FONTS["text"], ORANGE)
            # 乘积示意
            d.rounded_rectangle([80, 300, 1180, 380], radius=10, fill=PANEL, outline=PURPLE, width=2)
            center(d, 640, 325, "每次滑动产生“垂直截断”的部分积（整列对齐，无无效位）", FONTS["text"], WHITE)
            center(d, 640, 360, "ESUM 大的输入先滑 → 高位优先对齐；PBW = 周期数（2~14 可调）", FONTS["small"], PURPLE)
            center(d, 640, 420, "对比输入对齐方案：非垂直截断产生斜线无效位 → 白算", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v02 MXFP 映射 ============
def mapping_demo():
    frames = []
    NCYC = 20
    for cyc in range(NCYC):
        mxfp8 = (cyc % 2) == 0
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            mode = "MXFP8（E4M3）· 9 个数/子阵列" if mxfp8 else "MXFP6（E2M3）· 12 个数/子阵列"
            col = BLUE if mxfp8 else PURPLE
            center(d, W//2, 56, "HDM 无害数据映射：" + mode, FONTS["title"], col)
            # 子阵列
            d.rounded_rectangle([120, 130, 1160, 420], radius=10, fill=PANEL, outline=col, width=2)
            center(d, 640, 158, "18 行 × 4 列子阵列（每次 72b 容量）", FONTS["text"], WHITE)
            for r in range(8):
                even = (r % 2 == 0)
                for c in range(12):
                    x0 = 150 + c * 82
                    y0 = 180 + r * 28
                    if mxfp8:
                        filled = (r * 12 + c) % 13 < 9
                    else:
                        filled = True
                    col2 = (col if even else ORANGE) if filled else (40, 48, 64, 255)
                    d.rounded_rectangle([x0, y0, x0 + 74, y0 + 22], radius=4, fill=(26, 44, 66, 255), outline=col2, width=2)
                # 标签
                if even:
                    center(d, 620, 470 + (r % 2) * 24, "偶数行：符号 + 尾数" if even else "奇数行：指数", FONTS["small"], col)
            if mxfp8:
                center(d, 640, 500, "9 个数 × 8b = 72b → 子阵列满用", FONTS["text"], GREEN)
            else:
                center(d, 640, 500, "12 个数 × 6b = 72b → 子阵列满用（奇数行并排 2 个指数）", FONTS["text"], GREEN)
            center(d, 640, 560, "→ MXFP6/8 模式切换不浪费任何存储位（“无害”）", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v03 数据流 ============
def datapath_demo():
    frames = []
    NCYC = 20
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "MXFP-CIM 数据流：从位宽分配到输出", FONTS["title"], WHITE)
            stages = [
                ("① 全局解码+位宽分配", "CGA/FGA 决定本层/本组 PBW", ORANGE),
                ("② 指数相加 ESUM", "MF 找最大 → SDT 生成滑动控制", BLUE),
                ("③ DBSU 双位滑动", "每周期滑 2b（时钟门控+C2MOS）", GREEN),
                ("④ 压缩+加法树", "6 全加器压缩 → 通道级加法树", PURPLE),
                ("⑤ A&N 累加归一化", "输出 FP 结果", RED),
            ]
            for k, (name, sub, col) in enumerate(stages):
                x0 = 60 + k * 235
                active = k <= int(t * 5) % 6
                d.rounded_rectangle([x0, 150, x0 + 220, 300], radius=12,
                                     fill=(26, 44, 70, 255) if active else PANEL,
                                     outline=col if active else LINE, width=2 if active else 1)
                center(d, x0 + 110, 185, name, FONTS["med"], col if active else GRAY)
                center(d, x0 + 110, 230, sub[:14], FONTS["small"], WHITE)
                center(d, x0 + 110, 260, sub[14:] if len(sub) > 14 else "", FONTS["small"], GRAY)
            # 进度
            p = (t * 5) % 5
            center(d, 640, 380, f"正在执行：{stages[min(int(p),4)][0]}", FONTS["text"], ORANGE)
            center(d, 640, 440, "PBW 随周期数伸缩（2~14 周期）：位宽分配器按层/组实时调节精度", FONTS["small"], GRAY)
            center(d, 640, 490, "24 个 bank 并行：每 bank 本地 EPU + 尾数 MAC", FONTS["small"], GRAY)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(sdbs_demo(), "v01_sdbs.mp4")
    write_video(mapping_demo(), "v02_mapping.mp4")
    write_video(datapath_demo(), "v03_datapath.mp4")
    print("PAPER06 VIDEOS DONE")
