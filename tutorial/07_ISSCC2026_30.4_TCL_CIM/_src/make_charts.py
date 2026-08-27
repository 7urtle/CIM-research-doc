# -*- coding: utf-8 -*-
"""论文07教学图：能效 / FoM / MAC cell FoM"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\07_ISSCC2026_30.4_TCL_CIM\assets\charts"
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
labels = ["INT8", "BF16"]
vals = [106.85, 77.68]
colors = [BLUE, PURPLE]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 2, f"{v} TOPS/W" if v > 90 else f"{v} TFLOPS/W", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 125)
ax.set_ylabel("能效 (TOPS/W 或 TFLOPS/W)", fontsize=12.5, color=INK)
ax.set_title("28nm TCL-CIM 实测能效（论文 Fig. 30.4.6）\nINT8 106.85 TOPS/W · BF16 77.68 TFLOPS/W（90% 输入稀疏、10% 翻转率、50% 权重稀疏）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_energy.png"), bbox_inches="tight")
plt.close(fig)

# c02 FoM 提升
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
foms = ["FoM1\n精度×TOPS/W×TOPS/mm²\nvs 前作有符号 CIM [2,3,6,7]", "FoM2\nTFLOPS/W×TFLOPS/mm²\nvs 前作 [2,3,6,7]"]
lo, hi = [1.25, 2.2], [2.88, 19.9]
x = [0, 1]
for i in x:
    ax.bar(i - 0.18, lo[i], width=0.36, color=GRAY, edgecolor="white", linewidth=1.5, zorder=3)
    ax.bar(i + 0.18, hi[i], width=0.36, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3)
    ax.text(i - 0.18, lo[i] + 0.3, f"{lo[i]}×", ha="center", fontsize=12, fontweight="bold", color=INK)
    ax.text(i + 0.18, hi[i] + 0.3, f"{hi[i]}×", ha="center", fontsize=12, fontweight="bold", color=INK)
style_ax(ax)
ax.set_xticks(x); ax.set_xticklabels(foms, fontsize=11)
ax.set_ylim(0, 23)
ax.set_ylabel("提升倍数 (×)", fontsize=12.5, color=INK)
ax.set_title("FoM 相对前作有符号 CIM 的提升（论文 Fig. 30.4.6 对比表）\n灰=下限 · 蓝=上限（对比对象跨度的反映）", fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_fom.png"), bbox_inches="tight")
plt.close(fig)

# c03 MAC cell FoM（能效/晶体管数）
fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150)
labels = ["标准数字压缩器", "模拟乘法+3b ADC\n压缩 [5]", "4b 位并行 MAC\n+ 行波进位 [6]", "本论文 TCL"]
vals = [1.0, 1.0, 1.0, 1.87]  # 归一化：论文 FoM 提升 1.66~1.87×，取上限示意
colors = [GRAY, GRAY, GRAY, GREEN]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.05, f"{v}×", ha="center", fontsize=13, fontweight="bold", color=v > 1.5 and GREEN or INK)
style_ax(ax)
ax.set_ylim(0, 2.3)
ax.set_ylabel("MAC cell FoM（能效/晶体管数，归一化）", fontsize=12, color=INK)
ax.set_title("8b 位并行 MAC 单元的 FoM 对比（论文 Fig. 30.4.5 仿真）\nTCL 以最少晶体管实现位列加法 → FoM 提升 1.66~1.87×（此处示 1.87×）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_tcl_fom.png"), bbox_inches="tight")
plt.close(fig)

print("paper07 charts done")
