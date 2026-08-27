# -*- coding: utf-8 -*-
"""论文08演示视频：3D 堆叠组装 / GEMM 数据流 / 近存访问延迟"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\08_ISSCC2026_30.7_3D_PNM_LLM\assets\videos"
os.makedirs(OUT, exist_ok=True)

FONTS = {
    "title": ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 38),
    "big":   ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 30),
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

def panel(d, box, title=None):
    d.rounded_rectangle(box, radius=16, fill=PANEL, outline=LINE, width=2)
    if title:
        d.text((box[0]+18, box[1]+10), title, font=FONTS["med"], fill=WHITE)

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

# ============ v01 3D 堆叠组装 ============
def stack_demo():
    frames = []
    NCYC = 40
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "3D 堆叠组装：Two-DRAM-One-Logic", FONTS["title"], WHITE)
            # 三层依次出现
            layers = []
            if t > 0.05: layers.append(("DRAM_F（512Mb）", GREEN, 180))
            if t > 0.35: layers.append(("DRAM_N（512Mb）", GREEN, 300))
            if t > 0.65: layers.append(("逻辑晶圆（28nm CMOS）", BLUE, 420))
            for name, col, y in layers:
                d.rounded_rectangle([300, y, 980, y + 90], radius=12, fill=(20, 40, 62, 255), outline=col, width=3)
                center(d, 640, y + 30, name, FONTS["med"], col)
                center(d, 640, y + 62, "← HB 互连（pitch 3μm）" if y < 400 else "← 计算模块 + 3D DRAM PHY", FONTS["small"], GRAY)
            # TSV 出现
            if t > 0.5:
                d.rectangle([360, 300, 368, 420], fill=ORANGE)
                d.rectangle([900, 300, 908, 420], fill=ORANGE)
                center(d, 400, 460, "mini-TSV（pitch 5μm）穿过 DRAM_N", FONTS["small"], ORANGE)
            # 数据路径动画
            if t > 0.8:
                p = (t - 0.8) / 0.2
                y = 180 + p * 330
                d.ellipse([620, y, 636, y + 16], fill=RED)
                center(d, 640, 540, "RDL 数据流：DRAM_F → HB-TSV-HB → 逻辑层", FONTS["text"], WHITE)
            # 底部指标
            if t > 0.9:
                center(d, 640, 640, "1GB 片上 DRAM · 99.4 Mb/mm² · 2048b/BG 总线 · 12.77 GB/s/mm²", FONTS["text"], GREEN)
            frames.append(im)
    return frames

# ============ v02 GEMM 数据流 ============
def gemm_demo():
    frames = []
    NCYC = 30
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "GEMM 数据流：M、K 各切 4 份 → 16 个 ACC 并行", FONTS["title"], WHITE)
            # 矩阵
            d.rounded_rectangle([80, 140, 360, 420], radius=8, fill=(16, 28, 44, 255), outline=BLUE, width=2)
            center(d, 220, 120, "输入 I (M×N)", FONTS["text"], BLUE)
            for r in range(4):
                for c in range(4):
                    d.rectangle([96 + c*66, 156 + r*66, 96 + c*66 + 60, 156 + r*66 + 60], outline=BLUE)
            d.rounded_rectangle([420, 140, 700, 420], radius=8, fill=(16, 28, 44, 255), outline=RED, width=2)
            center(d, 560, 120, "权重 W (N×K)", FONTS["text"], RED)
            for r in range(4):
                for c in range(4):
                    d.rectangle([436 + c*66, 156 + r*66, 436 + c*66 + 60, 156 + r*66 + 60], outline=RED)
            d.rounded_rectangle([740, 140, 1180, 420], radius=8, fill=(16, 28, 44, 255), outline=GREEN, width=2)
            center(d, 960, 120, "输出 O (M×K)", FONTS["text"], GREEN)
            # 活跃块按时间移动
            k = int(t * 16) % 16
            r, c = k // 4, k % 4
            for pair, col in [((r, c), BLUE), ((c, r), RED)]:
                pass
            d.rectangle([96 + c*66, 156 + r*66, 96 + c*66 + 60, 156 + r*66 + 60], fill="rgba" if False else (30, 80, 130, 255), outline=BLUE, width=3)
            d.rectangle([436 + c*66, 156 + r*66, 436 + c*66 + 60, 156 + r*66 + 60], fill=(80, 40, 40, 255), outline=RED, width=3)
            d.rectangle([756 + c*66, 156 + r*66, 756 + c*66 + 60, 156 + r*66 + 60], fill=(40, 80, 60, 255), outline=GREEN, width=3)
            # 分配标签
            center(d, 640, 470, f"I{r}W{c} → BG{(r*2 + c//2) % 8}/ACC{(r*2 + c) % 2}（示意）", FONTS["text"], ORANGE)
            center(d, 640, 520, "权重连续存放 + DMA 读取；输入行均匀分布到全部 bank 顺序读 → 全 bank 并行", FONTS["small"], GRAY)
            center(d, 640, 560, "结果由主机直接拼接，无跨 BG 累加 → 扩展到多芯片只需继续切分 M、K", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v03 近存访问 vs 传统 ============
def access_demo():
    frames = []
    NCYC = 60
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "近存访问 vs 传统 DRAM 访问（连续读）", FONTS["title"], WHITE)
            # 左：传统
            panel(d, [60, 120, 600, 380], "传统：CPU ↔ LPDDR4")
            d.rounded_rectangle([100, 200, 260, 300], radius=8, fill=(30, 44, 66, 255), outline=WHITE, width=2)
            center(d, 180, 250, "CPU", FONTS["text"], WHITE)
            d.rounded_rectangle([420, 200, 560, 300], radius=8, fill=(30, 44, 66, 255), outline=WHITE, width=2)
            center(d, 490, 250, "LPDDR4", FONTS["text"], WHITE)
            # 数据块往返（长路径）
            p = (t % 1)
            x = 260 + p * 160
            d.ellipse([x, 238, x + 20, 258], fill=GRAY)
            center(d, 330, 350, f"单次往返 ≈ 46 ns（连续读，折算 1.2GHz 系统）", FONTS["small"], RED)
            # 右：近存
            panel(d, [660, 120, 1220, 380], "本设计：ACC 就在 DRAM 旁边")
            d.rounded_rectangle([700, 170, 900, 260], radius=8, fill=(30, 60, 44, 255), outline=GREEN, width=2)
            center(d, 800, 215, "3D DRAM", FONTS["text"], WHITE)
            d.rounded_rectangle([1000, 170, 1180, 260], radius=8, fill=(24, 44, 68, 255), outline=BLUE, width=2)
            center(d, 1090, 215, "ACC", FONTS["text"], WHITE)
            d.rounded_rectangle([700, 290, 1180, 330], radius=8, fill=(30, 44, 66, 255), outline=ORANGE, width=2)
            center(d, 940, 310, "2048b 缓冲（buf_hit 直接命中）", FONTS["small"], ORANGE)
            p2 = (t * 3 % 1)
            x2 = 900 + p2 * 100
            d.ellipse([x2, 208, x2 + 16, 224], fill=GREEN)
            center(d, 940, 360, f"连续读 ≈ 3.24 ns（-93%）", FONTS["small"], GREEN)
            # 累计
            center(d, 640, 560, "连续访问 -90%~-93%；随机访问 -37%~-44%；DMA+缓冲使 GEMM 吞吐 +53.8%", FONTS["text"], WHITE)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(stack_demo(), "v01_3d_stack.mp4")
    write_video(gemm_demo(), "v02_gemm.mp4")
    write_video(access_demo(), "v03_access.mp4")
    print("PAPER08 VIDEOS DONE")
