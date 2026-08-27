# -*- coding: utf-8 -*-
"""论文01教学图：能效 / 面积功耗收益 / 周期与稀疏性"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\01_ISSCC2025_14.3_B-A-N2CMAC_FP-CIM\assets\charts"
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
labels = ["BF16A/B 模式\n(FP32 输出)", "INT8 模式"]
vals = [62.84, 90.15]
colors = [BLUE, ORANGE]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 2, f"{v}", ha="center", fontsize=14, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 105)
ax.set_ylabel("能效 (TFLOPS/W 或 TOPS/W)", fontsize=12.5, color=INK)
ax.set_title("28nm B-A-N2CMAC FP-CIM 实测能效（论文 Fig. 14.3.6）\nBF16 62.84 TFLOPS/W（0.55-0.9V，ResNet50）· INT8 90.15 TOPS/W",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_energy.png"), bbox_inches="tight")
plt.close(fig)

# c02 面积/功耗收益
fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150)
cats = ["串行对齐\nvs 并行对齐[6]", "串行 MAC\nvs 并行 MAC[6]", "串行对齐\nvs 并行对齐[1,2]", "串行 MAC\nvs 并行 MAC[1,2]"]
area = [3.83, 1.56, 3.83, 1.56]
power = [1.71, 1.20, 1.71, 1.20]
x = range(4)
b1 = ax.bar([i-0.19 for i in x], area, width=0.36, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3, label="面积降低 (×)")
b2 = ax.bar([i+0.19 for i in x], power, width=0.36, color=GREEN, edgecolor="white", linewidth=1.5, zorder=3, label="功耗降低 (×)")
for i in x:
    ax.text(i-0.19, area[i]+0.08, f"{area[i]}×", ha="center", fontsize=11.5, fontweight="bold", color=BLUE)
    ax.text(i+0.19, power[i]+0.08, f"{power[i]}×", ha="center", fontsize=11.5, fontweight="bold", color=GREEN)
style_ax(ax)
ax.set_xticks(list(x)); ax.set_xticklabels(cats, fontsize=10.5)
ax.set_ylim(0, 4.6)
ax.set_ylabel("降低倍数 (×，越大越好)", fontsize=12.5, color=INK)
ax.set_title("串行对齐 + 串行 MAC 的面积/功耗收益（论文 Fig. 14.3.5 仿真）\n对齐电路本身另省 36.23% 面积（vs 减法器+桶形移位器）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
ax.legend(fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_improvements.png"), bbox_inches="tight")
plt.close(fig)

# c03 周期减少 + 稀疏性
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8), dpi=150)
ax = axes[0]
labels = ["8b 输入 (ViT)", "10b 输入 (ViT)"]
vals = [19.80, 16.50]
bars = ax.bar(labels, vals, color=PURPLE, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.6, f"-{v}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 25)
ax.set_ylabel("计算周期减少 (%)", fontsize=12, color=INK)
ax.set_title("N2CMAC 减少的计算周期\n（ViT DeiT-S @ImageNet）", fontsize=13, fontweight="bold", color=INK, pad=10)

ax = axes[1]
ax.bar(["2 的补码", "符号-数值"], [1.0, 1.83], color=[GRAY, GREEN], width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for x, v in zip([0, 1], [1.0, 1.83]):
    ax.text(x, v + 0.05, f"{v}×", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 2.3)
ax.set_ylabel("负 INT8 权重位级稀疏性 (×)", fontsize=12, color=INK)
ax.set_title("符号-数值格式的稀疏性提升\n（ResNet50，1.83×）", fontsize=13, fontweight="bold", color=INK, pad=10)
fig.suptitle("N2CMAC 与符号-数值格式的收益（论文 Fig. 14.3.5）", fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(os.path.join(OUT, "c03_cycles_sparsity.png"), bbox_inches="tight")
plt.close(fig)

print("paper01 charts done")
