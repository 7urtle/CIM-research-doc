# -*- coding: utf-8 -*-
"""论文15数据图：数据格式对比 / 三招能效提升 / 与SOTA对比"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "charts")
os.makedirs(OUT, exist_ok=True)

BLUE, GREEN, ORANGE, RED, PURPLE, GRAY = "#1e6fa8", "#1d8a5f", "#e08a1e", "#d9534f", "#7a5fa8", "#8a97a5"

# ---------- c01 数据格式精度-能耗对比 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
labels = ["FP32", "FP16", "BF16", "FP8", "POSIT8"]
rel_err = [0.0, 0.05, 0.08, 1.2, 0.15]     # 相对精度损失（示意，ViT-B 口径）
rel_energy = [4.0, 1.0, 1.0, 0.16, 0.16]  # 相对能耗（FP16=1）
x = np.arange(len(labels))
bars = ax.bar(x - 0.18, rel_err, width=0.34, color=BLUE, label="精度损失（%，示意）")
ax.bar(x + 0.18, rel_energy, width=0.34, color=GREEN, label="相对能耗（FP16=1）")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("数值")
ax.set_title("数据格式对比：POSIT8 用 FP8 的能耗达到 ≈FP16 的精度")
ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3)
for b, v in zip(bars, rel_err):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.03, "%.2f" % v, ha="center", fontsize=8)
fig.text(0.5, 0.01, "注：数值为示意（依据论文：POSIT8 精度差<0.4% vs FP16、能耗省 6.25× vs FP16；FP8 在梯度范围不足时掉精度）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c01_数据格式对比.png")); plt.close(fig)

# ---------- c02 三招贡献分解 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
stages = ["基线\nPOSIT8-CIM", "+BRPU", "+CPCS", "+CASU\n(PD-CIM)"]
eff = [3.0, 4.5, 6.9, 13.23]   # POSIT16 系统能效演进（示意，论文 Fig.18：最终 13.23→27.61 口径取系统级）
bars = ax.bar(stages, eff, color=[GRAY, BLUE, ORANGE, GREEN], width=0.55)
for b, v in zip(bars, eff):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.2, "%.1f" % v, ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("系统能效（TFLOPS/W，POSIT16）")
ax.set_title("三招逐步叠加的能效提升（示意）")
ax.set_ylim(0, 15)
ax.grid(axis="y", alpha=0.3)
ax.annotate("BRPU 1.94×\n（regime 处理）", xy=(1, 4.5), xytext=(0.2, 6.5),
            arrowprops=dict(arrowstyle="->", color=BLUE), color=BLUE, fontsize=9)
ax.annotate("CPCS 双位 MAC\n（单元利用）", xy=(2, 6.9), xytext=(1.2, 9.5),
            arrowprops=dict(arrowstyle="->", color=ORANGE), color=ORANGE, fontsize=9)
ax.annotate("CASU OR 累加\n（加法树）", xy=(3, 13.23), xytext=(2.2, 12.0),
            arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9)
fig.text(0.5, 0.01, "注：曲线为趋势示意（依据论文：三招对 ResNet18 训练 POSIT16 系统能效 3.48→27.61 TFLOPS/W，此处为简化演进）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c02_三招贡献.png")); plt.close(fig)

# ---------- c03 与 SOTA 对比 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
works = ["PD-CIM\n(本工作)", "FP-CIM\n[15]", "FP-CIM\n[16]", "FP-CIM\n[17]"]
eff = [83.23, 41.5, 32.0, 33.8]
bars = ax.bar(works, eff, color=[GREEN, BLUE, BLUE, BLUE], width=0.55)
for b, v in zip(bars, eff):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, "%.1f" % v, ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("峰值能效（TFLOPS/W）")
ax.set_title("与 SOTA FP-CIM 对比（论文表 III）")
ax.set_ylim(0, 95)
ax.grid(axis="y", alpha=0.3)
ax.annotate("能效超 [15] 2.36× · 加速 3.51×", xy=(0, 83.23), xytext=(0.7, 78),
            arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=10)
fig.text(0.5, 0.01, "注：[16]/[17] 数值为近似（论文给出同精度下 PD-CIM 超 [16] 2.6×、超 [17] 2.46× 的结论）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c03_SOTA对比.png")); plt.close(fig)

print("charts done")
