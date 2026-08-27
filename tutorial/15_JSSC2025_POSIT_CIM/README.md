# 15 · POSIT 存内计算宏 PD-CIM（JSSC 2025）

**论文**：Yang Wang 等, "An Energy-Efficient POSIT Compute-in-Memory Macro for High-Accuracy AI Applications," IEEE JSSC, vol. 60, no. 8, pp. 2981–2993, Aug. 2025

**教学对象**：未做过 CIM 实际研究的学生（零基础）

## 打开方式
直接用浏览器打开 `index.html` 即可（单文件，内联 CSS/JS，无需服务器）。

## 内容结构（10 节）
- 00 导读与本论文速览（30 秒版 + 摘要逐句精读 + 贡献清单）
- 01 背景：FP-CIM 瓶颈与 POSIT 数据格式（S/R/E/M、温度计码）
- 02 POSIT 动态特性三大挑战（regime 能耗 / 单元欠利用 / 加法树浪费）
- 03 PD-CIM 总体架构（BRPU + 16 CIM 核 + CASU + 全局 SRAM）
- 04 创新①：BRPU（shift-OR 替代 codec、双向移位控制、合并前导检测器）
- 05 创新②：CPCS（关键位预计算存储 → 双位 MAC、2–4b 关联、3b 优先分区）
- 06 创新③：CASU（OR 替代加法、提前检测、循环交替调度）
- 07 精度表现与三招适配性（FP16 / 经典 POSIT 处理器）
- 08 实测与 SOTA 对比（83.23 TFLOPS/W、省能 2.36×、加速 3.51×）
- 09 总结 · 未来研究方向 · 术语表 · 参考资料

## 配套素材
| 类型 | 内容 |
|---|---|
| 教学图 | `assets/diagrams/d01–d09.svg`（9 张，矢量） |
| 数据图 | `assets/charts/c01–c03.png`（3 张，matplotlib，注明"示意"） |
| 演示视频 | `assets/videos/v01–v03.mp4`（3 个，PIL 逐帧 + ffmpeg H.264） |
| 交互仿真 | 页内 3 个 canvas（演示 A：POSIT 位结构；演示 B：双位 MAC；演示 C：OR 累加） |
| 论文原图 | `assets/figs/fig15_*.png`（18 张，从 PDF 裁剪，© IEEE 教学引用） |
| 原文 PDF | `assets/原文论文.pdf` |

## 生成方法（_src/）
1. `make_charts.py` → 3 张数据图；
2. `make_videos.py` → 3 个演示视频（需 ffmpeg）；
3. 编辑 `head.html` / `part00–09.html` / `tail.html` / `assets/app.js`；
4. `build.py` → 拼接生成 `index.html`。

## 已做的质量验证
- 无头 Chrome 抓 console：0 JS 错误；
- 3 个 canvas 仿真均绘制非背景像素（31 万+ px/个）；
- 3 个 video source 存在且可解码；
- 所有图片资源引用无缺失；无 quiz（思考题/自测）内容。
