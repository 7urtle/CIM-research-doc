# 13 · Multiply-Less 近似 SRAM 存内计算宏（JSSC 2025）

**论文**：Haikang Diao 等, "A Multiply-Less Approximate SRAM Compute-In-Memory Macro for Neural-Network Inference," IEEE JSSC, vol. 60, no. 2, pp. 695–705, Feb. 2025（ISSCC'23 [19] 期刊扩展版）

**教学对象**：未做过 CIM 实际研究的学生（零基础）

## 打开方式
直接用浏览器打开 `index.html` 即可（单文件，内联 CSS/JS，无需服务器）。

## 内容结构（10 节）
- 00 导读与本论文速览（30 秒版 + 摘要逐句精读 + 贡献清单）
- 01 背景：CIM 与数据搬移、数字 CIM 的乘法二次成本
- 02 近似数字 CIM 三大挑战（电路近似误差 / 乘法二次成本 / 位级稀疏未利用）
- 03 创新①：Multiply-Less NN（L1 距离替代点积，AdderNet 思想）
- 04 创新②：预计算 L1 方案（|x−w| = x+w−2·min，权重截断 86× 稀疏度）
- 05 系统架构与数据流（16 阵列 + ACT Buffer + ActACCU + L1 计算单元）
- 06 创新③：位串行比较 + 稀疏感知提前停止（MinMUX / 读端口省电 1.8×）
- 07 改进动态逻辑比较器（电荷共享误差分析、激活正则化）
- 08 NN 部署流程与芯片实测（102 TOPS/W、91.71%/74.8%）
- 09 总结 · 未来研究方向 · 术语表 · 参考资料

## 配套素材
| 类型 | 内容 |
|---|---|
| 教学图 | `assets/diagrams/d01–d09.svg`（9 张，矢量） |
| 数据图 | `assets/charts/c01–c03.png`（3 张，matplotlib，注明"示意"） |
| 演示视频 | `assets/videos/v01–v03.mp4`（3 个，PIL 逐帧 + ffmpeg H.264） |
| 交互仿真 | 页内 3 个 canvas（演示 A：点积 vs L1；演示 B：位串行最小选择；演示 C：比较器波形） |
| 论文原图 | `assets/figs/fig13_*.png`（18 张，从 PDF 裁剪，© IEEE 教学引用） |
| 原文 PDF | `assets/原文论文.pdf` |

## 生成方法（_src/）
1. `make_charts.py` → 生成 3 张数据图；
2. `make_videos.py` → 生成 3 个演示视频（需 ffmpeg）；
3. 编辑 `head.html` / `part00–09.html` / `tail.html` / `assets/app.js`；
4. `build.py` → 拼接生成 `index.html`。

## 已做的质量验证
- 无头 Chrome 抓 console：0 JS 错误；
- 3 个 canvas 仿真均绘制非背景像素（31 万+ px/个）；
- 3 个 video source 存在且可解码（960×540, 180–210 帧, H.264）；
- 所有图片资源引用无缺失；无 quiz（思考题/自测）内容。
