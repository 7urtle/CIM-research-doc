# -*- coding: utf-8 -*-
"""论文11教学图：能效 / Winograd 权衡 / MDPS 收益"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

for cand in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc"]:
    if os.path.exists(cand):
        fm.fontManager.addfont(cand)
        break
plt.rcParams["font.family"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\11_JSSC2025_TwoCycle_Winograd_CIM\assets\charts"
os.makedirs(OUT, exist_ok=True)
BLUE = "#0e5a8a"; GREEN = "#1d8a5f"; ORANGE = "#e8a33d"
RED = "#c25e2e"; PURPLE = "#6b3fa0"; GRAY = "#9aa8bd"; INK = "#1a2332"

def style_ax(ax):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color("#b8c4d6")
    ax.tick_params(colors="#45536b", labelsize=11)
    ax.yaxis.grid(True, color="#e3e9f2", linewidth=1)
    ax.set_axisbelow(True)

# c01 能效
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["19.9~258.5\nTOPS/W 范围", "峰值\n(0.6V/116MHz)"]
vals = [140, 258.5]
colors = [BLUE, GREEN]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
ax.text(0, 148, "19.9~258.5", ha="center", fontsize=12.5, fontweight="bold", color=INK)
ax.text(1, 265, "258.5 TOPS/W", ha="center", fontsize=13, fontweight="bold", color=GREEN)
style_ax(ax)
ax.set_ylim(0, 320)
ax.set_ylabel("系统能效 (TOPS/W)", fontsize=13, color=INK)
ax.set_title("28nm CiM 处理器系统能效（论文 Fig. 17）\n0.6~1.1V · 78~287MHz · 峰值 258.5 TOPS/W @0.6V/116MHz（中值为范围示意）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_energy.png"), bbox_inches="tight")
plt.close(fig)

# c02 Winograd 权衡
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["基线（空间域）", "F2 单用", "F4 单用", "混合 F2+F4"]
speed = [1.0, 1.92, 3.32, 2.59]
loss = [0, 0, 9.1, 0.6]
colors = [GRAY, BLUE, RED, GREEN]
bars = ax.bar(labels, speed, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, s, l in zip(bars, speed, loss):
    ax.text(b.get_x()+b.get_width()/2, s + 0.08, f"{s}×" + (f"\n精度 −{l}%" if l else "\n无损"), ha="center", fontsize=11.5, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 4.0)
ax.set_ylabel("加速 (×，ResNet34@ImageNet)", fontsize=12.5, color=INK)
ax.set_title("Winograd 加速与精度权衡（论文 Fig. 12）\n混合策略 2.59× 且几乎无损 —— 帕累托最优点", fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_winograd.png"), bbox_inches="tight")
plt.close(fig)

# c03 MDPS 收益
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["50% 激活稀疏", "50% 权重稀疏", "双端 50%（合计）"]
vals = [1.84, 1.76, 3.11]
colors = [BLUE, PURPLE, GREEN]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.06, f"{v}×", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 3.8)
ax.set_ylabel("能效提升 (×，ResNet34)", fontsize=12.5, color=INK)
ax.set_title("MDPS 双端稀疏收益（论文 Fig. 16）\nISPU/PPRS/OMB 面积 4.5%、功耗 7.8%", fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_mdps.png"), bbox_inches="tight")
plt.close(fig)

print("paper11 charts done")
