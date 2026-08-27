# -*- coding: utf-8 -*-
"""论文02教学图：能效 / SER / 稀疏加速"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\02_ISSCC2025_14.4_CompoundAI_CIM\assets\charts"
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
labels = ["峰值能效\n（全技术）", "复合模型部署\n（平均范围）", "基础峰值\n（不含稀疏单元）"]
vals = [51.6, 9.05, 16.2]
colors = [GREEN, BLUE, GRAY]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 1.2, f"{v}", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 60)
ax.set_ylabel("能效 (TFLOPS/W)", fontsize=12.5, color=INK)
ax.set_title("28nm 异质 CIM 宏能效（论文 Fig. 14.4.6）\n峰值 51.6 TFLOPS/W · 复合模型平均 5.55~12.54 · 基础 16.2 TFLOPS/W（复合模型为范围中值示意）",
             fontsize=13, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_energy.png"), bbox_inches="tight")
plt.close(fig)

# c02 SER
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["前作 FP-CIM\n(预对齐)", "本论文\n(后乘积对齐)"]
vals = [60.1 / 3.14, 60.1]
colors = [GRAY, GREEN]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 1.5, f"{v:.1f} dB", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 75)
ax.set_ylabel("SER (dB，越大越好)", fontsize=13, color=INK)
ax.set_title("信号误差比 SER（论文 Fig. 14.4.3）\n60.1 dB = 前作的 3.14×；FP16-MAC 最大误差 < 2⁻³⁰（前作 2⁻¹）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_ser.png"), bbox_inches="tight")
plt.close(fig)

# c03 稀疏加速
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["静态 2:4\n(NIM)", "动态 Booth 池\n(启动器)", "合计\n(本宏)", "稀疏理论上限\n(1/稀疏度)"]
vals = [2.0, 2.65, 5.30, 5.72]
colors = [BLUE, PURPLE, GREEN, GRAY]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.12, f"{v}×", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 6.8)
ax.set_ylabel("加速倍数 (×)", fontsize=13, color=INK)
ax.set_title("静态+动态稀疏加速（论文 Fig. 14.4.5）\n合计 5.30× ≈ 理论上限的 92.6%（理论上限 1/稀疏度，此处示 5.72×）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_sparsity.png"), bbox_inches="tight")
plt.close(fig)

print("paper02 charts done")
