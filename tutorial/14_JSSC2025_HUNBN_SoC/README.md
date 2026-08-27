# 14 · HUNBN 16nm 数字存内计算 SoC（JSSC 2025）

**论文**：Weijie Jiang 等, "HUNBN, a 16-nm Digital In-Memory-Compute SoC for Edge CNN Application Achieving 24 TOPs/W (4b) at System Level," IEEE JSSC, vol. 60, no. 7, pp. 2434–2445, Jul. 2025

**教学对象**：未做过 CIM 实际研究的学生（零基础）

## 打开方式
直接用浏览器打开 `index.html` 即可（单文件，内联 CSS/JS，无需服务器）。

## 内容结构（10 节）
- 00 导读与本论文速览（30 秒版 + 摘要逐句精读 + 贡献清单）
- 01 背景：数字 PE vs DIMC、系统级能效的三个乘数
- 02 HUNBN SoC 总体架构（RISC-V + DIMC 簇 + P1–P3 SRAM + 双总线）
- 03 创新①：foundry 6T 高密度存储（508 kB/mm²、格雷码译码器省 50%）
- 04 创新②：分离 MAC 流程（面积 −20%）+ 同步 DIMC 操作（免延迟线）
- 05 创新③：CNN 数据流映射（4 种情形，含转置卷积）
- 06 创新④：四级数据结构 + 滑动窗口 + 数据前瞻
- 07 部分和精度控制与鲁棒性（Shmoo）
- 08 实测与端到端工作负载（U-Net/ResNet8/MobileNetV1/DS-CNN/自编码器）
- 09 总结 · 未来研究方向 · 术语表 · 参考资料

## 配套素材
| 类型 | 内容 |
|---|---|
| 教学图 | `assets/diagrams/d01–d09.svg`（9 张，矢量） |
| 数据图 | `assets/charts/c01–c03.png`（3 张，matplotlib，注明"示意"） |
| 演示视频 | `assets/videos/v01–v03.mp4`（3 个，PIL 逐帧 + ffmpeg H.264） |
| 交互仿真 | 页内 3 个 canvas（演示 A：PE vs DIMC；演示 B：1bit×2bit 乘法；演示 C：同步时序） |
| 论文原图 | `assets/figs/fig14_*.png`（22 张，从 PDF 裁剪，© IEEE 教学引用） |
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
