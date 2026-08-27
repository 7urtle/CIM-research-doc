# NeuroPilot 模拟路径搜索 CIM 零基础精讲 · ISSCC 2025 Paper 14.7

> NeuroPilot: A 28nm, 69.4fJ/node and 0.22ns/node, 32×32 Mimetic-Path-Searching
> CIM-Macro with Dynamic-Logic Pilot PE and Dual-Direction Searching
> （ISSCC 2025 · Session 14 · Paper 14.7 · 东南大学）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
04_ISSCC2025_14.7_NeuroPilot/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（路径搜索/波前/DDS/PE/OPC/TsCFP/架构）
│   ├── charts/         ← 3 张数据图（核心指标/DDS 收益/TsCFP 实例）
│   ├── videos/         ← 3 个 MP4（波前传播/DDS/TsCFP）
│   ├── figs/           ← 论文原图 Fig. 14.7.1–14.7.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 路径搜索应用 → 02 三大挑战 → 03 波前传播 → 04 创新① DDS →
05 创新② Pilot PE + OPC → 06 创新③ TsCFP → 07 架构与工作流 → 08 实测对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
