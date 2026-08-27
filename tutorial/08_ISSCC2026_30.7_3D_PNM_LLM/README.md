# 3D 双 DRAM 单逻辑近存计算（PNM）零基础精讲 · ISSCC 2026 Paper 30.7

> A 1.2GHz 12.77GB/s/mm² 3D Two-DRAM-One-Logic Process-Near-Memory Chip for
> Edge LLM Applications（ISSCC 2026 · Session 30 · Paper 30.7 · 复旦+中科院微电子所+张江实验室+西安紫光国芯）

## 打开方式

**用浏览器直接打开 `index.html` 即可**（无需服务器）。内嵌 3 个交互 Canvas 仿真、
3 个 MP4 演示视频、8 张教学 SVG 图、4 张数据图及论文原图 7 张。

## 目录结构

```
08_ISSCC2026_30.7_3D_PNM_LLM/
├── index.html          ← 教学主文件（单文件）
├── assets/
│   ├── style.css / app.js
│   ├── diagrams/       ← 8 张教学 SVG（3D 堆叠/架构/ACC/GEMM/存储层次）
│   ├── charts/         ← 4 张数据图（带宽密度/每比特能量/延迟/GEMM）
│   ├── videos/         ← 3 个 MP4（3D 堆叠组装/GEMM 数据流/访存延迟）
│   ├── figs/           ← 论文原图 Fig. 30.7.1–30.7.7（© IEEE，教学引用）
│   └── 原文论文.pdf
└── _src/               ← 源分片与构建脚本（python build.py 重新构建）
```

## 学习路径

00 速览 → 01 边缘 LLM 困境 → 02 PNM 路线与 3D 集成 → 03 LLM 与 GEMM 基础 →
04 创新① Two-DRAM-One-Logic → 05 创新② DDR4 兼容 + ACC → 06 创新③ GEMM 数据流与访存优化 →
07 存储层次 → 08 实测与对比 → 09 未来方向/术语表/参考

预计阅读 + 动手时间：约 60 分钟。建议把 3 个交互仿真玩一遍、3 个视频看完。
