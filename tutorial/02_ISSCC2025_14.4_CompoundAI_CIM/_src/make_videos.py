# -*- coding: utf-8 -*-
"""论文02演示视频：后乘积对齐 / AIM 累加 / 稀疏加速"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\02_ISSCC2025_14.4_CompoundAI_CIM\assets\videos"
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

# ============ v01 后乘积对齐 ============
def post_align_demo():
    frames = []
    NCYC = 24
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "后乘积对齐：尾数并行乘、指数累加、乘积后才对齐", FONTS["title"], WHITE)
            # 左：尾数乘法
            d.rounded_rectangle([80, 130, 560, 400], radius=10, fill=PANEL, outline=BLUE, width=2)
            center(d, 320, 160, "尾数并行乘法（ME-CIM）", FONTS["med"], BLUE)
            d.rounded_rectangle([110, 190, 250, 260], radius=8, fill=(24, 44, 70, 255), outline=BLUE, width=2)
            center(d, 180, 225, "输入尾数", FONTS["text"], WHITE)
            d.rounded_rectangle([390, 190, 530, 260], radius=8, fill=(24, 44, 70, 255), outline=BLUE, width=2)
            center(d, 460, 225, "权重尾数", FONTS["text"], WHITE)
            d.rounded_rectangle([110, 300, 530, 370], radius=8, fill=(26, 50, 40, 255), outline=GREEN, width=2)
            center(d, 320, 335, "未对齐乘积（宽位宽，无损）", FONTS["text"], GREEN)
            # 右：指数与后对齐
            d.rounded_rectangle([620, 130, 1200, 400], radius=10, fill=PANEL, outline=PURPLE, width=2)
            center(d, 910, 160, "指数累加 + 后乘积对齐", FONTS["med"], PURPLE)
            d.rounded_rectangle([650, 200, 1170, 270], radius=8, fill=(40, 34, 26, 255), outline=ORANGE, width=2)
            center(d, 910, 220, "指数和 → 最大指数 → 对齐移位量", FONTS["text"], WHITE)
            d.rounded_rectangle([650, 300, 1170, 370], radius=8, fill=(30, 60, 44, 255), outline=GREEN, width=2)
            center(d, 910, 320, "乘积按指数差移位 → 累加（一次性误差）", FONTS["text"], GREEN)
            center(d, 910, 350, "误差只发生在此处，不注入每个乘积", FONTS["small"], GRAY)
            center(d, 640, 460, "对比：预对齐把移位误差注入每个乘积 → 误差放大；后对齐只在累加时移一次 → FP16 误差 < 2⁻³⁰", FONTS["text"], ORANGE)
            center(d, 640, 520, "SER = 60.1 dB（3.14× 于传统 FP-CIM）· 精度损失平均降低 11.07×", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v02 AIM 累加 ============
def aim_demo():
    frames = []
    NCYC = 20
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "AIM 累加存内：部分和就地累加，不搬数据", FONTS["title"], WHITE)
            # 单元链
            for k in range(6):
                x0 = 90 + k * 175
                active = k == cyc % 6
                d.rounded_rectangle([x0, 160, x0 + 155, 300], radius=10,
                                     fill=(26, 44, 70, 255) if active else PANEL,
                                     outline=GREEN if active else LINE, width=2 if active else 1)
                center(d, x0 + 78, 190, f"存储值 {k}", FONTS["small"], WHITE)
                center(d, x0 + 78, 230, "部分和 →", FONTS["small"], ORANGE if active else GRAY)
                center(d, x0 + 78, 260, "AND/NOR + 部分全加", FONTS["small"], GREEN if active else GRAY)
                center(d, x0 + 78, 285, "写回（就地）", FONTS["small"], GREEN if active else GRAY)
            center(d, 640, 340, "部分和/残差从 CIM 送到 AIM，与存储值就地相加并写回 → 数据不出内存", FONTS["text"], WHITE)
            center(d, 640, 390, "XOR 区分 INT/FP；FP 多一步指数比较对齐", FONTS["small"], GRAY)
            center(d, 640, 440, "vs 全数字：INT32 省 38.3%、FP32 省 15.4% 功耗；系统级 INT −22.1% / FP −9.7%", FONTS["text"], GREEN)
            frames.append(im)
    return frames

# ============ v03 稀疏加速 ============
def sparsity_demo():
    frames = []
    NCYC = 24
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "NIM + 动态启动器：静态 2:4 与动态 Booth 池", FONTS["title"], WHITE)
            # 左：2:4 静态
            d.rounded_rectangle([60, 130, 600, 460], radius=10, fill=PANEL, outline=BLUE, width=2)
            center(d, 330, 160, "静态 2:4（NIM）", FONTS["med"], BLUE)
            for k in range(4):
                x0 = 90 + k * 120
                val = [1, 0, 1, 0][k]
                d.rounded_rectangle([x0, 190, x0 + 100, 250], radius=8,
                                     fill=(26, 44, 70, 255) if val else (24, 32, 44, 255),
                                     outline=BLUE if val else LINE, width=2)
                center(d, x0 + 50, 220, f"W{k}={val}", FONTS["small"], WHITE)
            center(d, 330, 300, "4 选 2（2:4 剪枝/掩码）", FONTS["text"], WHITE)
            center(d, 330, 340, "排除 2 条不可能路径 → 网络简化", FONTS["small"], GRAY)
            center(d, 330, 390, "静态加速 ~2×", FONTS["text"], BLUE)
            # 右：动态
            d.rounded_rectangle([660, 130, 1220, 460], radius=10, fill=PANEL, outline=PURPLE, width=2)
            center(d, 940, 160, "动态 Booth 池（启动器）", FONTS["med"], PURPLE)
            terms = [1, 0, 1, 0, 0, 1, 0, 1]
            for k in range(8):
                x0 = 690 + k * 62
                val = terms[k]
                d.rounded_rectangle([x0, 190, x0 + 52, 250], radius=8,
                                     fill=(40, 30, 40, 255) if val else (24, 32, 44, 255),
                                     outline=ORANGE if val else LINE, width=2)
                center(d, x0 + 26, 220, str(val), FONTS["small"], WHITE)
            center(d, 940, 300, "4 字段：ID/sign/valid/SF", FONTS["text"], WHITE)
            center(d, 940, 340, "BPLS 把非零项重排到空闲道", FONTS["small"], GRAY)
            center(d, 940, 380, "前导 1 检测器逐个找有效项 → 只算有效的", FONTS["small"], GRAY)
            center(d, 940, 420, "动态加速 ~2.65×", FONTS["text"], PURPLE)
            center(d, 640, 520, "合计 5.30×（≈ 理论上限 92.6%）· 配合 10T 无预充电单元：读 0 不耗电 → 峰值 51.6 TFLOPS/W", FONTS["text"], GREEN)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(post_align_demo(), "v01_post_align.mp4")
    write_video(aim_demo(), "v02_aim.mp4")
    write_video(sparsity_demo(), "v03_sparsity.mp4")
    print("PAPER02 VIDEOS DONE")
