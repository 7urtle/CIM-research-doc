# -*- coding: utf-8 -*-
"""论文07演示视频：TCL 数沿 / 10 相时序 / 数据流"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\07_ISSCC2026_30.4_TCL_CIM\assets\videos"
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

# ============ v01 TCL 数沿 ============
def tcl_demo():
    frames = []
    bits = [1, 1, 0, 0, 1, 0, 0, 1]
    NCYC = 8
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "TCL 转移计数：边沿沿 MMU 链传播，CNT 数沿得列和", FONTS["title"], WHITE)
            # MMU 链
            level = 0
            for k in range(8):
                x0 = 90 + k * 135
                active = (k == cyc)
                col = RED if bits[k] == 1 else GRAY
                d.rounded_rectangle([x0, 150, x0 + 120, 240], radius=10,
                                     fill=(30, 26, 40, 255) if active else PANEL,
                                     outline=col, width=2 if active else 1)
                center(d, x0 + 60, 175, f"MMU{k}", FONTS["small"], col)
                center(d, x0 + 60, 200, f"P{k}7 = {bits[k]}", FONTS["small"], WHITE)
                if active:
                    center(d, x0 + 60, 225, "Path1: 取反!" if bits[k] else "Path2: 直通", FONTS["small"], ORANGE if bits[k] else GRAY)
                # 连线
                if k > 0:
                    d.line([x0 - 15, 195, x0, 195], fill=LINE, width=2)
            d.line([90, 195, 70, 195], fill=GREEN, width=3)
            center(d, 60, 185, "VDD", FONTS["small"], GREEN)
            # CNT
            d.rounded_rectangle([1180, 150, 1250, 240], radius=10, fill=PANEL, outline=ORANGE, width=2)
            center(d, 1215, 175, "CNT", FONTS["small"], ORANGE)
            # 电平/计数
            cnt = sum(bits[:cyc + 1])
            d.text((90, 270), f"已遇到 {cyc+1} 个 MMU · 其中 1 的个数 = {cnt}", font=FONTS["text"], fill=WHITE)
            # 电平线
            level = 1
            segs = []
            for k in range(cyc + 1):
                if bits[k] == 1:
                    level = 1 - level
                    segs.append((k, level))
            # 画电平轨迹
            for k in range(cyc):
                y = 320 if (sum(bits[:k+1]) % 2 == 0) else 350
                pass
            # 简化：直接画当前电平
            d.text((90, 310), f"边沿传播后当前电平 = {'高' if (sum(bits[:cyc+1]) % 2 == 0) else '低'}（每次遇到 1 取反）", font=FONTS["text"], fill=GREEN if bits[cyc] else GRAY)
            center(d, 640, 360, "例：{1,1,0,0,1,0,0,1} → 4 个跳变沿 → CNT = 4 = 列和", FONTS["text"], ORANGE)
            center(d, 640, 420, "0 的 MMU 直通不翻转（稀疏自适应）→ 省动态功耗", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v02 10 相时序 ============
def phases_demo():
    frames = []
    NCYC = 12
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "10 相发生器：一个周期内相位依次点亮", FONTS["title"], WHITE)
            cur = cyc % 10
            d.text((80, 110), f"当前相位：Ph{cur}", font=FONTS["text"], fill=ORANGE)
            # 10 个相位块
            for k in range(10):
                x0 = 80 + k * 115
                active = k == cur
                col = RED if k < 8 else (GREEN if k == 8 else BLUE)
                d.rounded_rectangle([x0, 150, x0 + 100, 230], radius=8,
                                     fill=(44, 34, 26, 255) if active else PANEL,
                                     outline=col if active else LINE, width=2 if active else 1)
                center(d, x0 + 50, 175, f"Ph{k}", FONTS["small"], col if active else GRAY)
                role = "MMU" if k < 8 else ("合并加法器" if k == 8 else "块内加法树")
                center(d, x0 + 50, 205, role, FONTS["small"], WHITE)
            # 说明
            if cur < 8:
                center(d, 640, 280, f"Ph{cur}：使能第 {cur} 个 MMU 列，边沿向前传播一格", FONTS["text"], RED)
            elif cur == 8:
                center(d, 640, 280, "Ph8：打开合并加法器（之前输入强制接地，无毛刺）", FONTS["text"], GREEN)
            else:
                center(d, 640, 280, "Ph9：打开块内加法树，生成 16b 乘积", FONTS["text"], BLUE)
            # 波形示意
            for k in range(10):
                x0 = 80 + k * 115
                on = k <= cur
                d.rectangle([x0 + 10, 330, x0 + 90, 338], fill=ORANGE if on else (40, 50, 66, 255))
            center(d, 640, 380, "Ph0~7 串行做乘法（TCL 逐位传播）· Ph8/Ph9 才开加法 → 加法器不空转 → 能效 +42%", FONTS["text"], WHITE)
            frames.append(im)
    return frames

# ============ v03 数据流 ============
def datapath_demo():
    frames = []
    NCYC = 24
    for cyc in range(NCYC):
        snn = False
        bf16 = (cyc % 2) == 1
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            mode = "BF16 模式" if bf16 else "INT8 模式"
            col = PURPLE if bf16 else BLUE
            center(d, W//2, 56, "数据流：" + mode, FONTS["title"], col)
            # 输入
            d.rounded_rectangle([80, 130, 320, 260], radius=10, fill=PANEL, outline=col, width=2)
            center(d, 200, 160, "全局输入缓冲", FONTS["med"], col)
            if bf16:
                center(d, 200, 200, "指数预对齐 + 尾数", FONTS["small"], WHITE)
                center(d, 200, 225, "（BF16）", FONTS["small"], GRAY)
            else:
                center(d, 200, 200, "64 个特征 XIN(8b)", FONTS["small"], WHITE)
                center(d, 200, 225, "送 4 个 bank", FONTS["small"], GRAY)
            # 4 banks
            for k in range(4):
                x0 = 380 + k * 200
                d.rounded_rectangle([x0, 130, x0 + 180, 420], radius=10, fill=PANEL, outline=BLUE, width=2)
                center(d, x0 + 90, 160, f"Bank {k}", FONTS["small"], BLUE)
                d.rounded_rectangle([x0 + 12, 180, x0 + 168, 300], radius=8, fill=(24, 40, 60, 255), outline=GREEN, width=2)
                center(d, x0 + 90, 200, "4 CIM 块", FONTS["small"], GREEN)
                center(d, x0 + 90, 240, "16 单元/块", FONTS["small"], GRAY)
                center(d, x0 + 90, 270, "TCL 8b×8b", FONTS["small"], GREEN)
                d.rounded_rectangle([x0 + 12, 320, x0 + 168, 390], radius=8, fill=(40, 34, 26, 255), outline=ORANGE, width=2)
                center(d, x0 + 90, 340, "加法树", FONTS["small"], ORANGE)
                center(d, x0 + 90, 365, "→ 22b MACV", FONTS["small"], ORANGE)
                # 数据脉冲
                if 0.2 < t < 0.9:
                    p = (t - 0.2) / 0.7
                    y = 130 + p * 300
                    d.ellipse([x0 + 80, y - 6, x0 + 100, y + 10], fill=col)
            # 底部
            if bf16:
                center(d, 640, 480, "4 个尾数 MACV → 指数后处理 → FP32 输出（每周期 1 个）", FONTS["text"], PURPLE)
            else:
                center(d, 640, 480, "64 特征 × 64×4 预读权重 → 每周期 4 个 22b MACV", FONTS["text"], BLUE)
            center(d, 640, 530, "位并行：1 周期完成 8b×8b → 无需串并转换", FONTS["small"], GRAY)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(tcl_demo(), "v01_tcl.mp4")
    write_video(phases_demo(), "v02_phases.mp4")
    write_video(datapath_demo(), "v03_datapath.mp4")
    print("PAPER07 VIDEOS DONE")
