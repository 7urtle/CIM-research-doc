# SpikeRAM 事件驱动感-存-算-学处理器零基础精讲 · ISSCC 2026 Paper 18.4

> SpikeRAM: A 48.1pW/Synapse/Bit Event-Driven Spiking Compute-Near/In-Memory Processor
> with Neuromorphic Sensor Enabling Life-Long On-Chip Learning
> （ISSCC 2026 · Session 18 · Paper 18.4 · 香港科技大学（广州）+时识科技）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
05_ISSCC2026_18.4_SpikeRAM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（EVS/系统/事件卷积/e-OTBP/格雷码/演示）
│   ├── charts/         ← 3 张数据图（精度/MRAM 收益/对比）
│   ├── videos/         ← 3 个 MP4（事件流/e-OTBP/格雷码）
│   ├── figs/           ← 论文原图 Fig. 18.4.1–18.4.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 EVS 与 SNN → 02 三大挑战与系统 → 03 EVS 基础 → 04 EVS-sCNN 核 →
05 sFC-OCL 核 → 06 创新① e-OTBP → 07 创新② 三值梯度+格雷码 → 08 实测与应用 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
