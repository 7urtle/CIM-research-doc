# 两周期数字存内计算处理器零基础精讲 · IEEE JSSC 2025

> A 28-nm 19.9-to-258.5-TOPS/W 8b Digital Computing-in-Memory Processor With
> Two-Cycle Macro Featuring Winograd-Domain Convolution and Macro-Level Parallel
> Dual-Side Sparsity（IEEE JSSC, vol.60, no.1, 2025 · 中科院微电子所等）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图。

## 目录结构

```
11_JSSC2025_TwoCycle_Winograd_CIM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（吞吐瓶颈/乘法分解/Radix16/Winograd/MDPS）
│   ├── charts/         ← 3 张数据图（能效/Winograd 权衡/MDPS 收益）
│   ├── videos/         ← 3 个 MP4（两周期乘法/Winograd/MDPS）
│   ├── figs/           ← 论文原图（© IEEE 2024，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 吞吐瓶颈 → 02 乘法分解 → 03 创新① Radix16+LUT → 04 Winograd 基础 →
05 创新② 混合 Winograd → 06 创新③ MDPS → 07 系统架构 → 08 实测对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
