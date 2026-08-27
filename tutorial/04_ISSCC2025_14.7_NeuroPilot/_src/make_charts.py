# -*- coding: utf-8 -*-
"""论文04教学图：核心指标 / DDS 收益 / TsCFP 大图"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\04_ISSCC2025_14.7_NeuroPilot\assets\charts"
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

# c01 核心指标
fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.6), dpi=150)
ax = axes[0]
ax.bar(["搜索率"], [3670], color=BLUE, width=0.4, edgecolor="white", linewidth=1.5, zorder=3)
ax.text(0, 3670 + 80, "3670M", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 4200)
ax.set_ylabel("M nodes/s", fontsize=12, color=INK)
ax.set_title("搜索率", fontsize=13, fontweight="bold", color=INK, pad=8)

ax = axes[1]
ax.bar(["单节点能量"], [69.4], color=GREEN, width=0.4, edgecolor="white", linewidth=1.5, zorder=3)
ax.text(0, 69.4 + 2, "69.4 fJ", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 85)
ax.set_ylabel("fJ / node", fontsize=12, color=INK)
ax.set_title("单节点能量", fontsize=13, fontweight="bold", color=INK, pad=8)

ax = axes[2]
ax.bar(["PE 面积"], [213.6], color=ORANGE, width=0.4, edgecolor="white", linewidth=1.5, zorder=3)
ax.text(0, 213.6 + 6, "213.6 μm²", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 260)
ax.set_ylabel("μm²", fontsize=12, color=INK)
ax.set_title("PE 面积（14.5×14.7）", fontsize=13, fontweight="bold", color=INK, pad=8)

fig.suptitle("NeuroPilot 核心指标（论文 Fig. 14.7.6）· 28nm 32×32", fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.9])
fig.savefig(os.path.join(OUT, "c01_metrics.png"), bbox_inches="tight")
plt.close(fig)

# c02 DDS vs SDS
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8), dpi=150)
ax = axes[0]
labels = ["SDS", "DDS"]
vals = [2.1, 1.0]
bars = ax.bar(labels, vals, color=[GRAY, GREEN], width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.06, f"{v}×", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 2.6)
ax.set_ylabel("处理时间（归一化，越小越好）", fontsize=12, color=INK)
ax.set_title("DDS：处理时间 −2.1×", fontsize=13, fontweight="bold", color=INK, pad=10)

ax = axes[1]
labels2 = ["SDS", "DDS"]
vals2 = [1.13, 1.0]
bars = ax.bar(labels2, vals2, color=[GRAY, BLUE], width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals2):
    ax.text(b.get_x()+b.get_width()/2, v + 0.03, f"{v}×", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 1.4)
ax.set_ylabel("功耗（归一化，越小越好）", fontsize=12, color=INK)
ax.set_title("DDS：功耗 −1.13×", fontsize=13, fontweight="bold", color=INK, pad=10)
fig.suptitle("双向搜索（DDS）vs 单向搜索（SDS）· 例图（论文 Fig. 14.7.2）", fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.9])
fig.savefig(os.path.join(OUT, "c02_dds.png"), bbox_inches="tight")
plt.close(fig)

# c03 TsCFP 大图
fig, ax = plt.subplots(figsize=(9.0, 5.0), dpi=150)
labels = ["求解时间 (ns)", "能耗 (pJ)", "路径长度 (L)"]
vals = [373.82, 512.5, 1279.8]
bars = ax.bar(labels, vals, color=[BLUE, GREEN, ORANGE], width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 20, f"{v}", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 1500)
ax.set_ylabel("数值", fontsize=12, color=INK)
ax.set_title("TsCFP 三步粗/细路径 · 旧金山 1024×1024 地图（论文 Fig. 14.7.5）\n373.82ns 求解 · 512.5pJ · 1279.8L 路径",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_tscfp.png"), bbox_inches="tight")
plt.close(fig)

print("paper04 charts done")
