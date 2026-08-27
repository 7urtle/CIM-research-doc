# -*- coding: utf-8 -*-
"""论文05演示视频：事件流 / e-OTBP / 格雷码更新"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\05_ISSCC2026_18.4_SpikeRAM\assets\videos"
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

# ============ v01 事件流 ============
def event_flow_demo():
    frames = []
    NCYC = 40
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "事件驱动流水：EVS → sCNN → sFC-OCL（只有事件才流动）", FONTS["title"], WHITE)
            # EVS
            d.rounded_rectangle([80, 140, 300, 320], radius=10, fill=PANEL, outline=BLUE, width=2)
            center(d, 190, 170, "片上 EVS", FONTS["med"], BLUE)
            # 事件点
            for k in range(12):
                if (cyc + k) % 3 != 0:
                    x = 100 + ((k * 37) % 180)
                    y = 200 + ((k * 53) % 100)
                    d.ellipse([x, y, x + 8, y + 8], fill=ORANGE)
            center(d, 190, 300, "异步事件（x,y,t,p）", FONTS["small"], GRAY)
            # sCNN
            d.rounded_rectangle([360, 140, 620, 320], radius=10, fill=PANEL, outline=GREEN, width=2)
            center(d, 490, 170, "EVS-sCNN 核（NMC）", FONTS["med"], GREEN)
            center(d, 490, 210, "事件驱动卷积", FONTS["text"], WHITE)
            center(d, 490, 240, "LIF 神经元 → 特征事件", FONTS["small"], GRAY)
            # sFC
            d.rounded_rectangle([680, 140, 1180, 320], radius=10, fill=PANEL, outline=PURPLE, width=2)
            center(d, 930, 170, "sFC-OCL 核（CIM）", FONTS["med"], PURPLE)
            center(d, 930, 210, "事件滤波器 + 移位相加", FONTS["text"], WHITE)
            center(d, 930, 240, "推理 → e-OTBP 在线学习", FONTS["small"], GRAY)
            # 流动脉冲
            if 0.2 < t < 0.85:
                p = (t - 0.2) / 0.65
                for lane in range(3):
                    x = 300 + p * 380 + lane * 0
                    y = 200 + lane * 40
                    d.ellipse([x, y, x + 10, y + 10], fill=col_for(lane))
            center(d, 640, 380, "全程无帧转换、无时钟树（异步双轨握手）→ 无事件时电路静止", FONTS["text"], WHITE)
            center(d, 640, 440, "NoC 调度事件路由 · 推理状态复用于学习", FONTS["small"], GRAY)
            frames.append(im)
    return frames

def col_for(lane):
    return [GREEN, BLUE, PURPLE][lane]

# ============ v02 e-OTBP ============
def eotbp_demo():
    frames = []
    NCYC = 8
    # 对比 BPTT 与 e-OTBP
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "在线学习：BPTT（展开）vs e-OTBP（单时间步）", FONTS["title"], WHITE)
            # 左 BPTT
            d.rounded_rectangle([60, 130, 600, 500], radius=10, fill=PANEL, outline=RED, width=2)
            center(d, 330, 160, "BPTT：按时间展开", FONTS["med"], RED)
            for k in range(8):
                x0 = 80 + k * 62
                d.rounded_rectangle([x0, 200, x0 + 52, 260], radius=6, fill=(44, 30, 30, 255), outline=RED, width=2)
                center(d, x0 + 26, 230, f"TW{k}", FONTS["small"], RED)
            center(d, 330, 300, "要保存/展开整个时间窗口的历史", FONTS["text"], WHITE)
            center(d, 330, 340, "内存与功耗随 TW 深度线性增长", FONTS["small"], RED)
            center(d, 330, 400, "32 TW → 内存需求 100%", FONTS["text"], RED)
            # 右 e-OTBP
            d.rounded_rectangle([660, 130, 1220, 500], radius=10, fill=PANEL, outline=GREEN, width=2)
            center(d, 940, 160, "e-OTBP：单时间步 + 资格迹", FONTS["med"], GREEN)
            d.rounded_rectangle([700, 200, 1160, 260], radius=6, fill=(30, 60, 44, 255), outline=GREEN, width=2)
            center(d, 930, 230, "只用当前时间步 + ET（资格迹）", FONTS["text"], WHITE)
            center(d, 930, 300, "ET 压缩历史贡献 → 不展开 TW", FONTS["text"], WHITE)
            center(d, 930, 340, "推理状态（Vmem/脉冲）直接复用", FONTS["small"], GRAY)
            center(d, 930, 400, "32 TW → 内存需求 26.9%（−73.1%）", FONTS["text"], GREEN)
            center(d, 640, 560, "Surr 函数=2 个比较器 · ET=循环累加器 · 转置权重=水平加法树 → 硬件开销极小（vs BPTT 为 4.3%/3.1%）", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v03 格雷码更新 ============
def graycode_demo():
    frames = []
    NCYC = 14
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "三值梯度 + 格雷码：权重每次更新只翻 1 位", FONTS["title"], WHITE)
            # 二进制对比
            d.text((80, 130), "二进制权重 7 → 8（+1）：", font=FONTS["text"], fill=RED)
            for k, ch in enumerate("0111"):
                d.rounded_rectangle([420 + k*44, 118, 420 + k*44 + 36, 152], radius=5, fill=(44, 30, 30, 255), outline=RED, width=2)
                center(d, 420 + k*44 + 18, 135, ch, FONTS["mono"], WHITE)
            for k, ch in enumerate("1000"):
                x0 = 420 + k*44
                d.rounded_rectangle([x0, 168, x0 + 36, 202], radius=5, fill=(44, 30, 30, 255), outline=RED, width=2)
                center(d, x0 + 18, 185, ch, FONTS["mono"], WHITE)
            center(d, 660, 190, "4 位全翻！", FONTS["text"], RED)
            # 格雷码
            d.text((80, 260), "格雷码 5 → 6（+1）：", font=FONTS["text"], fill=GREEN)
            for k, ch in enumerate("0111"):
                d.rounded_rectangle([420 + k*44, 248, 420 + k*44 + 36, 282], radius=5, fill=(30, 60, 44, 255), outline=GREEN, width=2)
                center(d, 420 + k*44 + 18, 265, ch, FONTS["mono"], WHITE)
            for k, ch in enumerate("0101"):
                x0 = 420 + k*44
                d.rounded_rectangle([x0, 298, x0 + 36, 332], radius=5, fill=(30, 60, 44, 255), outline=GREEN, width=2)
                center(d, x0 + 18, 315, ch, FONTS["mono"], WHITE)
            center(d, 660, 320, "只翻 1 位！", FONTS["text"], GREEN)
            center(d, 640, 400, "三值梯度 {−1,0,+1}：0 不写、±1 只翻 1 位 → 每个权重每批最多写 1b", FONTS["text"], WHITE)
            center(d, 640, 460, "实测：编程次数 −89.1%（NMNIST）· MRAM 寿命 +13.9×", FONTS["text"], ORANGE)
            center(d, 640, 520, "格雷码解码器 = 并行 XOR（与 SA 集成，推理时二值读出）", FONTS["small"], GRAY)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(event_flow_demo(), "v01_event_flow.mp4")
    write_video(eotbp_demo(), "v02_eotbp.mp4")
    write_video(graycode_demo(), "v03_graycode.mp4")
    print("PAPER05 VIDEOS DONE")
