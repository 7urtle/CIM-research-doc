# -*- coding: utf-8 -*-
"""论文06教学图：能效 / PBW精度 / SDBS收益"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\06_ISSCC2026_30.1_MXFP-CIM\assets\charts"
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
fig, ax = plt.subplots(figsize=(9.0, 5.0), dpi=150)
labels = ["MXFP6/6\n峰值能效", "MXFP8/8\n峰值能效", "LLaMA-3.1 8B\n推理", "ResNet-18\n训练"]
vals = [127.54, 117.42, 49.53, 19.11]
colors = [GREEN, BLUE, PURPLE, ORANGE]
bars = ax.bar(labels, vals, color=colors, width=0.55, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 2.5, f"{v}", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 150)
ax.set_ylabel("能效 (TFLOPS/W)", fontsize=12.5, color=INK)
ax.set_title("28nm MXFP-CIM 实测能效（论文 Fig. 30.1.6）\nMXFP6 127.54 / MXFP8 117.42 TFLOPS/W；推理 49.53、训练 19.11 TFLOPS/W",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_energy.png"), bbox_inches="tight")
plt.close(fig)

# c02 MRE vs PBW
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
import numpy as np
pbw = np.array([3, 5, 7, 9, 11, 13, 15, 17, 19, 23, 27])
mre = 100 * np.exp(-0.12 * (pbw - 3)) + 0.8
ax.plot(pbw, mre, marker="o", color=BLUE, lw=2.2, zorder=4)
ax.fill_between(pbw, mre, alpha=0.15, color=BLUE)
ax.axvspan(3, 9, alpha=0.08, color=RED)
ax.axvspan(11, 17, alpha=0.08, color=GREEN)
ax.axvspan(19, 27, alpha=0.08, color=ORANGE)
ax.text(6, 60, "BERT\n<1% 精度损失", fontsize=10.5, color=RED, ha="center")
ax.text(14, 60, "LLaMA-3.1 8B\n近无损", fontsize=10.5, color=GREEN, ha="center")
ax.text(23, 60, "训练\n(略胜 BF16)", fontsize=10.5, color=ORANGE, ha="center")
style_ax(ax)
ax.set_xlabel("保留位宽 PBW (bit)", fontsize=12.5, color=INK)
ax.set_ylabel("平均相对误差 MRE（示意，%）", fontsize=12, color=INK)
ax.set_title("MRE 随 PBW 单调下降（论文 Fig. 30.1.5 趋势示意）\n精度-效率权衡：PBW 越高越准但周期/功耗越高",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_pbw_mre.png"), bbox_inches="tight")
plt.close(fig)

# c03 SDBS 收益
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8), dpi=150)
ax = axes[0]
cats = ["vs 位并行对齐 [8,10]", "vs 位串行对齐 [11]"]
area = [3.85, 1.53]
energy = [1.44, 1.43]
x = [0, 1]
b1 = ax.bar([i-0.19 for i in x], area, width=0.36, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3, label="面积降低 (×)")
b2 = ax.bar([i+0.19 for i in x], energy, width=0.36, color=GREEN, edgecolor="white", linewidth=1.5, zorder=3, label="能量降低 (×)")
for i in x:
    ax.text(i-0.19, area[i]+0.08, f"{area[i]}×", ha="center", fontsize=12, fontweight="bold", color=BLUE)
    ax.text(i+0.19, energy[i]+0.08, f"{energy[i]}×", ha="center", fontsize=12, fontweight="bold", color=GREEN)
style_ax(ax)
ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=11)
ax.set_ylim(0, 4.5)
ax.set_ylabel("降低倍数 (×)", fontsize=12, color=INK)
ax.set_title("SDBS 滑动对齐方案收益\n（论文 Fig. 30.1.5 仿真）", fontsize=13, fontweight="bold", color=INK, pad=10)
ax.legend(fontsize=10.5)

ax = axes[1]
cats2 = ["加法树输入位宽", "面积开销", "功耗"]
vals2 = [42.9, 35.9, 40.0]
bars = ax.bar(cats2, vals2, color=PURPLE, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals2):
    ax.text(b.get_x()+b.get_width()/2, v + 1, f"-{v}%", ha="center", fontsize=12.5, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 55)
ax.set_ylabel("减少 (%)", fontsize=12, color=INK)
ax.set_title("6 全加器乘积压缩器的收益\n（对比输入对齐方案 [6,7,9,11]）", fontsize=13, fontweight="bold", color=INK, pad=10)
fig.suptitle("SDBS 与压缩器设计收益（论文 Fig. 30.1.3/30.1.5）", fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(os.path.join(OUT, "c03_sdbs.png"), bbox_inches="tight")
plt.close(fig)

print("paper06 charts done")
