# Compound AI 全数据通路浮点存内计算（FP-CIM）零基础精讲 · ISSCC 2025 Paper 14.4

> A 51.6TFLOPs/W Full-Datapath CIM Macro Approaching Sparsity Bound and &lt;2⁻³⁰ Loss
> for Compound AI（ISSCC 2025 · Session 14 · Paper 14.4 · 清华大学）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
02_ISSCC2025_14.4_CompoundAI_CIM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（Compound AI/MantissaEE/后对齐/AIM/稀疏）
│   ├── charts/         ← 3 张数据图（能效/SER/稀疏加速）
│   ├── videos/         ← 3 个 MP4（后对齐/AIM/稀疏）
│   ├── figs/           ← 论文原图 Fig. 14.4.1–14.4.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 Compound AI 背景 → 02 三大挑战 → 03 MantissaEE → 04 创新① 后乘积对齐 →
05 创新② 全数据路径存内 → 06 创新③ 稀疏加速 → 07 系统架构 → 08 实测对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
