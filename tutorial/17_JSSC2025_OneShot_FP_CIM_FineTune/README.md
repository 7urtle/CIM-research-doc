# 17 · One-Shot 浮点 CIM 引擎（JSSC 2025）

**论文**：Haikang Diao 等, "A Computing-in-Memory Engine Supporting One-Shot Floating-Point NN Inference and On-Device Fine-Tuning for Edge AI," IEEE JSSC, vol. 60, no. 9, pp. 3403–3414, Sep. 2025

**教学对象**：未做过 CIM 实际研究的学生（零基础）

## 打开方式
直接用浏览器打开 `index.html` 即可（单文件，内联 CSS/JS，无需服务器）。

## 内容结构（10 节）
- 00 导读与本论文速览（30 秒版 + 摘要逐句精读 + 贡献清单）
- 01 背景：预对齐 FP-CIM 的四步流程（尾数 MAC 8 周期瓶颈）
- 02 三大挑战与总体架构（ManAU / CIM core / ITFU / ODFC）
- 03 创新①：One-Shot 计算（multiply-less → 最小选择，8 周期→1 周期）
- 04 ParMS 并行最小选择器（进位前瞻比较树、三态门控）
- 05 创新②：输入-权重协同对齐 + UBF16（免 XE_max、归一化 16→8 位）
- 06 创新③：ODFC 片上微调（128 轮顺序更新、保损失 FP 加法）
- 07 部署流程与 NN 演示（重训练补偿、三任务零损失）
- 08 实测与对比（128 TFLOPS/W、7.02 TFLOPS/mm²、FoM +5×）
- 09 总结 · 未来研究方向 · 术语表 · 参考资料

## 配套素材
| 类型 | 内容 |
|---|---|
| 教学图 | `assets/diagrams/d01–d09.svg`（9 张，矢量） |
| 数据图 | `assets/charts/c01–c03.png`（3 张，matplotlib，注明"示意"） |
| 演示视频 | `assets/videos/v01–v03.mp4`（3 个，PIL 逐帧 + ffmpeg H.264） |
| 交互仿真 | 页内 3 个 canvas（演示 A：one-shot 流水；演示 B：ParMS 比较；演示 C：ODFC 恢复） |
| 论文原图 | `assets/figs/fig17_*.png`（24 张，从 PDF 裁剪，© IEEE 教学引用） |
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
