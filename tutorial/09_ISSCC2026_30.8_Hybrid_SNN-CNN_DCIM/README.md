# 混合 SNN-CNN 全数字 SRAM 存内计算（DCIM）零基础精讲 · ISSCC 2026 Paper 30.8

> A 16nm, 1Mb, 1-to-8b-Configurable 444.21 TOPS/W Fully Digital SRAM Compute-In-Memory
> Macro for Hybrid SNN-CNN Edge Computing（ISSCC 2026 · Session 30 · Paper 30.8 · NTHU+ITRI）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
09_ISSCC2026_30.8_Hybrid_SNN-CNN_DCIM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（神经元模型/CMDM-LCC/映射/架构）
│   ├── charts/         ← 3 张数据图（能效/FoM/面积-能效）
│   ├── videos/         ← 3 个 MP4（神经元动画/双模式数据流/映射时序）
│   ├── figs/           ← 论文原图 Fig. 30.8.1–30.8.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 SNN 与 CNN 背景 → 02 为什么需要混合 CIM → 03 神经元模型（IF/LIF/IQIF）→
04 创新① CFD-SC-RC 与 CMDM-LCC（双模式共享） → 05 创新② DM-MPDBU → 06 创新③ PS-WR-ODM 数据映射 →
07 系统架构与数据流 → 08 实测与对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。建议把 3 个交互仿真玩一遍、3 个视频看完。
