# -*- coding: utf-8 -*-
"""论文03教学图：能效 / 精度 / 近似收益"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\03_ISSCC2025_14.5_DualMode_Transpose_CIM\assets\charts"
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

# c01 能效（FP8 192.3 峰值，示意与其他格式关系）
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["FP8\n（近似模式峰值）", "FP8\n（精确模式）", "BF16", "INT8"]
vals = [192.3, 145, 118, 102]
colors = [GREEN, BLUE, PURPLE, ORANGE]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 3, f"{v}", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 225)
ax.set_ylabel("能效 (TFLOPS/W 或 TOPS/W)", fontsize=12.5, color=INK)
ax.set_title("28nm 转置 DCIM 能效（论文 Fig. 14.5.6）\nFP8 峰值 192.3 TFLOPS/W（0.55V，50% 权重稀疏，近似模式）；其余为量级示意",
             fontsize=13, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_energy.png"), bbox_inches="tight")
plt.close(fig)

# c02 精度
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["INT4", "FP8", "INT8", "BF16"]
vals = [92.1, 94.8, 95.6, 95.7]  # 示意（FP8 略低但远高于 INT4）
colors = [GRAY, GREEN, BLUE, PURPLE]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.3, f"{v:.1f}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(88, 99)
ax.set_ylabel("推理精度（示意，%）", fontsize=13, color=INK)
ax.set_title("格式精度对比（论文 Fig. 14.5.6 结论示意）\nFP8 略低于 INT8/BF16、显著高于 INT4；能效却最优 → 精度-能效平衡点",
             fontsize=13, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_accuracy.png"), bbox_inches="tight")
plt.close(fig)

# c03 近似模式收益
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8), dpi=150)
ax = axes[0]
labels = ["计算速度", "功耗"]
vals = [12, 31]
bars = ax.bar(labels, vals, color=[GREEN, BLUE], width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.8, f"+{v}%" if v == 12 else f"-{v}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 40)
ax.set_ylabel("变化 (%)", fontsize=12, color=INK)
ax.set_title("近似模式 vs 精确模式（论文 Fig. 14.5.5）", fontsize=13, fontweight="bold", color=INK, pad=10)

ax = axes[1]
ax.bar(["NMED\n(归一化平均误差距离)"], [5.3], color=PURPLE, width=0.4, edgecolor="white", linewidth=1.5, zorder=3)
ax.text(0, 5.9, "5.3%", ha="center", fontsize=14, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 8)
ax.set_ylabel("误差 (%)", fontsize=12, color=INK)
ax.set_title("近似误差（50k 随机采样）\n误差高斯分布、均值≈0（有偏置补偿）", fontsize=13, fontweight="bold", color=INK, pad=10)
fig.suptitle("DMBP-MAC 双模式权衡", fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(os.path.join(OUT, "c03_approx.png"), bbox_inches="tight")
plt.close(fig)

print("paper03 charts done")
