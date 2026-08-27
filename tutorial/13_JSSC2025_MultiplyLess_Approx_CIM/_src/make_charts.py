# -*- coding: utf-8 -*-
"""论文13数据图：位宽成本 / 能效-电压-位宽缩放 / 比较器误差率"""
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

# ---------- c01 面积-周期积 vs 位宽（示意，基于论文 Fig.2(b) 的定性描述） ----------
bits = np.arange(1, 9, 0.2)
area_cycle_parallel = bits ** 2            # 位并行：面积∝位宽²（乘法器展开）
area_cycle_serial = bits ** 2              # 位串行：周期∝位宽²
multiplyless = bits * 1.0                  # 本工作：线性
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
ax.plot(bits, area_cycle_parallel / area_cycle_parallel.max(), "-", color=RED, lw=2.2, label="位并行数字CIM（面积∝位宽²）")
ax.plot(bits, area_cycle_serial / area_cycle_serial.max(), "--", color=ORANGE, lw=2.2, label="位串行数字CIM（周期∝位宽²）")
ax.plot(bits, multiplyless / multiplyless.max(), "-", color=GREEN, lw=3, label="本工作 multiply-less（线性）")
ax.set_xlabel("位宽（bit）"); ax.set_ylabel("面积×周期（归一化）")
ax.set_title("面积-周期积 vs 位宽：乘法成本二次膨胀 vs 线性扩展（示意）")
ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.3)
ax.annotate("位宽↑ → 乘法器/周期 二次膨胀", xy=(8, 1.0), xytext=(4.2, 0.86),
            arrowprops=dict(arrowstyle="->", color=RED), color=RED, fontsize=9)
ax.annotate("本工作面积/能耗随位宽线性增长", xy=(8, 1.0), xytext=(4.6, 0.28),
            arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9)
fig.text(0.5, 0.01, "注：曲线为示意（定性趋势），依据论文 Fig.2(b) 关于二次增长成本的论述", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(os.path.join(OUT, "c01_面积周期积_位宽缩放.png")); plt.close(fig)

# ---------- c02 能效 vs 电压（8-bit，不同输入稀疏度；示意，论文 Fig.15(b) 描述 102 TOPS/W 峰值） ----------
v = np.array([0.54, 0.6, 0.66, 0.72, 0.8, 0.9])
eff_sparse = np.array([102, 82, 66, 54, 42, 30])   # 10%输入稀疏+50%权重稀疏（峰值）
eff_dense = np.array([60, 50, 42, 35, 28, 20])     # 高输入稀疏度（示意，趋势）
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
ax.plot(v, eff_sparse, "o-", color=GREEN, lw=2.4, label="10% 输入稀疏 + 50% 权重稀疏")
ax.plot(v, eff_dense, "s--", color=BLUE, lw=2.0, label="高输入稀疏度（示意趋势）")
ax.set_xlabel("电压（V）"); ax.set_ylabel("能效（TOPS/W）")
ax.set_title("8-bit 能效 vs 电压缩放（0.54–0.9 V）")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
ax.annotate("峰值 102 TOPS/W\n@0.54V / 20MHz", xy=(0.54, 102), xytext=(0.60, 92),
            arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9.5, fontweight="bold")
fig.text(0.5, 0.01, "注：102 TOPS/W 为论文实测峰值（0.54V/20MHz/10%输入稀疏/50%权重稀疏）；其余点为趋势示意", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(os.path.join(OUT, "c02_能效_电压缩放.png")); plt.close(fig)

# ---------- c03 比较器误差率 vs 高-高对数（改进 vs [19]；示意，论文 Fig.17 描述） ----------
n_high = np.arange(0, 11, 1)
err_old = np.where(n_high < 2, 0, np.clip((n_high - 2) * 14, 0, 100))      # [19] 从2个开始
err_new = np.where(n_high < 6, 0, np.clip((n_high - 6) * 22, 0, 100))      # 改进从6个开始
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
ax.plot(n_high, err_old, "o-", color=RED, lw=2.2, label="原比较器 [19]（从 2 个高-高对出错）")
ax.plot(n_high, err_new, "s-", color=GREEN, lw=2.4, label="改进比较器（从 6 个高-高对出错）")
ax.axvline(2, color=RED, ls=":", alpha=0.6); ax.axvline(6, color=GREEN, ls=":", alpha=0.6)
ax.set_xlabel("连续高-高（ACT=W=1）比较次数"); ax.set_ylabel("比较误差率（%，示意）")
ax.set_title("动态比较器误差率：改进设计延迟电荷共享失效（0.54 V）")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.text(0.5, 0.01, "注：曲线为示意（趋势依据论文 Fig.13/17 的定量描述：误差从 3 次[旧]与 6 次[新]比较后出现；0.65V 以上无误差）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(os.path.join(OUT, "c03_比较器误差率.png")); plt.close(fig)

print("charts done")
