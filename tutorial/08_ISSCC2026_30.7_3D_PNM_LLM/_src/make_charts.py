# -*- coding: utf-8 -*-
"""论文08教学图：带宽密度 / 每比特能量 / 访问延迟 / GEMM 执行时间"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\08_ISSCC2026_30.7_3D_PNM_LLM\assets\charts"
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

# c01 带宽密度
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["本论文 3D PNM\n(1.2GHz)", "HBM3E", "GDDR6"]
vals = [12.77, 12.77 / 1.22, 12.77 / 8.63]
colors = [GREEN, BLUE, GRAY]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.35, f"{v:.1f}", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 15.5)
ax.set_ylabel("带宽密度 (GB/s/mm²)", fontsize=13, color=INK)
ax.set_title("带宽密度对比（论文 Fig. 30.7.6）\n本设计 12.77 GB/s/mm² = HBM3E 的 1.22× = GDDR6 的 8.63×（HBM3E/GDDR6 为按倍数换算值）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_bandwidth.png"), bbox_inches="tight")
plt.close(fig)

# c02 每比特能量
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["本论文 3D PNM", "HBM3E", "GDDR6"]
vals = [0.67, 0.67 / 0.28, 0.67 / 0.09]
colors = [GREEN, BLUE, GRAY]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.2, f"{v:.2f}", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 8.5)
ax.set_ylabel("每比特访问能量 (pJ/b)", fontsize=13, color=INK)
ax.set_title("每比特访问能量对比（论文 Fig. 30.7.4）\n本设计 0.67 pJ/b = GDDR6 的 9% = HBM3E 的 28%（越低越好）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_energy.png"), bbox_inches="tight")
plt.close(fig)

# c03 访问延迟
fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=150)
import numpy as np
cats = ["连续写\n(8192次)", "连续读", "随机写", "随机读"]
ours = [3.21, 3.24, 45.12, 50.01]
lpddr = [32.1, 46.3, 71.6, 89.3]
x = np.arange(4)
b1 = ax.bar(x - 0.19, lpddr, width=0.36, color=GRAY, edgecolor="white", linewidth=1.5, zorder=3, label="LPDDR4（系统频率折算到 1.2GHz）")
b2 = ax.bar(x + 0.19, ours, width=0.36, color=GREEN, edgecolor="white", linewidth=1.5, zorder=3, label="本论文 3D 近存")
for i, (l, o) in enumerate(zip(lpddr, ours)):
    ax.text(i - 0.19, l + 1, f"{l:.0f}", ha="center", fontsize=11, color=INK)
    ax.text(i + 0.19, o + 1, f"{o:.1f}", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    pct = (1 - o / l) * 100
    ax.text(i, max(l, o) + 6, f"-{pct:.0f}%", ha="center", fontsize=12.5, fontweight="bold", color=RED)
style_ax(ax)
ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=12)
ax.set_ylim(0, 108)
ax.set_ylabel("访问延迟 (ns)", fontsize=13, color=INK)
ax.set_title("访存延迟对比（论文 Fig. 30.7.5）\n连续访问 -90%~-93%、随机访问 -37%~-44%（LPDDR4 为按缩减比例反推的换算值）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
ax.legend(fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_latency.png"), bbox_inches="tight")
plt.close(fig)

# c04 GEMM 执行时间
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["CPU i7-13700F\n(2.1GHz)", "本论文 1 芯片", "8 芯片 DIMM\n(8GB, 128 ACC)"]
vals = [100, 14, 2]
colors = [GRAY, GREEN, BLUE]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 1.5, f"{v}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 115)
ax.set_ylabel("128×128×128 GEMM 执行时间（归一化，%）", fontsize=12.5, color=INK)
ax.set_title("GEMM 执行时间对比（论文 Fig. 30.7.5）\n1 芯片 -86%；扩展到 8 芯片 DIMM 系统 -98%（归一化到 CPU = 100%）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c04_gemm.png"), bbox_inches="tight")
plt.close(fig)

print("paper08 charts done")
