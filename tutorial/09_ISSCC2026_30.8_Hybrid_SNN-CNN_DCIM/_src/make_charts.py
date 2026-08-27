# -*- coding: utf-8 -*-
"""论文09教学图：能效对比 / FoM 提升 / 面积-能效收益"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\09_ISSCC2026_30.8_Hybrid_SNN-CNN_DCIM\assets\charts"
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

# c01 两种模式能效
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["SNN 模式\n1bIN-8bW-14bOUT", "CNN 模式\n8bIN-8bW-22bOUT"]
vals = [444.21, 62.84]
colors = [BLUE, RED]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 8, f"{v} TOPS/W", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 520)
ax.set_ylabel("能效 (TOPS/W)", fontsize=13, color=INK)
ax.set_title("同一宏的两种模式能效（16nm 实测，论文 Fig. 30.8.6）\nSNN 模式 1b 脉冲输入极其稀疏 → 能效高 7 倍",
             fontsize=14, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_modes.png"), bbox_inches="tight")
plt.close(fig)

# c02 FoM 提升
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
foms = ["FoM1\n能效/(面积×延迟)\nvs 两种极端映射", "FoM2\n精度×能效/(面积×延迟)\nvs 基线[4,10]", "FoM3\nIN精度×W精度×能效\nvs 近期工作"]
vals = [1.22, 5.48, 8.2]
colors = [PURPLE, BLUE, GREEN]
bars = ax.bar(foms, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.12, f"{v}×", ha="center", fontsize=14, fontweight="bold", color=INK)
style_ax(ax)
ax.axhline(1, color=GRAY, linestyle="--", linewidth=1.2)
ax.text(2.45, 1.12, "基线 = 1×", color=GRAY, fontsize=10.5, ha="center")
ax.set_ylim(0, 9.5)
ax.set_ylabel("相对提升 (×)", fontsize=13, color=INK)
ax.set_title("三个 FoM 的量化收益（论文 Fig. 30.8.5 仿真数据）\nFoM1 为 PS-WR-ODM 相对两种极端映射；FoM2/FoM3 为全方案综合收益",
             fontsize=14, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_fom.png"), bbox_inches="tight")
plt.close(fig)

# c03 面积/能效对比 vs 前作
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
cats = ["宏面积 (越小越好)", "能效 (越大越好)"]
baseline = [1.0, 1.0]
thiswork = [0.67, 2.31]
x = [0, 1]
b1 = ax.bar([i-0.19 for i in x], baseline, width=0.36, color=GRAY, edgecolor="white", linewidth=1.5, zorder=3, label="前作混合 SNN-CNN CIM [4]（归一化）")
b2 = ax.bar([i+0.19 for i in x], thiswork, width=0.36, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3, label="本论文 CFD-SC-RC")
for i, (bv, tv) in enumerate(zip(baseline, thiswork)):
    ax.text(i-0.19, bv+0.05, "1.0×", ha="center", fontsize=12, fontweight="bold", color=INK)
    ax.text(i+0.19, tv+0.05, f"{tv}×", ha="center", fontsize=12, fontweight="bold", color=INK)
ax.text(0, 0.52, "面积 -33%", ha="center", fontsize=12, color=RED, fontweight="bold")
ax.text(1, 1.9, "能效 2.31×", ha="center", fontsize=12, color=GREEN, fontweight="bold")
style_ax(ax)
ax.set_xticks(x)
ax.set_xticklabels(cats, fontsize=13)
ax.set_ylim(0, 2.9)
ax.set_ylabel("归一化数值 (×)", fontsize=13, color=INK)
ax.set_title("CFD-SC-RC 硬件共享的收益（论文 Fig. 30.8.5）\n同一套 MAC 电路服务 SNN 与 CNN → 面积 -33%、能效 2.31×",
             fontsize=14, fontweight="bold", color=INK, pad=12)
ax.legend(fontsize=11, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_area_energy.png"), bbox_inches="tight")
plt.close(fig)

print("paper09 charts done")
