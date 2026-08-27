# -*- coding: utf-8 -*-
"""论文16演示视频：v01 共享与XNOR / v02 ASCON解密流程 / v03 PUF密钥"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
VDIR = os.path.join(ROOT, "assets", "videos")
os.makedirs(VDIR, exist_ok=True)
FFMPEG = r"C:\Users\weiyu\Desktop\CIM研究\_ffmpeg\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
FONT = r"C:\Windows\Fonts\msyh.ttc"
def font(sz): return ImageFont.truetype(FONT, sz)
W, H, FPS = 960, 540, 30

def make_frames(render, nframes, outdir):
    os.makedirs(outdir, exist_ok=True)
    for i in range(nframes):
        img = Image.new("RGB", (W, H), (10, 17, 25))
        d = ImageDraw.Draw(img)
        render(d, i, nframes)
        img.save(os.path.join(outdir, "f%04d.png" % i))

def encode(frames_dir, out_path):
    cmd = [FFMPEG, "-y", "-framerate", str(FPS), "-i", os.path.join(frames_dir, "f%04d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22", "-movflags", "+faststart", out_path]
    subprocess.run(cmd, check=True, capture_output=True)

def panel(d, x, y, w, h, fill, outline, r=10):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=2)

def txt(d, s, x, y, size, fill=(240, 244, 250), anchor="lm", fnt=None):
    d.text((x, y), s, font=fnt or font(size), fill=fill, anchor=anchor)

def title(d, s, y=28):
    d.rounded_rectangle([20, 10, W - 20, 56], radius=10, fill=(15, 27, 45))
    txt(d, s, W // 2, y, 19, fill=(255, 255, 255), anchor="mm")

# ================= v01 Boolean sharing + XNOR =================
def v01(d, i, n):
    t = i / n
    title(d, "Boolean 共享 + XNOR 乘法：免随机比特的安全计算")
    # left: sharing
    panel(d, 40, 80, 440, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "3 份共享：b = b1⊕b2⊕b3", 260, 102, 15, fill=(170, 240, 200), anchor="mm")
    k = i % 40
    b = k // 20  # 0 or 1
    b1 = (k // 4) % 2
    b2 = (k // 8) % 2
    b3 = b1 ^ b2 ^ b
    panel(d, 70, 140, 100, 56, (22, 44, 34), (70, 190, 130), r=8)
    txt(d, "b1 = %d" % b1, 120, 168, 16, fill=(200, 240, 220), anchor="mm")
    panel(d, 190, 140, 100, 56, (22, 44, 34), (70, 190, 130), r=8)
    txt(d, "b2 = %d" % b2, 240, 168, 16, fill=(200, 240, 220), anchor="mm")
    panel(d, 310, 140, 100, 56, (22, 44, 34), (70, 190, 130), r=8)
    txt(d, "b3 = %d" % b3, 360, 168, 16, fill=(200, 240, 220), anchor="mm")
    txt(d, "秘密 b = %d（由 3 份恢复）" % b, 260, 230, 15, fill=(255, 255, 255), anchor="mm")
    txt(d, "单独看任何一份 → 看似随机 → 功耗不泄露 b", 260, 262, 12.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "每条子电路只用输入份的严格子集（非完备性）", 260, 292, 12.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "→ 电路功耗与真实数据无关", 260, 320, 12.5, fill=(170, 240, 200), anchor="mm")
    txt(d, "理想 TI 需每周期随机比特 → IMC 百万 MAC 不可行", 260, 356, 12, fill=(255, 200, 190), anchor="mm")

    # right: XNOR vs AND
    panel(d, 500, 80, 420, 330, (22, 26, 44), (150, 120, 200))
    txt(d, "XNOR 乘法（线性）vs AND（非线性）", 710, 102, 15, fill=(210, 190, 240), anchor="mm")
    aw, ak = 1, 1  # activation bit, weight bit
    # AND panel
    panel(d, 530, 130, 180, 100, (40, 26, 24), (230, 120, 110), r=8)
    txt(d, "AND 乘法（传统）", 620, 150, 13, fill=(255, 190, 180), anchor="mm")
    txt(d, "非线性 → 共享后不均匀", 620, 176, 11.5, fill=(230, 180, 170), anchor="mm")
    txt(d, "需随机比特+输出寄存器", 620, 200, 11.5, fill=(230, 180, 170), anchor="mm")
    txt(d, "48 门等效 / 2 随机比特", 620, 222, 11.5, fill=(255, 210, 200), anchor="mm")
    # XNOR panel
    panel(d, 730, 130, 170, 100, (22, 44, 34), (70, 190, 130), r=8)
    txt(d, "XNOR（本论文）", 815, 150, 13, fill=(170, 240, 200), anchor="mm")
    txt(d, "线性 → 每份独立计算", 815, 176, 11.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "天然均匀+抗毛刺", 815, 200, 11.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "6 门等效 / 0 随机比特", 815, 222, 11.5, fill=(120, 230, 180), anchor="mm")
    # SV/BV
    txt(d, "XNOR 乘法 = ±1 乘法 → 用有符号值 SV=Σ2ⁱ·(−1)^(1−bᵢ)", 710, 262, 12.5, fill=(200, 185, 230), anchor="mm")
    txt(d, "校正因子：SVout = 2·BVout − (2ⁿᵂ−1)(2ⁿᴬ−1)·r（常量可预计算）", 710, 292, 12, fill=(200, 185, 230), anchor="mm")
    txt(d, "→ 多位 MAC 也能用 XNOR → NN 精度零影响（表 I）", 710, 322, 12.5, fill=(170, 240, 200), anchor="mm")
    txt(d, "→ 运行期零随机比特 → IMC 可扩展", 710, 352, 13, fill=(255, 210, 130), anchor="mm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "安全三性质：正确性 · 非完备性 · 近似均匀性（AND 不满足，XNOR 天然满足）", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "加法树用进位保存（免半加器）· 累加器首拍用复用式随机 0 共享 → 全链路零运行期随机比特", W // 2, 490, 13, fill=(180, 220, 200), anchor="mm")

# ================= v02 ASCON decryption =================
def v02(d, i, n):
    t = i / n
    title(d, "模型解密：ASCON 轻量密码（BPA 安全）")
    # pipeline
    panel(d, 40, 80, 300, 120, (22, 26, 44), (150, 120, 200))
    txt(d, "片外 DRAM/NVM", 190, 108, 14, fill=(210, 190, 240), anchor="mm")
    txt(d, "权重以密文存储", 190, 134, 12, fill=(200, 185, 230), anchor="mm")
    txt(d, "冷启动攻击也读不出", 190, 158, 11.5, fill=(200, 185, 230), anchor="mm")
    txt(d, "总线可被探针窃听", 190, 182, 11.5, fill=(255, 200, 190), anchor="mm")

    panel(d, 380, 80, 240, 120, (30, 34, 24), (240, 200, 90))
    txt(d, "ASCON 解密（片上）", 500, 108, 14, fill=(255, 220, 140), anchor="mm")
    txt(d, "NIST 轻量密码冠军", 500, 134, 12, fill=(240, 210, 130), anchor="mm")
    txt(d, "AND 门占比最低（共享最省）", 500, 158, 11.5, fill=(240, 210, 130), anchor="mm")
    txt(d, "TI 实现仅需 4 个一次性随机比特", 500, 182, 11.5, fill=(255, 230, 160), anchor="mm")

    panel(d, 660, 80, 260, 120, (16, 32, 26), (70, 190, 130))
    txt(d, "SCA 安全 IMC 计算", 790, 108, 14, fill=(170, 240, 200), anchor="mm")
    txt(d, "明文权重写入 SRAM", 790, 134, 12, fill=(190, 230, 210), anchor="mm")
    txt(d, "一次解密、多次计算", 790, 158, 11.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "开销被摊薄", 790, 182, 11.5, fill=(120, 230, 180), anchor="mm")

    # arrows
    d.line([344, 140, 376, 140], fill=(150, 200, 255), width=3)
    d.polygon([(376, 134), (388, 140), (376, 146)], fill=(150, 200, 255))
    d.line([624, 140, 656, 140], fill=(90, 220, 160), width=3)
    d.polygon([(656, 134), (668, 140), (656, 146)], fill=(90, 220, 160))

    # key
    panel(d, 40, 230, 880, 130, (24, 22, 40), (170, 120, 220))
    txt(d, "密钥从哪来？—— PUF 片上生成（见视频 v03）", 480, 254, 14, fill=(210, 190, 240), anchor="mm")
    txt(d, "密钥从片外传入会被探测 → 安全性归零；e-fuse 会被 SEM 成像读出", 480, 284, 12.5, fill=(200, 185, 230), anchor="mm")
    txt(d, "PUF：制造随机失配 → 挑战-响应对 → 密钥；ASCON 支持 2¹²⁸ 次解密不换钥（远超实用需求）", 480, 310, 12.5, fill=(200, 185, 230), anchor="mm")
    txt(d, "可定期用新挑战刷新密钥 → 额外安全", 480, 336, 12, fill=(190, 175, 220), anchor="mm")

    d.rectangle([40, 390, W - 40, 396], fill=(40, 60, 85))
    d.rectangle([40, 390, 40 + (W - 80) * t, 396], fill=(70, 190, 140))
    txt(d, "ASCON 的『Changing of the Guards』（Daemen）：用状态内比特互 remask → 运行期零随机比特", W // 2, 422, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "解密延迟 +3.2×，但权重加载不频繁（数据复用）→ 整体能耗/延迟影响小 · ASCON 仅占宏面积 ~16%", W // 2, 450, 13, fill=(180, 220, 200), anchor="mm")
    txt(d, "CPA 测试：ASCON 正确密钥与错误猜测不可区分（Fig.9c）", W // 2, 478, 13, fill=(170, 240, 200), anchor="mm")

# ================= v03 SRAM PUF =================
def v03(d, i, n):
    t = i / n
    title(d, "PUF 密钥生成：复用 IMC SRAM（反馈切断）")
    # bitcell
    panel(d, 40, 80, 440, 330, (16, 32, 26), (70, 190, 130))
    txt(d, "SCA 安全位单元（反馈切断晶体管）", 260, 102, 14, fill=(170, 240, 200), anchor="mm")
    # cross-coupled inverters
    ox, oy = 100, 130
    # left inverter
    d.rectangle([ox, oy, ox + 70, oy + 46], fill=(24, 46, 70), outline=(140, 200, 255), width=2)
    txt(d, "反相器 A", ox + 35, oy + 14, 11, fill=(140, 200, 255), anchor="mm")
    txt(d, "（制造失配）", ox + 35, oy + 32, 10, fill=(160, 200, 235), anchor="mm")
    # right inverter
    d.rectangle([ox + 120, oy, ox + 190, oy + 46], fill=(24, 46, 70), outline=(140, 200, 255), width=2)
    txt(d, "反相器 B", ox + 155, oy + 14, 11, fill=(140, 200, 255), anchor="mm")
    txt(d, "（制造失配）", ox + 155, oy + 32, 10, fill=(160, 200, 235), anchor="mm")
    # feedback cut switch
    d.rectangle([ox + 70, oy - 16, ox + 120, oy + 10], fill=(44, 30, 24), outline=(240, 180, 70), width=2)
    txt(d, "反馈切断", ox + 95, oy - 4, 11, fill=(255, 210, 130), anchor="mm")
    d.line([ox + 70, oy + 8, ox + 70, oy + 20, ox + 120, oy + 20, ox + 120, oy + 8], fill=(240, 180, 70), width=2)
    # steps
    steps = ["① 切断反馈", "② 预放电输入", "③ 重连反馈", "④ 标准读出"]
    for s in range(4):
        sy = oy + 90 + s * 34
        col = (255, 210, 130) if (i // 30) % 4 == s else (190, 230, 210)
        txt(d, steps[s], 260, sy, 13.5, fill=col, anchor="mm")
        if (i // 30) % 4 == s:
            d.rectangle([200, sy - 14, 380, sy + 14], outline=(240, 180, 70), width=2)
    txt(d, "SRAM 按较强反相器沉降到 0/1（制造随机性）", 260, oy + 235, 12.5, fill=(190, 230, 210), anchor="mm")
    txt(d, "→ PUF 位 = 芯片独有的「指纹」", 260, oy + 258, 12.5, fill=(170, 240, 200), anchor="mm")

    # FSM / TMV
    panel(d, 500, 80, 420, 330, (22, 26, 44), (150, 120, 200))
    txt(d, "密钥读出：FSM + 时间多数投票（TMV）", 710, 102, 14, fill=(210, 190, 240), anchor="mm")
    # TMV votes
    votes = [1, 1, 1, 0, 1]
    txt(d, "同一单元多次评估：", 540, 130, 12.5, fill=(200, 185, 230), anchor="lm")
    for v in range(5):
        x = 540 + v * 40
        d.rectangle([x, 148, x + 30, 172], fill=(40, 90, 130) if votes[v] else (30, 44, 30), outline=(140, 200, 255))
        txt(d, str(votes[v]), x + 15, 160, 12, fill=(255, 255, 255), anchor="mm")
    txt(d, "→ 多数（3 个 1）→ 该位 = 1（抗噪声）", 710, 198, 12.5, fill=(200, 185, 230), anchor="mm")
    txt(d, "FSM 处理 4 位一组 → 会泄露统计 → 差分操作：", 540, 226, 12.5, fill=(200, 185, 230), anchor="lm")
    txt(d, "感放差分输出都给 FSM → 恒定翻转 → 抗简单功耗分析", 540, 250, 12.5, fill=(200, 185, 230), anchor="lm")
    txt(d, "TMV 次数可配置 → 按用例设鲁棒性", 540, 280, 12.5, fill=(190, 175, 220), anchor="lm")
    # results
    panel(d, 540, 306, 360, 86, (26, 40, 30), (70, 190, 130), r=8)
    txt(d, "NIST 800-22 随机性全过（5 芯片 p>0.01）", 590, 328, 12, fill=(190, 230, 210), anchor="lm")
    txt(d, "最小熵 ~0.91–0.93 · Von Neumann 去偏", 590, 352, 12, fill=(190, 230, 210), anchor="lm")
    txt(d, "TMV+BCH 纠错 → 0% 误码 · intra-HD≈0 · inter-HD≈192", 590, 376, 12, fill=(170, 240, 200), anchor="lm")

    d.rectangle([40, 430, W - 40, 436], fill=(40, 60, 85))
    d.rectangle([40, 430, 40 + (W - 80) * t, 436], fill=(70, 190, 140))
    txt(d, "只用小块综合数字逻辑（FSM+TMV）→ 复用 IMC SRAM → 几乎零面积开销", W // 2, 462, 13.5, fill=(210, 225, 240), anchor="mm")
    txt(d, "噪声鲁棒：TMV + 老化烧灼硬化 + 不稳定单元掩蔽/裁剪；CNN 攻击预测密钥 RMSE 显著增大（表 II）", W // 2, 490, 13, fill=(180, 220, 200), anchor="mm")

def main():
    jobs = [("v01", v01, 200), ("v02", v02, 200), ("v03", v03, 200)]
    for name, fn, nf in jobs:
        fd = os.path.join(ROOT, "_work_vid16", name)
        make_frames(fn, nf, fd)
        encode(fd, os.path.join(VDIR, name + ".mp4"))
        print(name, "done", os.path.getsize(os.path.join(VDIR, name + ".mp4")))

if __name__ == "__main__":
    main()
