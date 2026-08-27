# 广播对齐浮点存内计算（FP-CIM）零基础精讲 · ISSCC 2025 Paper 14.3

> A 28nm 17.83-to-62.84TFLOPS/W Broadcast-Alignment Floating-Point CIM Macro with
> Non-Two's-Complement MAC for CNNs and Transformers（ISSCC 2025 · Session 14 · Paper 14.3 · 东南大学+清华）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
01_ISSCC2025_14.3_B-A-N2CMAC_FP-CIM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（FP/INT、对齐、ESICU、N2CMAC、模式）
│   ├── charts/         ← 3 张数据图（能效/面积功耗/周期稀疏性）
│   ├── videos/         ← 3 个 MP4（串行对齐/N2CMAC/广播数据流）
│   ├── figs/           ← 论文原图 Fig. 14.3.1–14.3.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 为什么需要 FP-CIM → 02 浮点格式与对齐 → 03 三大挑战 → 04 宏架构 →
05 创新① ESICU 串行对齐 → 06 创新② N2CMAC → 07 三种模式 → 08 实测对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
