# -*- coding: utf-8 -*-
"""论文11演示视频：两周期乘法 / Winograd / MDPS"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\11_JSSC2025_TwoCycle_Winograd_CIM\assets\videos"
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

# ============ v01 两周期乘法 ============
def twocycle_demo():
    frames = []
    NCYC = 24
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "Radix16 两周期乘法：5 bit/周期，INT8 只需 2 周期", FONTS["title"], WHITE)
            # 激活位（8b）
            bits = [1, 0, 1, 1, 0, 1, 0, 1]  # 8b 激活示例
            for k in range(8):
                x0 = 180 + k * 80
                active = (k < 5 and cyc % 2 == 0) or (k >= 3 and cyc % 2 == 1)
                d.rounded_rectangle([x0, 120, x0 + 70, 180], radius=8,
                                     fill=(26, 44, 70, 255) if active else (20, 28, 40, 255),
                                     outline=BLUE if active else LINE, width=2 if active else 1)
                center(d, x0 + 35, 150, str(bits[k]), FONTS["med"], WHITE)
            # 分组标注
            if cyc % 2 == 0:
                center(d, 480, 230, "周期 0：处理 bit4~bit0（5 bit，Radix16 码）", FONTS["text"], BLUE)
                center(d, 480, 280, "编码器 → NEG/EIGHT[3:0]/ZERO → 移位器/LUT → P[10:0]", FONTS["small"], GRAY)
            else:
                center(d, 480, 230, "周期 1：处理 bit7~bit3（重叠 2 bit）", FONTS["text"], BLUE)
                center(d, 480, 280, "两周期部分积 → 补码加法器 → 18b MAC 结果", FONTS["small"], GRAY)
            center(d, 640, 340, "对比：位串行 8 周期 · Radix4 4 周期 · 本文 2 周期", FONTS["text"], ORANGE)
            center(d, 640, 400, "LUT 处理 {±3W,±5W,±6W,±7W} 部分积 → 动态功耗 −21.7%", FONTS["small"], GREEN)
            center(d, 640, 450, "完整 MAC 功耗比现有方案低 2.44×（即使每周期功耗更高）", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v02 Winograd ============
def winograd_demo():
    frames = []
    NCYC = 18
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "Winograd 域卷积：空间域 → 变换 → 逐元素乘加 → 逆变换", FONTS["title"], WHITE)
            stages = [
                ("空间域 CONV", "d × g（9 次乘法/输出块）", RED),
                ("BᵀdB + GgGᵀ 变换", "加/减/移位（便宜）", BLUE),
                ("逐元素乘加 EWMM", "F4：乘法 ÷4", GREEN),
                ("Aᵀ()A 逆变换", "还原空间域输出", ORANGE),
            ]
            for k, (name, sub, col) in enumerate(stages):
                x0 = 60 + k * 300
                active = k <= int(t * 4) % 4
                d.rounded_rectangle([x0, 160, x0 + 280, 320], radius=12,
                                     fill=(26, 44, 70, 255) if active else PANEL,
                                     outline=col if active else LINE, width=2 if active else 1)
                center(d, x0 + 140, 200, name, FONTS["med"], col if active else GRAY)
                center(d, x0 + 140, 250, sub[:16], FONTS["small"], WHITE)
                center(d, x0 + 140, 280, sub[16:] if len(sub) > 16 else "", FONTS["small"], GRAY)
                if k < 3:
                    d.polygon([(x0 + 280, 240), (x0 + 296, 232), (x0 + 296, 248)], fill=LINE)
            center(d, 640, 380, "变换开销远小于乘法开销 → 净加速（F4 = 3.32× 理论）", FONTS["text"], WHITE)
            center(d, 640, 440, "本文混合 F2+F4：按层选择 → ResNet34 2.59× 加速、精度仅 −0.6%", FONTS["text"], GREEN)
            center(d, 640, 500, "核分解（>3×3）+ 激活分段（stride=2）→ 各种卷积配置都支持", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v03 MDPS ============
def mdps_demo():
    frames = []
    NCYC = 24
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "MDPS 双端稀疏：激活压缩 + 权重水平压缩", FONTS["title"], WHITE)
            # 激活压缩
            d.rounded_rectangle([60, 130, 600, 400], radius=10, fill=PANEL, outline=BLUE, width=2)
            center(d, 330, 160, "激活侧：bit-mask + 连续 4 零跳过", FONTS["med"], BLUE)
            acts = [5, 0, 0, 0, 0, 3, 0, 0, 0, 0, 7, 1]
            k = cyc % 4
            for idx, a in enumerate(acts):
                x0 = 90 + idx * 42
                skip = a == 0 and idx % 4 != 0  # 连续 4 个中的后 3 个
                d.rounded_rectangle([x0, 200, x0 + 36, 250], radius=6,
                                     fill=(40, 34, 26, 255) if skip else (24, 44, 70, 255),
                                     outline=RED if skip else BLUE, width=2)
                center(d, x0 + 18, 225, str(a), FONTS["small"], WHITE)
            center(d, 330, 290, "连续 4 个稀疏 → 整组跳过（对应 4×32 宏输入规模）", FONTS["small"], GRAY)
            center(d, 330, 320, "→ 激活输入周期减少", FONTS["text"], BLUE)
            # 权重压缩
            d.rounded_rectangle([660, 130, 1220, 400], radius=10, fill=PANEL, outline=PURPLE, width=2)
            center(d, 940, 160, "权重侧：水平压缩（只改列位置）", FONTS["med"], PURPLE)
            ws = [3, 0, 5, 0, 7, 0, 2, 0]
            for idx, wv in enumerate(ws):
                x0 = 690 + idx * 62
                valid = wv != 0
                d.rounded_rectangle([x0, 200, x0 + 54, 260], radius=6,
                                     fill=(30, 40, 60, 255) if valid else (34, 26, 26, 255),
                                     outline=PURPLE if valid else RED, width=2)
                center(d, x0 + 27, 230, str(wv), FONTS["small"], WHITE)
            # 压缩后
            d.rounded_rectangle([690, 290, 1180, 350], radius=8, fill=(26, 50, 40, 255), outline=GREEN, width=2)
            center(d, 935, 320, "压缩后：[3,5,7,2] 左移填满 → PPRS 按索引移回", FONTS["small"], GREEN)
            center(d, 940, 380, "稀疏权重不占宏 → 利用率↑", FONTS["text"], PURPLE)
            center(d, 640, 470, "OMB 把有效结果写回正确位置 → 完整 tile 输出", FONTS["text"], WHITE)
            center(d, 640, 530, "50% 激活 + 50% 权重 → 能效 3.11×（ResNet34）", FONTS["text"], ORANGE)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(twocycle_demo(), "v01_twocycle.mp4")
    write_video(winograd_demo(), "v02_winograd.mp4")
    write_video(mdps_demo(), "v03_mdps.mp4")
    print("PAPER11 VIDEOS DONE")
