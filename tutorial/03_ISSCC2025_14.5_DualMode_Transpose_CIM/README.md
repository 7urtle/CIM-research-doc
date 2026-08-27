# 训练/推理双模式转置浮点存内计算（FP-CIM）零基础精讲 · ISSCC 2025 Paper 14.5

> A 28nm 192.3TFLOPS/W Accurate/Approximate Dual-Mode-Transpose Digital 6T-SRAM CIM
> Macro for Floating-Point Edge Training and Inference
> （ISSCC 2025 · Session 14 · Paper 14.5 · 中科院微电子所+北理工+澳大）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、9 张教学 SVG 图、3 张数据图及论文原图 7 张。

## 目录结构

```
03_ISSCC2025_14.5_DualMode_Transpose_CIM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 9 张教学 SVG（片上训练/转置/CWM/SFME/VWPA/DMBP/格式）
│   ├── charts/         ← 3 张数据图（能效/精度/近似收益）
│   ├── videos/         ← 3 个 MP4（转置读取/SFME/DMBP 双模）
│   ├── figs/           ← 论文原图 Fig. 14.5.1–14.5.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 片上训练 → 02 T-CIM 挑战 → 03 转置概念 → 04 创新① CWM-SRAM →
05 创新② SFME+VWPA → 06 创新③ DMBP-MAC → 07 架构与格式 → 08 实测对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。
