# 转移计数行（TCL）位并行存内计算零基础精讲 · ISSCC 2026 Paper 30.4

> A 28nm 106.85TOPS/W and 77.68TFLOPS/W CIM Macro with Stage-Wise-Enabled Lossless
> Compressors Based on Sign-Bit-Embedded Transition-Counting-Lines for Edge-AI Devices
> （ISSCC 2026 · Session 30 · Paper 30.4 · 西安电子科技大学）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
07_ISSCC2026_30.4_TCL_CIM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（位并行/外积/TCL/符号嵌入/10 相/架构）
│   ├── charts/         ← 3 张数据图（能效/FoM/MAC cell FoM）
│   ├── videos/         ← 3 个 MP4（TCL 数沿/10 相时序/数据流）
│   ├── figs/           ← 论文原图 Fig. 30.4.1–30.4.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 位串行 vs 位并行 → 02 三大挑战 → 03 外积与位列 → 04 创新① TCL 数沿 →
05 创新② 符号位嵌入 → 06 创新③ 10 相使能 → 07 架构与模式 → 08 实测对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
