# 16 · 安全的数字存内计算宏（JSSC 2025）

**论文**：Maitreyi Ashok 等, "Digital In-Memory Compute for Machine Learning Applications With Input and Model Security," IEEE JSSC, vol. 60, no. 9, pp. 3390–3400, Sep. 2025

**教学对象**：未做过 CIM 实际研究的学生（零基础）

## 打开方式
直接用浏览器打开 `index.html` 即可（单文件，内联 CSS/JS，无需服务器）。

## 内容结构（10 节）
- 00 导读与本论文速览（30 秒版 + 摘要逐句精读 + 贡献清单）
- 01 背景：ML 加速器的安全威胁（SCA / BPA、威胁模型）
- 02 安全基础：Boolean 共享与阈值实现（正确性/非完备性/均匀性）
- 03 创新①：XNOR 原生安全乘法（6 门+0 随机比特、SV/BV 换算）
- 04 安全加法树与累加器（CSA 免半加器、近似均匀、随机 0 共享）
- 05 创新②：ASCON 轻量密码做片上模型解密（BPA 安全）
- 06 创新③：SRAM PUF 密钥生成（反馈切断、TMV 抗噪）
- 07 安全评估：CPA / DPA 证明（100 万采样不可攻破）
- 08 性能与安全开销（8.1 TOPS/W、位单元 ×5.3、加法树 ×15.5）
- 09 总结 · 未来研究方向 · 术语表 · 参考资料

## 配套素材
| 类型 | 内容 |
|---|---|
| 教学图 | `assets/diagrams/d01–d09.svg`（9 张，矢量） |
| 数据图 | `assets/charts/c01–c03.png`（3 张，matplotlib，注明"示意"） |
| 演示视频 | `assets/videos/v01–v03.mp4`（3 个，PIL 逐帧 + ffmpeg H.264） |
| 交互仿真 | 页内 3 个 canvas（演示 A：Boolean 共享；演示 B：XNOR vs AND；演示 C：CPA 相关性） |
| 论文原图 | `assets/figs/fig16_*.png`（13 张，从 PDF 裁剪，© IEEE 教学引用） |
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
