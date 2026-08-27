# -*- coding: utf-8 -*-
"""论文16数据图：T值对比 / 开销分解 / 性能对比"""
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

# ---------- c01 DPA T值 vs 采样数（保护 vs 未保护） ----------
samples = np.logspace(2, 6.5, 40)
t_unprot = np.clip(1.5 * (samples / 100) ** 0.55, 0, 30)   # 未保护：5000 样本即显著（>4.5）
t_prot = np.clip(0.15 + 0.05 * np.log10(samples), 0, 2.5)  # 保护：100 万样本仍小
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
ax.semilogx(samples, t_unprot, "-", color=RED, lw=2.4, label="未保护（T 值快速上升）")
ax.semilogx(samples, t_prot, "-", color=GREEN, lw=2.4, label="保护（Boolean 共享）")
ax.axhline(4.5, color=GRAY, ls="--", lw=1.2)
ax.text(1e6, 5.2, "显著性阈值（|T|&gt;4.5）", color=GRAY, fontsize=9, ha="right")
ax.annotate("未保护 &lt;5000 样本即显著", xy=(5000, 7), xytext=(120, 16),
            arrowprops=dict(arrowstyle="->", color=RED), color=RED, fontsize=9.5)
ax.annotate("保护 100 万样本仍安全", xy=(1e6, 0.6), xytext=(2e4, 3.2),
            arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9.5)
ax.set_xlabel("攻击采样数"); ax.set_ylabel("|T| 值（Welch t-test）")
ax.set_title("DPA/TVLA：保护 vs 未保护（示意，依据论文 Fig.11）")
ax.set_xlim(1e2, 3e6); ax.set_ylim(0, 18)
ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.3)
fig.text(0.5, 0.01, "注：曲线为趋势示意（论文：未保护 5000 样本 T 值大、保护 100 万样本 T 值小）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c01_DPA对比.png")); plt.close(fig)

# ---------- c02 面积开销分解 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
comps = ["位单元+乘法列", "加法树（全加器）", "加法器+累加器"]
ovh = [5.3, 15.5, 6.4]
bars = ax.bar(comps, ovh, color=[BLUE, ORANGE, PURPLE], width=0.5)
for b, v in zip(bars, ovh):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.3, "×%.1f" % v, ha="center", fontsize=11, fontweight="bold")
ax.set_ylabel("面积开销倍数（vs 未保护）")
ax.set_title("Boolean 共享的面积开销（论文 §IV-C，示意）")
ax.set_ylim(0, 18)
ax.grid(axis="y", alpha=0.3)
fig.text(0.5, 0.01, "注：位单元 ×5.3（3 份共享+2 个 PUF 晶体管）；全加器 ×14.2→加法树 ×15.5；与 [30] 的 6.1×/5.7× 一致", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c02_面积开销.png")); plt.close(fig)

# ---------- c03 性能对比（表 V 未保护 vs 保护） ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
labels = ["未保护", "保护（本论文）"]
eff = [14.0, 8.1]   # TOPS/W（示意：保护后 8.1 实测）
area = [1.0, 0.19]  # 面积效率归一化（1/5.3 附近，示意）
x = np.arange(2)
bars1 = ax.bar(x - 0.18, eff, width=0.34, color=GREEN, label="能效（TOPS/W）")
ax2 = ax.twinx()
bars2 = ax2.bar(x + 0.18, area, width=0.34, color=BLUE, label="面积效率（归一化）")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("能效（TOPS/W）", color=GREEN); ax.tick_params(axis="y", labelcolor=GREEN)
ax2.set_ylabel("面积效率（归一化）", color=BLUE); ax2.tick_params(axis="y", labelcolor=BLUE)
ax.set_ylim(0, 18); ax2.set_ylim(0, 1.4)
ax.set_title("安全开销：能效 8.1 TOPS/W、面积效率下降（示意，论文表 V/Fig.13）")
ax.grid(axis="y", alpha=0.3)
for b, v in zip(bars1, eff): ax.text(b.get_x() + b.get_width() / 2, v + 0.3, "%.1f" % v, ha="center", fontsize=10, fontweight="bold")
fig.text(0.5, 0.01, "注：能效 8.1 TOPS/W 为论文实测；面积效率为归一化示意（加法树/累加器 −6.4× 等）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c03_性能开销.png")); plt.close(fig)

print("charts done")
