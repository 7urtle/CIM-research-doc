# -*- coding: utf-8 -*-
"""论文12演示视频：SpG 采集 / EOCI 初始化 / ILA 计算"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\12_JSSC2025_TensorCIM\assets\videos"
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

# ============ v01 REGM 采集 ============
def regm_demo():
    frames = []
    NCYC = 24
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "REGM 冗余消除采集：高频特征住进 CIM", FONTS["title"], WHITE)
            # 访问张量
            feats = [("f0", 5), ("f1", 3), ("f2", 1), ("f3", 4), ("f4", 1), ("f5", 1)]
            for idx, (name, cnt) in enumerate(feats):
                x0 = 90 + idx * 180
                hot = cnt >= 3
                d.rounded_rectangle([x0, 140, x0 + 160, 240], radius=10,
                                     fill=(26, 60, 44, 255) if hot else PANEL,
                                     outline=GREEN if hot else LINE, width=2 if hot else 1)
                center(d, x0 + 80, 175, name, FONTS["med"], GREEN if hot else GRAY)
                center(d, x0 + 80, 215, f"访问 {cnt} 次" + ("（高频→入 CIM）" if hot else "（低频→DRAM）"), FONTS["small"], WHITE if hot else GRAY)
            # 归约复用
            d.rounded_rectangle([90, 280, 1000, 360], radius=10, fill=PANEL, outline=ORANGE, width=2)
            center(d, 545, 305, "归约复用：f0+f3 被重复需要 → 结果存 CIM，后续直接复用（不再重算）", FONTS["text"], ORANGE)
            center(d, 545, 345, "未命中才触发 DRAM/跨芯粒访问 + REGM 更新（驱逐低频特征）", FONTS["small"], GRAY)
            center(d, 640, 420, "→ 实测：DRAM 访问 −1.74× · 跨芯粒 −3.55× · 归约 −1.35×", FONTS["text"], GREEN)
            center(d, 640, 480, "访问张量重排 → 聚类分组 → 各芯粒主要访问本地 DRAM", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v02 EOCI 初始化 ============
def eoci_demo():
    frames = []
    NCYC = 20
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "EOCI 等操作初始化：按有效 MAC 数平衡子阵列", FONTS["title"], WHITE)
            # 相交识别
            d.rounded_rectangle([60, 130, 600, 420], radius=10, fill=PANEL, outline=PURPLE, width=2)
            center(d, 330, 160, "① 有效操作识别", FONTS["med"], PURPLE)
            gt_ids = [0, 1, 2, 3, 4, 7]
            wt_ids = [0, 4, 5, 6, 7]
            for idx, v in enumerate(gt_ids):
                x0 = 90 + idx * 80
                inter = wt_ids.includes(v) if False else v in wt_ids
                d.rounded_rectangle([x0, 190, x0 + 70, 250], radius=8,
                                     fill=(40, 30, 46, 255) if inter else (24, 30, 44, 255),
                                     outline=ORANGE if inter else PURPLE, width=2)
                center(d, x0 + 35, 220, str(v), FONTS["small"], WHITE)
            center(d, 330, 290, "GT 非零列 {0,1,2,3,4,7} ∩ WT 非零行 {0,4,5,6,7}", FONTS["small"], GRAY)
            center(d, 330, 320, "相交 {0,4,7}（橙）= 有效 MAC；其余跳过", FONTS["text"], ORANGE)
            center(d, 330, 370, "操作数 = GT 列非零数 × WT 行非零数", FONTS["small"], GRAY)
            # 平衡分配
            d.rounded_rectangle([660, 130, 1220, 420], radius=10, fill=PANEL, outline=GREEN, width=2)
            center(d, 940, 160, "② 平衡的 WT/GT 分配", FONTS["med"], GREEN)
            d.rounded_rectangle([690, 200, 1160, 280], radius=10, fill=(26, 50, 40, 255), outline=GREEN, width=2)
            center(d, 925, 225, "Core0：Row{0,10,4,13} ｜ Core1：Row{7,15,9,16}", FONTS["text"], WHITE)
            center(d, 925, 265, "每子阵列 MAC 数相同 → 同时算完（无空闲）", FONTS["small"], GREEN)
            center(d, 940, 330, "CIM 自适应 WT 映射：大 WT 分片、纵向遍历", FONTS["text"], WHITE)
            center(d, 940, 380, "→ 利用率 17.6%→95.4%（配合 ILA）· EOCI 面积 +1.96%", FONTS["small"], ORANGE)
            frames.append(im)
    return frames

# ============ v03 ILA 前瞻 ============
def ila_demo():
    frames = []
    NCYC = 20
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "ILA-CIM 输入前瞻：空闲子阵列提前算未来输入", FONTS["title"], WHITE)
            # 传统
            d.rounded_rectangle([60, 130, 600, 400], radius=10, fill=PANEL, outline=RED, width=2)
            center(d, 330, 160, "传统：一次一行", FONTS["med"], RED)
            for r in range(3):
                for c in range(4):
                    x0 = 90 + c * 120; y0 = 190 + r * 60
                    busy = (r == 0 and c == 0)
                    d.rounded_rectangle([x0, y0, x0 + 105, y0 + 48], radius=8,
                                         fill=(46, 34, 26, 255) if busy else (20, 28, 40, 255),
                                         outline=ORANGE if busy else LINE, width=2)
                    center(d, x0 + 52, y0 + 24, "忙" if busy else "空闲", FONTS["small"], WHITE if busy else GRAY)
            center(d, 330, 420, "输入行稀疏 → 大部分子阵列空闲 → 利用率 17.6%", FONTS["small"], RED)
            # ILA
            d.rounded_rectangle([660, 130, 1220, 400], radius=10, fill=PANEL, outline=GREEN, width=2)
            center(d, 940, 160, "ILA-CIM：前瞻未来输入", FONTS["med"], GREEN)
            for r in range(3):
                for c in range(4):
                    x0 = 690 + c * 120; y0 = 190 + r * 60
                    busy = (r == 0 and c == 0) or (r == 2 and c == 3)
                    d.rounded_rectangle([x0, y0, x0 + 105, y0 + 48], radius=8,
                                         fill=(30, 50, 40, 255) if busy else (26, 44, 70, 255),
                                         outline=GREEN if busy else BLUE, width=2)
                    center(d, x0 + 52, y0 + 24, "现在" if (r == 0 and c == 0) else "未来" if (r == 2 and c == 3) else "忙", FONTS["small"], WHITE)
            center(d, 940, 420, "所有子阵列保持忙碌 → 利用率 95.4%（联合）", FONTS["small"], GREEN)
            center(d, 640, 470, "三步：① 输入前瞻 → ② FP 对齐（指数和归一化）→ ③ 输出合并（写回全局缓冲）", FONTS["text"], WHITE)
            center(d, 640, 530, "稀疏归约也在 ILA-CIM 里做（不加载特征张量中的零）→ 1.88× 加速（单独）· 5.28×（联合）", FONTS["small"], GRAY)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(regm_demo(), "v01_regm.mp4")
    write_video(eoci_demo(), "v02_eoci.mp4")
    write_video(ila_demo(), "v03_ila.mp4")
    print("PAPER12 VIDEOS DONE")
