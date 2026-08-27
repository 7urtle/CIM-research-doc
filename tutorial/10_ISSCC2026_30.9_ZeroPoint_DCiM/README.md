# 数字存内计算（DCiM）零基础精讲 · ISSCC 2026 Paper 30.9

> A 147TOPS/W, 250TOPS/mm², Fully Synthesizable, Digital Compute-in-Memory Accelerator
> Supporting INT8×INT8 with Zero-Point Quantization in Intel 18A Technology
> （ISSCC 2026 · Session 30 · Paper 30.9 · Intel）

## 打开方式

**直接用浏览器打开 `index.html` 即可**（双击即可，无需服务器；所有图片/视频/动画均使用相对路径）。

推荐使用 Chrome / Edge 最新版。教程内嵌 5 个可交互 Canvas 仿真、3 个 MP4 演示视频、
11 张教学 SVG 图、4 张数据图以及论文原图 7 张。

## 目录结构

```
10_ISSCC2026_30.9_ZeroPoint_DCiM/
├── index.html              ← 教学主文件（单文件，内联 CSS/JS）
├── 原文论文.pdf 位置        ← assets/原文论文.pdf
├── assets/
│   ├── style.css           ← 样式（构建时内联进 index.html）
│   ├── app.js              ← 交互仿真脚本（构建时内联）
│   ├── diagrams/           ← 11 张自制教学 SVG（架构/电路/量化/流水线）
│   ├── charts/             ← 4 张 matplotlib 数据图（面积功耗分解、对比、实测）
│   ├── videos/             ← 3 个 MP4 演示视频（Booth 乘法/数据流/双缓冲）
│   └── figs/               ← 论文原图 Fig. 30.9.1–30.9.7（© IEEE，教学引用）
└── _src/                   ← 源分片与构建脚本（可重新生成 index.html）
    ├── head.html / tail.html / part00..part09.html
    ├── style.css 源、app.js 源
    ├── build.py            ← python build.py 重新构建
    ├── make_charts.py      ← 重新生成数据图（需 matplotlib）
    └── make_videos.py      ← 重新生成演示视频（需 PIL；ffmpeg 在 ../../_ffmpeg）
```

## 修改与重建

```powershell
python _src/build.py        # 重新拼接 index.html（改 HTML/CSS/JS 后执行）
python _src/make_charts.py  # 重绘数据图
python _src/make_videos.py  # 重制视频（较慢，约 2 分钟）
```

## 学习路径

01 为什么需要存内计算 → 02 数字 CiM 与可综合 → 03 零点量化基础 →
04 核心数学（9b→8b 映射） → 05 Booth 编码 → 06 存储与双缓冲 →
07 系统架构与数据流 → 08 面积功耗与实测 → 09 自测/未来方向/术语表

预计阅读 + 动手时间：60–90 分钟。建议把 5 个交互仿真都玩一遍、3 个视频都看完。
