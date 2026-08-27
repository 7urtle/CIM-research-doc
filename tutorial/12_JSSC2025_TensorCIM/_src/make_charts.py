# -*- coding: utf-8 -*-
"""论文12教学图：能效 / 技术分解 / 利用率"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\12_JSSC2025_TensorCIM\assets\charts"
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
labels = ["INT8", "INT16", "FP32"]
vals = [85.0, 14.2, 8.3]
colors = [BLUE, PURPLE, GREEN]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.5, f"{v}", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 95)
ax.set_ylabel("峰值代数能效 (TOPS/W 或 TFLOPS/W)", fontsize=12, color=INK)
ax.set_title("TensorCIM 峰值代数能效（论文 Table IV）\n0.65V/175MHz，稀疏 GCN Pubmed：85.0 TOPS/W(INT8) · 8.3 TFLOPS/W(FP32)",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_energy.png"), bbox_inches="tight")
plt.close(fig)

# c02 技术分解（能耗节省）
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["SpG 优化\n(REGM)", "SpA 优化\n(EOCI+ILA)", "总模型\nGCN", "总模型\nDLRM"]
vals = [3.55, 5.95, 4.58, 3.52]
colors = [BLUE, PURPLE, GREEN, ORANGE]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.12, f"{v}×", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 7.2)
ax.set_ylabel("能耗节省 (×)", fontsize=13, color=INK)
ax.set_title("技术分解：各项优化的能耗节省（论文 Fig. 23）\nGCN 总省 4.58×、DLRM 总省 3.52×（0.65V/175MHz）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c02_breakdown.png"), bbox_inches="tight")
plt.close(fig)

# c03 利用率提升
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["基线\n(无优化)", "ILA-CIM\n(单独)", "EOCI+ILA-CIM\n(联合)"]
vals = [17.6, 33.2, 95.4]
colors = [GRAY, BLUE, GREEN]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 2, f"{v}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 110)
ax.set_ylabel("宏内利用率 (%)", fontsize=13, color=INK)
ax.set_title("宏内利用率提升（论文 Fig. 19）\n17.6% → 33.2%（ILA）→ 95.4%（联合）· 总加速 5.28×",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_utilization.png"), bbox_inches="tight")
plt.close(fig)

print("paper12 charts done")
