# MXFP 自适应位宽存内计算（MXFP-CIM）零基础精讲 · ISSCC 2026 Paper 30.1

> A 28nm 127.54TFLOPS/W MXFP6 and 117.42TFLOPS/W MXFP8 Compute-in-Memory Macro with
> Adaptive-Preserved-Bit-Width and Serial-Dual-Bit-Sliding Schemes
> （ISSCC 2026 · Session 30 · Paper 30.1 · 东南大学+小米+北大）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
06_ISSCC2026_30.1_MXFP-CIM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（MXFP 格式/SDBS/HDM/分配/架构）
│   ├── charts/         ← 3 张数据图（能效/PBW-MRE/SDBS 收益）
│   ├── videos/         ← 3 个 MP4（SDBS 滑动/MXFP 映射/数据流）
│   ├── figs/           ← 论文原图 Fig. 30.1.1–30.1.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 为什么需要 MXFP → 02 MXFP 格式 → 03 三大挑战 → 04 创新① SDBS →
05 创新② HDM 映射 → 06 创新③ 双级分配 → 07 架构 → 08 实测对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
