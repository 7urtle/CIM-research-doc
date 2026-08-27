# -*- coding: utf-8 -*-
"""论文14数据图：宏级vs系统级能效 / FoM对比 / 特征图尺寸与工作负载"""
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

# ---------- c01 宏级 vs 系统级能效（本论文与 SOTA 对比，表 I 数据） ----------
works = ["本工作\n宏级", "本工作\n系统级", "Axelera\n[28] 宏级", "MediaTek\n[23] 系统级", "近似DIMC\n[15] 宏级"]
eff = [126.3, 24.28, 15, 23.2, 15.5]
cols = [GREEN, GREEN, BLUE, BLUE, RED]
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
bars = ax.bar(works, eff, color=cols, edgecolor="none", width=0.6)
for b, v in zip(bars, eff):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, "%.1f" % v, ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("能效（TOPS/W，4b MAC）")
ax.set_title("能效对比：宏级 vs 系统级（论文表 I + 摘要）")
ax.set_ylim(0, 145)
ax.grid(axis="y", alpha=0.3)
ax.axhline(24.28, color=GREEN, ls="--", alpha=0.5)
fig.text(0.5, 0.01, "注：能效口径不一（宏级仅 MAC、系统级含全部片内能耗）；Axelera 为 8b 宏级 15 TOPS/W，MediaTek 为 12b 系统级 23.2 TOPS/W", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c01_能效对比.png")); plt.close(fig)

# ---------- c02 FoM（存储密度×MAC密度）对比 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
fom = [0.64, 0.53, 0.40, 0.31, 0.25]
labels = ["本工作", "竞品A", "竞品B", "竞品C", "竞品D"]
bars = ax.bar(labels, fom, color=[GREEN, BLUE, BLUE, BLUE, BLUE], width=0.55)
for b, v in zip(bars, fom):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.01, "%.2f" % v, ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("FoM = (MB/mm²) × (#MAC/mm²)（归一化 K 单位）")
ax.set_title("面积利用率 FoM 对比：本工作高 20%（示意）")
ax.set_ylim(0, 0.75)
ax.grid(axis="y", alpha=0.3)
fig.text(0.5, 0.01, "注：竞品数值为示意（论文仅给出“20% 提升”结论）；本工作存储密度 508 kB/mm²、MAC 密度 1.27K/mm²", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c02_FoM对比.png")); plt.close(fig)

# ---------- c03 特征图尺寸 vs 能效/吞吐 + 工作负载能效 ----------
fig, ax1 = plt.subplots(figsize=(6.6, 4.4), dpi=150)
fm = np.array([4, 8, 12, 16, 24, 32, 48, 64])
eff_fm = np.array([6, 12, 18, 23, 28, 29, 29.2, 29.3])
thr = np.array([0.05, 0.12, 0.2, 0.28, 0.4, 0.42, 0.44, 0.45])
ax1.plot(fm, eff_fm, "o-", color=GREEN, lw=2.2, label="能效（TOPS/W）")
ax1.set_xlabel("特征图尺寸（×）"); ax1.set_ylabel("能效（TOPS/W）", color=GREEN)
ax1.tick_params(axis="y", labelcolor=GREEN)
ax1.set_ylim(0, 35); ax1.grid(alpha=0.3)
ax1.annotate("24 后趋于饱和（29 TOPS/W @ 0.42 TOPS）", xy=(24, 28), xytext=(28, 20),
             arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9)
ax2 = ax1.twinx()
ax2.plot(fm, thr, "s--", color=BLUE, lw=2, label="吞吐（TOPS）")
ax2.set_ylabel("吞吐（TOPS）", color=BLUE)
ax2.tick_params(axis="y", labelcolor=BLUE)
ax2.set_ylim(0, 0.5)
ax1.set_title("能效与吞吐 vs 特征图尺寸（论文 Fig.18，趋势示意）")
fig.text(0.5, 0.01, "注：曲线为趋势示意（依据论文 Fig.18：小图受时钟/静态能耗主导，24 后饱和）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c03_特征图尺寸.png")); plt.close(fig)

print("charts done")
