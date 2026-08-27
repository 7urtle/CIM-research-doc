# -*- coding: utf-8 -*-
"""论文18数据图：流长成本 / 能效对比 / 电压能效"""
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

# ---------- c01 精度 vs 求值次数（SC 指数 vs 定点/模拟 CIM 平方） ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
prec = np.arange(1, 9)
sc_ops = 2 ** prec                       # SC: 2^N
cim_ops = prec ** 2                      # CIM: N^2
ax.plot(prec, sc_ops, "o-", color=ORANGE, lw=2.2, label="SC（流长 2^N，指数）")
ax.plot(prec, cim_ops, "s--", color=BLUE, lw=2.0, label="ADC 位串行 CIM（N^2，平方）")
ax.set_xlabel("精度（bit）"); ax.set_ylabel("1-bit 求值次数（MAC 评估）")
ax.set_title("SC 的指数流长 vs CIM 的平方成本（论文 Fig.8）")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
ax.annotate("<=4-bit 两者相当（4^2=2^4=16）", xy=(4, 16), xytext=(1.5, 30),
            arrowprops=dict(arrowstyle="->", color=GRAY), color=GRAY, fontsize=9)
ax.annotate("8-bit：SC 256 次\n= CIM 的 4×", xy=(8, 256), xytext=(5.4, 180),
            arrowprops=dict(arrowstyle="->", color=RED), color=RED, fontsize=9.5, fontweight="bold")
fig.text(0.5, 0.01, "注：依据论文 Fig.8 的对比（8-bit SC 需 256 次 vs CIM 64 次；平均池化跳算缩短 4×）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c01_流长成本.png")); plt.close(fig)

# ---------- c02 能效对比（1-bit 与 8-bit） ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
labels = ["1-bit", "8-bit", "8-bit + 平均池化"]
scim_vs_analog = [6.0, 1.6, 6.4]
scim_vs_digital = [8.0, 2.0, 8.0]
x = np.arange(3)
bars1 = ax.bar(x - 0.18, scim_vs_analog, width=0.34, color=GREEN, label="SCIM vs 模拟 CIM")
bars2 = ax.bar(x + 0.18, scim_vs_digital, width=0.34, color=BLUE, label="SCIM vs 数字 CIM")
for b, v in zip(bars1, scim_vs_analog): ax.text(b.get_x() + b.get_width() / 2, v + 0.12, "×%.1f" % v, ha="center", fontsize=10)
for b, v in zip(bars2, scim_vs_digital): ax.text(b.get_x() + b.get_width() / 2, v + 0.12, "×%.1f" % v, ha="center", fontsize=10)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("SCIM 能效优势（倍数）")
ax.set_title("SCIM 相对其他 CIM 的能效优势（论文 Fig.9）")
ax.set_ylim(0, 10)
ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3)
fig.text(0.5, 0.01, "注：依据论文 Fig.9（1-bit 时 SCIM 超模拟 CIM 6×、超数字 CIM 8×；8-bit 收窄；平均池化跳算恢复优势）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c02_能效优势.png")); plt.close(fig)

# ---------- c03 电压 vs 能效 + 14nm 宏 ----------
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=150)
v = np.array([0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
eff65 = np.array([7.96, 7.2, 5.75, 4.9, 4.2, 3.6, 3.0])
ax.plot(v, eff65, "o-", color=GREEN, lw=2.4, label="65nm 系统能效（全利用卷积层）")
ax.set_xlabel("电压（V）"); ax.set_ylabel("能效（TOPS/W）")
ax.set_title("65nm 加速器能效 vs 电压（论文 Fig.17）")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
ax.annotate("峰值 7.96 TOPS/W @0.7V", xy=(0.7, 7.96), xytext=(0.78, 7.3),
            arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN, fontsize=9.5, fontweight="bold")
fig.text(0.5, 0.01, "注：曲线为趋势示意（依据论文 Fig.17；14nm 宏 8-bit 35 TOPS/W、带池化 140 TOPS/W 见正文）", ha="center", fontsize=8, color=GRAY)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "c03_电压能效.png")); plt.close(fig)

print("charts done")
