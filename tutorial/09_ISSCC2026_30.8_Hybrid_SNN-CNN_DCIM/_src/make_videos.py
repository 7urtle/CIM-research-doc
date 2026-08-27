# -*- coding: utf-8 -*-
"""论文09演示视频：神经元膜电位动画 / 双模式数据流 / 数据映射对比"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\09_ISSCC2026_30.8_Hybrid_SNN-CNN_DCIM\assets\videos"
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
INK = (26, 35, 50); GRAY = (127, 147, 173); WHITE = (240, 244, 250)
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

# ============ v01 神经元膜电位（IF / LIF / IQIF 对比） ============
def neuron_demo():
    frames = []
    # 三种模型曲线数据（预计算）
    def if_traj(spikes, thresh):
        mp = 0; out = []
        for s in spikes:
            mp += s
            if mp >= thresh: mp = 0
            out.append(mp)
        return out
    def lif_traj(spikes, thresh, leak):
        mp = 0; out = []
        for s in spikes:
            mp = max(0, mp - leak) + s
            if mp >= thresh: mp = 0
            out.append(mp)
        return out
    def iqif_traj(spikes, thresh, alpha, beta, rest, pdeth):
        mp = 0; out = []
        for s in spikes:
            if mp < pdeth: iq = (alpha*rest - mp) >> 3
            else: iq = (beta*(mp - thresh)) >> 3
            mp = max(0, mp + iq) + s
            if mp >= thresh: mp = 0
            out.append(mp)
        return out
    import random
    random.seed(7)
    spikes = [1 if random.random() < 0.45 else 0 for _ in range(48)]
    thresh = 8
    trajs = {
        "IF": if_traj(spikes, thresh),
        "LIF": lif_traj(spikes, thresh, 1),
        "IQIF": iqif_traj(spikes, thresh, 3, 2, 2, 3),
    }
    modes = ["IF", "LIF", "IQIF"]
    colors = {"IF": BLUE, "LIF": PURPLE, "IQIF": GREEN}
    desc = {"IF": "积分到阈值就发放并清零（简单）", "LIF": "每步漏电 → 滤时间噪声", "IQIF": "整数二次项 → 非线性积分更准"}

    # 第一段：单个模式逐个演示
    for mi, mode in enumerate(modes):
        for i in range(FPS * 4):
            im, d = new_frame()
            t = i / FPS
            center(d, W//2, 70, "神经元模型：" + mode, FONTS["title"], colors[mode])
            center(d, W//2, 120, desc[mode], FONTS["text"], GRAY)
            # 绘图区
            x0, y0, x1, y1 = 120, 180, 1160, 560
            d.rectangle([x0, y0, x1, y1], fill=(14, 24, 38, 255), outline=LINE)
            d.line([x0, y0, x1, y0], fill=GRAY)  # 顶部=阈值线下方
            # 阈值线（在 y0+40 处，视觉上）
            thy = y0 + 60
            d.line([x0, thy, x1, thy], fill=RED, width=2)
            d.text((x1+8, thy-9), "阈值", font=FONTS["small"], fill=RED)
            # 当前显示步数
            nshow = min(len(trajs[mode]), int(t * 10) + 2)
            traj = trajs[mode][:nshow]
            # 画线
            pts = []
            for k, v in enumerate(traj):
                px = x0 + k * (x1 - x0) / 47
                py = y1 - 20 - v * ((y1 - y0 - 60) / (thresh + 2))
                pts.append((px, py))
            if len(pts) > 1:
                d.line(pts, fill=colors[mode], width=4)
            # 脉冲条
            for k in range(nshow):
                if spikes[k]:
                    px = x0 + k * (x1 - x0) / 47
                    d.rectangle([px, y1 - 14, px + 8, y1 - 2], fill=ORANGE)
            d.text((x0, y1 + 14), "橙色竖条 = 输入脉冲（1b spike）", font=FONTS["small"], fill=ORANGE)
            d.text((x0 + 460, y1 + 14), "曲线 = 膜电位 MP（撞阈值清零）", font=FONTS["small"], fill=colors[mode])
            # 当前 MP 值
            if traj:
                center(d, W//2, 640, f"当前膜电位 = {traj[-1]}　/　阈值 = {thresh}", FONTS["text"], WHITE)
            frames.append(im)

    # 第二段：三模并排对比
    for i in range(FPS * 5):
        im, d = new_frame()
        t = i / FPS
        center(d, W//2, 56, "三种神经元模型对比（同一输入脉冲序列）", FONTS["title"], WHITE)
        nshow = min(48, int(t * 12) + 3)
        for mi, mode in enumerate(modes):
            x0 = 60 + mi * 400; x1 = x0 + 360; y0 = 150; y1 = 560
            panel(d, [x0-16, y0-16, x1+16, y1+16], mode + " · " + ("积分" if mode=="IF" else "泄漏" if mode=="LIF" else "二次"))
            d.line([x0, y0, x1, y0], fill=GRAY)
            thy = y0 + 60
            d.line([x0, thy, x1, thy], fill=RED, width=2)
            traj = trajs[mode][:nshow]
            pts = []
            for k, v in enumerate(traj):
                px = x0 + k * (x1 - x0) / 47
                py = y1 - 20 - v * ((y1 - y0 - 60) / (thresh + 2))
                pts.append((px, py))
            if len(pts) > 1:
                d.line(pts, fill=colors[mode], width=3)
            for k in range(nshow):
                if spikes[k]:
                    px = x0 + k * (x1 - x0) / 47
                    d.rectangle([px, y1 - 10, px + 6, y1 - 2], fill=ORANGE)
            if traj:
                center(d, (x0+x1)//2, 640, f"MP={traj[-1]}", FONTS["text"], colors[mode])
        center(d, W//2, 690, "看差异：LIF 无输入时膜电位会掉（泄漏）；IQIF 在阈值附近有非线性加速", FONTS["small"], GRAY)
        frames.append(im)
    return frames

# ============ v02 双模式数据流（SNN/CNN 切换） ============
def mode_flow_demo():
    frames = []
    NCYC = 20
    for cyc in range(NCYC):
        snn = (cyc % 2) == 0
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            mode = "SNN 模式（1b 脉冲）" if snn else "CNN 模式（8b 字宽）"
            col = BLUE if snn else RED
            center(d, W//2, 56, "数据流演示：" + mode, FONTS["title"], col)
            # 左侧：输入
            panel(d, [60, 120, 300, 300], "输入")
            if snn:
                for k in range(10):
                    if (cyc + k) % 3 != 0:
                        px = 80 + ((t + k/10) % 1) * 200
                        d.ellipse([px, 180, px+14, 194], fill=ORANGE)
                center(d, 180, 250, "稀疏脉冲流", FONTS["text"], WHITE)
            else:
                for k in range(8):
                    px = 80 + ((t + k/8) % 1) * 200
                    d.rectangle([px, 180, px+22, 196], fill=col)
                center(d, 180, 250, "稠密 8b 数据流", FONTS["text"], WHITE)
            # 中间：CMDM-LCC
            panel(d, [360, 120, 700, 380], "CMDM-LCC（跨模型双模式）")
            d.rounded_rectangle([390, 170, 640, 230], radius=8, fill=(26, 44, 70, 255), outline=col, width=2)
            center(d, 515, 200, "两个 MUX 乘法器", FONTS["text"], WHITE)
            d.rounded_rectangle([390, 250, 640, 310], radius=8, fill=(40, 34, 26, 255), outline=ORANGE, width=2)
            center(d, 515, 280, "SaA（CNN 才启用）", FONTS["text"], ORANGE if not snn else GRAY)
            # pMAC
            for k in range(6):
                d.rectangle([390 + k*44, 330, 390 + k*44 + 30, 348], fill=PURPLE)
            center(d, 515, 366, "pMAC0–7", FONTS["small"], PURPLE)
            # 右侧：出口
            panel(d, [760, 120, 1220, 380], "出口")
            if snn:
                d.rounded_rectangle([790, 170, 1190, 250], radius=8, fill=(26, 44, 70, 255), outline=BLUE, width=2)
                center(d, 990, 190, "DM-MPDBU：IF/LIF/IQIF", FONTS["text"], WHITE)
                center(d, 990, 218, "膜电位积分 → 发放脉冲", FONTS["small"], GRAY)
                d.rounded_rectangle([790, 270, 1190, 330], radius=8, fill=(30, 60, 44, 255), outline=GREEN, width=2)
                center(d, 990, 300, "输出脉冲到下一层", FONTS["text"], WHITE)
            else:
                d.rounded_rectangle([790, 170, 1190, 250], radius=8, fill=(54, 40, 34, 255), outline=RED, width=2)
                center(d, 990, 190, "跳过神经元（无 MPDB）", FONTS["text"], WHITE)
                center(d, 990, 218, "直接输出 8b 特征", FONTS["small"], GRAY)
                d.rounded_rectangle([790, 270, 1190, 330], radius=8, fill=(30, 60, 44, 255), outline=GREEN, width=2)
                center(d, 990, 300, "外部激活函数（ReLU 等）", FONTS["text"], WHITE)
            # 模式切换提示
            if t < 0.4:
                center(d, 640, 660, "模式由层配置决定：SNN 层 → 脉冲路径；CNN 层 → SaA + 直通", FONTS["small"], GRAY)
            frames.append(im)
    return frames

# ============ v03 数据映射对比（TS-first vs 复用-first vs PS-WR-ODM） ============
def mapping_demo():
    frames = []
    NCYC = 60
    for cyc in range(NCYC):
        for i in range(FPS // 2):
            im, d = new_frame()
            t = (i % (FPS//2)) / (FPS//2)
            center(d, W//2, 56, "数据映射策略对比（K=8 个输入神经元，N=8 个时间步）", FONTS["title"], WHITE)
            # 三个方案并排
            schemes = [
                ("① TS-first（时间步优先）", "权重反复加载：W 更新能耗高 · PSUM 小", RED, 0.9),
                ("② 复用-first（权重复用优先）", "权重只读一次 · PSUM 缓冲巨大", PURPLE, 3.4),
                ("③ PS-WR-ODM（本文，块=2 TS）", "块内复用：W 能耗低 · PSUM 只增一点", GREEN, 1.6),
            ]
            for si, (name, note, col, cost) in enumerate(schemes):
                x0 = 40 + si * 400; x1 = x0 + 380; y0 = 140; y1 = 560
                d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=PANEL, outline=col, width=2)
                center(d, (x0+x1)//2, y0+24, name, FONTS["med"], col)
                # 权重加载条（随时间增长）
                load = min(1.0, (cyc / NCYC) * cost / 2.0)
                if si == 0:
                    load = min(1.0, (cyc / NCYC) * 1.6)
                elif si == 1:
                    load = min(1.0, (cyc / NCYC) * 0.5)
                else:
                    load = min(1.0, (cyc / NCYC) * 0.9)
                d.rounded_rectangle([x0+20, y0+60, x1-20, y0+80], radius=6, fill=(40, 60, 84, 255))
                d.rectangle([x0+20, y0+60, x0+20 + (x1-x0-40)*load, y0+80], fill=RED)
                d.text((x0+20, y0+86), f"权重加载/更新能耗 {load*100:.0f}%", font=FONTS["small"], fill=RED)
                # PSUM 存储条
                psum = 0.15 if si == 0 else (0.85 if si == 1 else 0.35)
                d.rounded_rectangle([x0+20, y0+120, x1-20, y0+140], radius=6, fill=(40, 60, 84, 255))
                d.rectangle([x0+20, y0+120, x0+20 + (x1-x0-40)*psum, y0+140], fill=BLUE)
                d.text((x0+20, y0+146), f"PSUM 缓冲占用 {psum*100:.0f}%", font=FONTS["small"], fill=BLUE)
                # 时间轴
                d.text((x0+20, y0+180), "时间轴（块内遍历顺序）", font=FONTS["small"], fill=GRAY)
                for k in range(8):
                    px = x0 + 20 + k * ((x1-x0-40)/8)
                    d.rectangle([px, y0+200, px+((x1-x0-40)/8)-4, y0+220], fill=(30, 48, 72, 255), outline=GRAY)
                # 当前游标
                pos = x0 + 20 + (cyc % NCYC) / NCYC * (x1 - x0 - 40)
                d.polygon([(pos, y0+230), (pos-8, y0+242), (pos+8, y0+242)], fill=ORANGE)
                d.text((x0+20, y0+280), note, font=FONTS["small"], fill=col)
            center(d, W//2, 640, "结论：③ 用‘块内权重复用’同时压低权重更新能耗与 PSUM 存储 → FoM1 提升 >1.22×", FONTS["text"], GREEN)
            frames.append(im)
    return frames

if __name__ == "__main__":
    write_video(neuron_demo(), "v01_neuron.mp4")
    write_video(mode_flow_demo(), "v02_modes.mp4")
    write_video(mapping_demo(), "v03_mapping.mp4")
    print("PAPER09 VIDEOS DONE")
