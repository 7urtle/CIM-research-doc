# -*- coding: utf-8 -*-
"""论文05教学图：精度 / MRAM 收益 / 对比"""
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

OUT = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\05_ISSCC2026_18.4_SpikeRAM\assets\charts"
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

# c01 精度
fig, ax = plt.subplots(figsize=(9.0, 5.0), dpi=150)
labels = ["NMNIST", "DVS Gesture", "DailyDVS", "EHSV 签名\n(2-shot)"]
vals = [96.4, 92.9, 90.5, 94.3]
colors = [BLUE, GREEN, PURPLE, ORANGE]
bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 0.8, f"{v}%", ha="center", fontsize=13, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 110)
ax.set_ylabel("精度 (%)", fontsize=13, color=INK)
ax.set_title("SpikeRAM 各任务精度（论文 Fig. 18.4.5）\n全部仅 1 个 OCL epoch、随机初始化；EHSV 为 2-shot 在线学习",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c01_accuracy.png"), bbox_inches="tight")
plt.close(fig)

# c02 MRAM 收益
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8), dpi=150)
ax = axes[0]
labels = ["NMNIST\n编程次数", "DVS Gesture\n编程次数", "最大被写器件数", "每样本总写时间"]
vals = [89.1, 88.4, 92.8, 86.3]
bars = ax.bar(labels, vals, color=GREEN, width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v + 1.5, f"-{v}%", ha="center", fontsize=12, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 108)
ax.set_ylabel("减少 (%)", fontsize=12, color=INK)
ax.set_title("MRAM 写操作减少（论文 Fig. 18.4.5 底部）", fontsize=13, fontweight="bold", color=INK, pad=10)

ax = axes[1]
labels2 = ["更新次数均值\n(DVS)", "更新次数标准差\n(DVS)", "MRAM 寿命"]
vals2 = [10.9, 35.6, 13.9]
bars = ax.bar(labels2, vals2, color=[BLUE, PURPLE, RED], width=0.5, edgecolor="white", linewidth=1.5, zorder=3)
for b, v in zip(bars, vals2):
    ax.text(b.get_x()+b.get_width()/2, v + 0.5, f"{v}×", ha="center", fontsize=12.5, fontweight="bold", color=INK)
style_ax(ax)
ax.set_ylim(0, 42)
ax.set_ylabel("倍数 (×)", fontsize=12, color=INK)
ax.set_title("写压力与寿命（前两项为减少倍数，寿命为延长倍数）", fontsize=13, fontweight="bold", color=INK, pad=10)
fig.suptitle("三值梯度 + 格雷码 + e-OTBP 的 eNVM 收益", fontsize=14, fontweight="bold", color=INK)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(os.path.join(OUT, "c02_mram.png"), bbox_inches="tight")
plt.close(fig)

# c03 对比
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=150)
labels = ["功率密度\n(pW/Synapse/Bit)", "网络密度\n(Synapse/Byte)"]
ours = [48.1, 441.9]
prior = [48.1 * 2.7, 441.9 / 24.3]
x = [0, 1]
b1 = ax.bar([i-0.19 for i in x], prior, width=0.36, color=GRAY, edgecolor="white", linewidth=1.5, zorder=3, label="前作（归一化基准）")
b2 = ax.bar([i+0.19 for i in x], ours, width=0.36, color=BLUE, edgecolor="white", linewidth=1.5, zorder=3, label="SpikeRAM")
for i in x:
    ax.text(i-0.19, prior[i] + 5, f"{prior[i]:.1f}", ha="center", fontsize=11, color=INK)
    ax.text(i+0.19, ours[i] + 5, f"{ours[i]:.1f}", ha="center", fontsize=11, fontweight="bold", color=BLUE)
style_ax(ax)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=12)
ax.set_yscale("log")
ax.set_ylim(1, 2000)
ax.set_ylabel("数值（对数轴）", fontsize=12, color=INK)
ax.set_title("与神经形态处理器对比（论文 Fig. 18.4.6）\n功率密度 2.7×、网络密度 24.3× 优于前作（前作数值为按倍数反推）",
             fontsize=13.5, fontweight="bold", color=INK, pad=12)
ax.legend(fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "c03_compare.png"), bbox_inches="tight")
plt.close(fig)

print("paper05 charts done")
