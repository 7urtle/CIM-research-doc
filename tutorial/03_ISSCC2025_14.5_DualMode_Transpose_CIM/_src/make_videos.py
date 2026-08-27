# -*- coding: utf-8 -*-
"""论文03演示视频：转置读取 / SFME / DMBP 双模式"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\03_ISSCC2025_14.5_DualMode_Transpose_CIM\assets\videos"
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

# ============ v01 转置读取 ============
def transpose_demo():
    frames = []
    NCYC = 20
    for cyc in range(NCYC):
        ff = (cyc % 2) == 0
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            mode = "FF：读行（A × W）" if ff else "BP：读对角（G × Wᵀ）"
            col = BLUE if ff else RED
            center(d, W//2, 56, "CWM-SRAM 转置读取：" + mode, FONTS["title"], col)
            # 6x6 矩阵
            d.rounded_rectangle([240, 140, 700, 600], radius=10, fill=PANEL, outline=GREEN, width=2)
            for r in range(6):
                for c in range(6):
                    x0 = 260 + c * 72
                    y0 = 160 + r * 72
                    if ff:
                        active = (cyc % 6) == r
                        col2 = GREEN if active else LINE
                    else:
                        active = (cyc % 6) == c
                        col2 = RED if active else LINE
                    d.rectangle([x0, y0, x0 + 66, y0 + 66], fill=(24, 40, 60, 255) if active else (18, 28, 42, 255), outline=col2, width=3 if active else 1)
            # 说明
            if ff:
                center(d, 640, 640, f"读第 {cyc % 6} 行 → 权重向量（循环映射后与激活对齐）", FONTS["text"], BLUE)
            else:
                center(d, 640, 640, f"读第 {cyc % 6} 条对角 → 权重转置向量（G × Wᵀ）", FONTS["text"], RED)
            center(d, 640, 690, "同一 256b 读口、同一套 MAC → FF/BP 电路完全复用", FONTS["small"], GREEN)
            frames.append(im)
    return frames

# ============ v02 SFME ============
def sfme_demo():
    frames = []
    NCYC = 12
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "SFME：浮点权重 → 有符号定点尾数（FP 走 INT 通路）", FONTS["title"], WHITE)
            # FP 权重
            d.rounded_rectangle([80, 130, 600, 400], radius=10, fill=PANEL, outline=BLUE, width=2)
            center(d, 340, 160, "FP 权重：−1ˢ·2^(E−Bias)·(1.M)", FONTS["text"], BLUE)
            d.rounded_rectangle([110, 190, 250, 260], radius=8, fill=(24, 44, 70, 255), outline=BLUE, width=2)
            center(d, 180, 225, "符号", FONTS["text"], WHITE)
            d.rounded_rectangle([270, 190, 410, 260], radius=8, fill=(24, 44, 70, 255), outline=BLUE, width=2)
            center(d, 340, 225, "指数 E", FONTS["text"], WHITE)
            d.rounded_rectangle([430, 190, 570, 260], radius=8, fill=(24, 44, 70, 255), outline=BLUE, width=2)
            center(d, 500, 225, "尾数 1.M", FONTS["text"], WHITE)
            center(d, 340, 320, "预对齐：共享指数 Es = Emax − Bias", FONTS["text"], ORANGE)
            center(d, 340, 360, "隐藏位+尾数归一化 → Mn", FONTS["text"], ORANGE)
            # 转换结果
            d.rounded_rectangle([660, 130, 1220, 400], radius=10, fill=PANEL, outline=GREEN, width=2)
            center(d, 940, 160, "SFME：Ma = −1ˢ · 0.Mn", FONTS["text"], GREEN)
            center(d, 940, 210, "有符号定点补码尾数", FONTS["text"], WHITE)
            d.rounded_rectangle([700, 240, 1180, 310], radius=8, fill=(26, 50, 40, 255), outline=GREEN, width=2)
            center(d, 940, 260, "4b → 复用 INT4 通路", FONTS["text"], WHITE)
            center(d, 940, 285, "8b → 复用 INT8 通路", FONTS["text"], WHITE)
            center(d, 940, 350, "四模式 4b 乘法器覆盖全部 8b 2C 部分积组合", FONTS["small"], GRAY)
            center(d, 640, 470, "→ FP 的 MAC 走整数数据通路 → 硬件几乎免费；FP8/BF16/INT4/INT8 一个宏全支持", FONTS["text"], GREEN)
            frames.append(im)
    return frames

# ============ v03 DMBP 双模式 ============
def dmbp_demo():
    frames = []
    NCYC = 16
    for cyc in range(NCYC):
        approx = (cyc % 2) == 1
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            mode = "精确模式" if not approx else "近似模式（丢 6 部分和 + 低位 OR）"
            col = BLUE if not approx else ORANGE
            center(d, W//2, 56, "DMBP-MAC 双模式：" + mode, FONTS["title"], col)
            # 部分积阵列
            d.rounded_rectangle([120, 140, 1160, 420], radius=10, fill=PANEL, outline=col, width=2)
            for r in range(6):
                for c in range(12):
                    x0 = 150 + c * 80
                    y0 = 170 + r * 40
                    dropped = approx and c >= 9
                    d.rectangle([x0, y0, x0 + 70, y0 + 32], fill=(36, 30, 24, 255) if dropped else (26, 44, 70, 255),
                                outline=RED if dropped else col, width=2 if dropped else 1)
            if approx:
                center(d, 640, 470, "右侧 6 个部分和丢弃（BAM）· 低位加法换 OR（LOA）· 偏置加法器补偿", FONTS["text"], ORANGE)
                center(d, 640, 520, "速度 +12% · 功耗 −31% · NMED 5.3%（高斯误差、均值≈0）", FONTS["text"], GREEN)
            else:
                center(d, 640, 470, "全部部分积 + 完整加法树 → 精度最高", FONTS["text"], BLUE)
                center(d, 640, 520, "适合训练/精度敏感场景", FONTS["text"], WHITE)
            center(d, 640, 580, "应用按需切换：训练用精确、大规模推理用近似", FONTS["small"], GRAY)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(transpose_demo(), "v01_transpose.mp4")
    write_video(sfme_demo(), "v02_sfme.mp4")
    write_video(dmbp_demo(), "v03_dmbp.mp4")
    print("PAPER03 VIDEOS DONE")
