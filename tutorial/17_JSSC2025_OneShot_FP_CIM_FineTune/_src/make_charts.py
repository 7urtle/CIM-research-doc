# -*- coding: utf-8 -*-
"""论文17数据图：one-shot吞吐 / ParMS收益 / SOTA对比"""
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

# ---------- c01 one-shot 周期对比 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
steps = ["步骤①\nXE_max 选择", "步骤②\n输入对齐", "步骤③\n尾数 MAC", "步骤④\nINT→FP"]
cyc_trad = [1, 1, 8, 1]
cyc_new = [0, 1, 1, 1]
x = np.arange(4)
bars1 = ax.bar(x - 0.18, cyc_trad, width=0.34, color=RED, label="传统预对齐 FP-CIM")
bars2 = ax.bar(x + 0.18, cyc_new, width=0.34, color=GREEN, label="One-Shot（本论文）")
for b, v in zip(bars1, cyc_trad): ax.text(b.get_x() + b.get_width() / 2, v + 0.1, str(v), ha="center", fontsize=10)
for b, v in zip(bars2, cyc_new): ax.text(b.get_x() + b.get_width() / 2, v + 0.1, str(v), ha="center", fontsize=10)
ax.set_xticks(x); ax.set_xticklabels(steps)
ax.set_ylabel("周期数（BF16）")
ax.set_title("One-Shot 计算：总周期 11 → 3（流水 1 周期/级）")
ax.set_ylim(0, 10)
ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3)
ax.annotate("步骤①被协同对齐消除", xy=(0, 0.5), xytext=(0.4, 6.5), arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9.5)
ax.annotate("最小选择 1 周期\n（原 8 周期位串行）", xy=(2, 1.2), xytext=(1.6, 5.2), arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9.5)
fig.text(0.5, 0.01, "注：依据论文 Fig.4（BF16：传统步③ 8 周期；本论文每级 1 周期，吞吐 +8×）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c01_one_shot.png")); plt.close(fig)

# ---------- c02 ParMS 收益 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
comps = ["INT8 乘法器", "综合数字比较器", "[14] 动态逻辑比较器"]
area_reduce = [11.5, 1.14, 1.0]   # 面积倍数（归一化：越大省越多）
energy_reduce = [8.2, 4.1, 1.5]   # 能耗倍数
x = np.arange(3)
bars1 = ax.bar(x - 0.18, area_reduce, width=0.34, color=BLUE, label="面积节省倍数")
bars2 = ax.bar(x + 0.18, energy_reduce, width=0.34, color=GREEN, label="能耗节省倍数")
for b, v in zip(bars1, area_reduce): ax.text(b.get_x() + b.get_width() / 2, v + 0.15, "×%.1f" % v, ha="center", fontsize=9.5)
for b, v in zip(bars2, energy_reduce): ax.text(b.get_x() + b.get_width() / 2, v + 0.15, "×%.1f" % v, ha="center", fontsize=9.5)
ax.set_xticks(x); ax.set_xticklabels(comps)
ax.set_ylabel("ParMS 相对节省倍数")
ax.set_title("ParMS vs 各类比较/乘法方案（论文 Fig.6）")
ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3)
ax.set_ylim(0, 13)
fig.text(0.5, 0.01, "注：[14] 动态逻辑比较器在稀疏度升高时 ParMS 优势更大（全静态逻辑利用 NN 稀疏）；数值为论文给出口径", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c02_ParMS.png")); plt.close(fig)

# ---------- c03 与 SOTA 对比 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
works = ["本工作\n(BF16)", "FP-CIM\n[21]", "FP-CIM\n[22]", "multiply-less\nCIM [14]"]
eff = [128, 31.2, 8.0, 102]    # TFLOPS/W（[14] 为 INT8 102 TOPS/W 参考）
area = [7.02, 1.95, 0.35, 1.0] # TFLOPS/mm²（示意）
x = np.arange(4)
ax2 = ax.twinx()
bars1 = ax.bar(x - 0.18, eff, width=0.34, color=GREEN, label="能效（TFLOPS/W）")
bars2 = ax2.bar(x + 0.18, area, width=0.34, color=BLUE, label="面积效率（TFLOPS/mm²）")
for b, v in zip(bars1, eff): ax.text(b.get_x() + b.get_width() / 2, v + 2, "%.0f" % v, ha="center", fontsize=9.5, fontweight="bold")
for b, v in zip(bars2, area): ax2.text(b.get_x() + b.get_width() / 2, v + 0.1, "%.2f" % v, ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(works)
ax.set_ylabel("能效（TFLOPS/W）", color=GREEN); ax.tick_params(axis="y", labelcolor=GREEN)
ax2.set_ylabel("面积效率（TFLOPS/mm²）", color=BLUE); ax2.tick_params(axis="y", labelcolor=BLUE)
ax.set_ylim(0, 150); ax2.set_ylim(0, 8)
ax.set_title("与 SOTA 对比：能效 4.1×、面积效率 3.6×（论文表 V）")
ax.grid(axis="y", alpha=0.3)
fig.text(0.5, 0.01, "注：[21]/[22] 数值为示意（论文给出 4.1×/3.6× 提升结论）；[14] 为前作 INT 版本参考", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c03_SOTA.png")); plt.close(fig)

print("charts done")
