# -*- coding: utf-8 -*-
"""生成教学用数据图表（面积/功耗分解、性能对比、能效测量）"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ---- 中文字体 ----
for cand in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
    if os.path.exists(cand):
        fm.fontManager.addfont(cand)
        break
plt.rcParams["font.family"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\10_ISSCC2026_30.9_ZeroPoint_DCiM\assets\charts"
os.makedirs(OUT, exist_ok=True)

BLUE = "#0e5a8a"; BLUE2 = "#0f7cb6"; GREEN = "#1d8a5f"; ORANGE = "#e8a33d"
RED = "#c25e2e"; PURPLE = "#6b3fa0"; GRAY = "#9aa8bd"; INK = "#1a2332"

def style_ax(ax):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color("#b8c4d6")
    ax.tick_params(colors="#45536b", labelsize=11)
    ax.yaxis.grid(True, color="#e3e9f2", linewidth=1)
    ax.set_axisbelow(True)

# ============ c01 面积分解 ============
fig, ax = plt.subplots(figsize=(9.2, 5.2), dpi=150)
labels = ["Booth选择器\n+ 加法树", "存储锁存\n+ 读 MUX", "Booth编码器\n+ S位 + 零点\n预计算", "写数据驱动\n+ 译码器", "其他"]
vals = [74, 21, 2, 3, 0]
vals[-1] = 100 - sum(vals[:-1])
colors = [BLUE, GREEN, PURPLE, ORANGE, GRAY]
bars = ax.bar(labels, vals, color=colors, width=0.62, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 88)
ax.set_ylabel("面积占比 (%)", fontsize=12.5, color=INK)
ax.set_title("DCiM 面积分解（论文 Fig. 30.9.4）\nBooth 选择器与加法树占 74% —— 计算逻辑主导面积",
             fontsize=14.5, fontweight="bold", color=INK, pad=14)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_area_breakdown.png"), bbox_inches="tight")
plt.close(fig)

# ============ c02 功耗分解（写功耗 与 计算功耗） ============
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.9), dpi=150)

# 左：写功耗
ax = axes[0]
wl = ["写数据驱动\n+ 译码器", "Booth编码器\n+ S位 + 零点", "存储锁存\n+ 读 MUX", "其他"]
wv = [56, 16, 11, 17]
wc = [ORANGE, PURPLE, GREEN, GRAY]
bars = ax.bar(wl, wv, color=wc, width=0.58, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, wv):
    ax.text(b.get_x()+b.get_width()/2, v+1, f"{v}%", ha="center", fontsize=12, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 68)
ax.set_title("权重写功耗分解\n（写驱动+译码器占 56%，但与面积相反只占 3%）", fontsize=13, fontweight="bold", color=INK, pad=10)
ax.set_ylabel("写功耗占比 (%)", fontsize=12, color=INK)

# 右：计算功耗
ax = axes[1]
cl = ["Booth选择器\n+ 加法树", "其他"]
cv = [98, 2]
cc = [BLUE, GRAY]
bars = ax.bar(cl, cv, color=cc, width=0.42, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, cv):
    ax.text(b.get_x()+b.get_width()/2, v+1, f"{v}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 112)
ax.set_title("计算功耗分解\n（双缓冲下写功耗降为 1%，计算主导 → 能效最高）", fontsize=13, fontweight="bold", color=INK, pad=10)
ax.set_ylabel("计算功耗占比 (%)", fontsize=12, color=INK)

fig.suptitle("功耗分解：双缓冲让“写”退居幕后（论文 Fig. 30.9.4）", fontsize=14.5, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(os.path.join(OUT, "c02_power_breakdown.png"), bbox_inches="tight")
plt.close(fig)

# ============ c03 对比散点 ============
fig, ax = plt.subplots(figsize=(8.6, 6.0), dpi=150)
# 本工作
ax.scatter([250], [147], s=260, marker="*", color=RED, edgecolor="white", linewidth=1.2, zorder=5, label="本工作 (ISSCC 2026, INT8)")
ax.annotate("本工作\n250 TOPS/mm²\n147 TOPS/W", xy=(250, 147), xytext=(215, 170),
            fontsize=12, fontweight="bold", color=RED, ha="center",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
# 近期工作（仅取论文标题/正文明确给出的可比较数字；位宽不同、归一化不同者不入图）
pts = [
    (90, 125, BLUE, "Mori VLSI'25\n3nm INT8"),
    (55, 32.5, BLUE2, "Fujiwara ISSCC'24\n3nm INT12"),
]
for x, y, c, lab in pts:
    ax.scatter([x], [y], s=120, color=c, edgecolor="white", linewidth=1, zorder=4)
    ax.annotate(lab, xy=(x, y), xytext=(x, y+12), fontsize=10.5, color=c, ha="center")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(15, 400); ax.set_ylim(15, 260)
ax.set_xlabel("面积效率 (TOPS/mm²)", fontsize=13, color=INK)
ax.set_ylabel("能效 (TOPS/W)", fontsize=13, color=INK)
ax.set_title("本工作与近期数字 CiM 对比（数据点取自论文标题/正文的明确数字）\n注：仅纳入位宽可比的 INT8/INT12 工作；按 bit 归一化或位宽不同者未入图（见正文表）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
style_ax(ax)
ax.grid(True, which="both", color="#e3e9f2", linewidth=1)
ax.legend(loc="lower right", fontsize=11, framealpha=0.9)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_compare.png"), bbox_inches="tight")
plt.close(fig)

# ============ c04 测量结果 ============
fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.8), dpi=150)

# 左：能效 vs 活动率（400mV）
ax = axes[0]
acts = ["10%", "25%", "50%", "100%"]
eff = [254, 147, 90, 60]  # 后两个为趋势示意（论文只给了前两个实测）
real = [True, True, False, False]
for a, e, r in zip(acts, eff, real):
    c = RED if r else GRAY
    ax.bar(a, e, color=c, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
    ax.text(a, e+4, f"{e}", ha="center", fontsize=12, fontweight="bold", color=INK)
    if not r:
        ax.text(a, e-16, "示意", ha="center", fontsize=9, color="#6b7a93")
style_ax(ax)
ax.set_ylim(0, 300)
ax.set_xlabel("输入活动率 (400 mV, 25°C)", fontsize=12.5, color=INK)
ax.set_ylabel("能效 (TOPS/W)", fontsize=12.5, color=INK)
ax.set_title("能效随输入活动率变化\n（活动率越低，动态功耗越小，能效越高）", fontsize=13.5, fontweight="bold", color=INK, pad=10)

# 右：频率/功耗 vs 电压
ax = axes[1]
v = [0.4, 0.55, 0.7, 0.85, 1.0, 1.1]
f = [0.30, 0.62, 1.05, 1.55, 2.15, 2.62]
p = [6.1, 38, 118, 280, 545, 1230]
ax.plot(v, f, marker="o", color=BLUE, lw=2.2, label="频率 (GHz)", zorder=4)
ax.plot(v, [x/1000 for x in p], marker="s", color=ORANGE, lw=2.2, label="功耗 (W)", zorder=4)
for x, y in zip(v, f):
    ax.annotate(f"{y:.2f}", xy=(x, y), xytext=(0, 7), textcoords="offset points", fontsize=9.5, color=BLUE, ha="center")
style_ax(ax)
ax.set_xlabel("电源电压 (V)", fontsize=12.5, color=INK)
ax.set_ylabel("频率 (GHz) / 功耗 (W)", fontsize=12.5, color=INK)
ax.set_title("频率与功耗随电压缩放（1.1V 峰值 → 400mV 低功耗）\n(400mV 功耗 6.1mW @25%活动率，示意连线)",
             fontsize=13.5, fontweight="bold", color=INK, pad=10)
ax.legend(fontsize=11, loc="upper left")

fig.suptitle("Intel 18A 实测结果：2.62 GHz / 21.5 TOPS / 250 TOPS/mm² / 147 TOPS/W（论文 Fig. 30.9.5）",
             fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.92])
fig.savefig(os.path.join(OUT, "c04_measurements.png"), bbox_inches="tight")
plt.close(fig)

print("charts done:", os.listdir(OUT))
