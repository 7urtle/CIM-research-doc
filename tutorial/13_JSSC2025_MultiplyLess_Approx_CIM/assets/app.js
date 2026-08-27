/* ============================================================
   Multiply-Less 近似 SRAM CIM 教学教程 · 交互脚本
   演示 A 点积 vs L1 距离 · 演示 B 位串行最小选择 · 演示 C 动态比较器波形
   ============================================================ */
"use strict";

function cvs(id, w, h) {
  const c = document.getElementById(id);
  if (!c) return null;
  c.width = w; c.height = h;
  return { c, ctx: c.getContext("2d"), w, h };
}
function rrect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}
function txt(ctx, s, x, y, size, color, align) {
  ctx.fillStyle = color || "#dbe6f4";
  ctx.font = (size || 13) + "px 'Microsoft YaHei','PingFang SC',sans-serif";
  ctx.textAlign = align || "left";
  ctx.textBaseline = "middle";
  ctx.fillText(s, x, y);
}
const PAL = {
  bg: "#0a1119", panel: "#12202f", line: "#2c4d73",
  blue: "#1e90dc", green: "#3cbe8c", orange: "#f0b446",
  red: "#e66e5a", purple: "#aa78dc", gray: "#7f93ad", white: "#f0f4fa"
};

(function () {
  const bar = document.getElementById("progress");
  const links = Array.from(document.querySelectorAll(".sidebar a"));
  const sections = links.map(a => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  function onScroll() {
    const st = window.scrollY;
    const h = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.width = (h > 0 ? (st / h) * 100 : 0) + "%";
    let cur = 0;
    sections.forEach((s, i) => { if (s && s.offsetTop - 120 <= st) cur = i; });
    links.forEach((a, i) => a.classList.toggle("active", i === cur));
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();

/* ============================================================
   演示 A · 点积 vs L1 距离（卷积核滑动）
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");
  // 4x4 二值输入图，3x3 对角边缘核
  const img = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0]
  ];
  const ker = [1, -1, 1, -1, 1, -1, 1, -1, 1];

  function win(r, c) {
    const v = [];
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) v.push(img[r + i][c + j]);
    return v;
  }

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 A · 卷积核滑动：点积（MAC）与 L1 距离输出对比", 30, 24, 15, PAL.white, "left");
    const pos = cyc % 4; // 滑动位置 0..3（4 个输出位置）
    const r = Math.floor(pos / 2), c = pos % 2;
    const wv = win(r, c);
    let dot = 0, l1 = 0;
    for (let k = 0; k < 9; k++) { dot += wv[k] * ker[k]; l1 += Math.abs(wv[k] - ker[k]); }

    // 输入图
    txt(ctx, "输入特征图（4×4）", 110, 62, 13, PAL.blue, "center");
    const cs = 44, ox = 40, oy = 80;
    for (let rr = 0; rr < 4; rr++) {
      for (let cc = 0; cc < 4; cc++) {
        const x = ox + cc * cs, y = oy + rr * cs;
        ctx.fillStyle = img[rr][cc] ? "#1e4a76" : "#101c2c";
        ctx.strokeStyle = PAL.line; ctx.lineWidth = 1;
        rrect(ctx, x, y, cs - 4, cs - 4, 5); ctx.fill(); ctx.stroke();
        txt(ctx, String(img[rr][cc]), x + cs / 2, y + cs / 2, 13, PAL.white, "center");
      }
    }
    // 高亮窗口
    ctx.strokeStyle = PAL.orange; ctx.lineWidth = 3;
    ctx.strokeRect(ox + c * cs - 2, oy + r * cs - 2, cs * 3 - 2, cs * 3 - 2);
    txt(ctx, "滑动窗口 @" + pos, ox + c * cs + cs * 1.5, oy + cs * 4 + 16, 12, PAL.orange, "center");

    // 核
    txt(ctx, "卷积核（对角边缘）", 330, 62, 13, PAL.purple, "center");
    const ks = 30, kx = 210, ky = 80;
    for (let rr = 0; rr < 3; rr++) {
      for (let cc = 0; cc < 3; cc++) {
        const v = ker[rr * 3 + cc];
        const x = kx + cc * ks, y = ky + rr * ks;
        ctx.fillStyle = v > 0 ? "#1e4a76" : "#4a1e1e";
        ctx.strokeStyle = v > 0 ? PAL.blue : PAL.red; ctx.lineWidth = 2;
        rrect(ctx, x, y, ks - 3, ks - 3, 5); ctx.fill(); ctx.stroke();
        txt(ctx, String(v), x + ks / 2, y + ks / 2, 12, PAL.white, "center");
      }
    }

    // 输出对比
    const bx = 420, by = 80;
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 2;
    rrect(ctx, bx, by, 250, 105, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "点积（MAC）  Σ x·w", bx + 20, by + 24, 14, PAL.blue, "left");
    txt(ctx, "= " + wv.join("·") + " 与核", bx + 20, by + 50, 11, PAL.gray, "left");
    txt(ctx, "= " + dot + "（需 9 次乘法）", bx + 20, by + 76, 15, PAL.white, "left");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, bx, by + 122, 250, 105, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "L1 距离  −Σ|x−w|", bx + 20, by + 146, 14, PAL.green, "left");
    txt(ctx, "= −(" + wv.join("−") + " 之差的绝对值)", bx + 20, by + 172, 11, PAL.gray, "left");
    txt(ctx, "= −" + l1 + "（只有减法+绝对值）", bx + 20, by + 198, 15, PAL.white, "left");

    // 结论
    txt(ctx, "两者响应方向一致（越匹配输出越大）→ L1 可替代点积", bx, by + 260, 13.5, PAL.orange, "left");
    txt(ctx, "硬件：乘法器消失 → 面积/能耗随位宽线性增长", bx, by + 284, 12, PAL.gray, "left");
    if (stat) stat.textContent = "滑动窗口 @" + pos + "：点积=" + dot + "，L1 距离=−" + l1;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1100); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1100);
  draw();
})();

/* ============================================================
   演示 B · 位串行最小选择（MinMUX）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");
  // x = 10 (1010), w = 6 (0110) → min = w
  const xb = [1, 0, 1, 0];
  const wb = [0, 1, 1, 0];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 B · 位串行比较（MSB 优先）：x=1010(10) vs w=0110(6) → min=w", 30, 24, 15, PAL.white, "left");
    const step = cyc % 5; // 0..4
    const decided = step >= 1; // 第1位 1 vs 0 即分出胜负

    // 位格
    const bx = 60, by = 70, bs = 90;
    for (let k = 0; k < 4; k++) {
      const x = bx + k * bs;
      ctx.fillStyle = k <= step ? (decided && k > 0 ? "#16321f" : "#1e4a76") : "#101c2c";
      ctx.strokeStyle = k === step ? PAL.orange : PAL.line; ctx.lineWidth = k === step ? 3 : 1;
      rrect(ctx, x, by, bs - 8, 46, 6); ctx.fill(); ctx.stroke();
      txt(ctx, "x bit" + k, x + (bs - 8) / 2, by + 14, 11, PAL.blue, "center");
      txt(ctx, String(xb[k]), x + (bs - 8) / 2, by + 32, 16, PAL.white, "center");
      const y2 = by + 62;
      ctx.fillStyle = k <= step ? (decided && k > 0 ? "#1f2413" : "#3c2a1e") : "#101c2c";
      ctx.strokeStyle = k === step ? PAL.orange : PAL.line; ctx.lineWidth = k === step ? 3 : 1;
      rrect(ctx, x, y2, bs - 8, 46, 6); ctx.fill(); ctx.stroke();
      txt(ctx, "w bit" + k, x + (bs - 8) / 2, y2 + 14, 11, PAL.orange, "center");
      txt(ctx, String(wb[k]), x + (bs - 8) / 2, y2 + 32, 16, PAL.white, "center");
    }
    // 比较进度
    const msg = step === 0 ? "第 1 位：x=1 vs w=0 → x>w 断言！比较结束"
      : decided ? "比较已锁定：min(x,w)=w（后续位直接输出 w，无需再比较）"
      : "比较中…";
    txt(ctx, msg, 30, by + 140, 14, PAL.orange, "left");
    txt(ctx, decided ? "→ 提前停止：第 2–4 位不再预充/读权重位（省电）" : "→ 正在比较…", 30, by + 166, 12.5, PAL.green, "left");

    // 数据流
    const fx = 30, fy = 218;
    txt(ctx, "L1 计算单元数据流：", fx, fy, 13, PAL.white, "left");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 2;
    rrect(ctx, fx + 150, fy - 14, 150, 28, 6); ctx.fill(); ctx.stroke();
    txt(ctx, "ActACCU: Σx=10", fx + 225, fy, 12, PAL.blue, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
    rrect(ctx, fx + 320, fy - 14, 140, 28, 6); ctx.fill(); ctx.stroke();
    txt(ctx, "WSUM: Σw=6", fx + 390, fy, 12, PAL.orange, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.purple; ctx.lineWidth = 2;
    rrect(ctx, fx + 480, fy - 14, 160, 28, 6); ctx.fill(); ctx.stroke();
    txt(ctx, "MinACCU: Σmin=6", fx + 560, fy, 12, PAL.purple, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, fx + 660, fy - 14, 240, 28, 6); ctx.fill(); ctx.stroke();
    txt(ctx, "ABS-ASM: 10+6−12=4=Σ|x−w|", fx + 780, fy, 12, PAL.green, "center");
    if (stat) stat.textContent = msg;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1200); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1200);
  draw();
})();

/* ============================================================
   演示 C · 动态比较器波形（电荷共享误差）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");
  // 周期数：6 个高-高位对比较，改进设计第 6 次出错（示意）
  const cycN = 8;
  const errAtOld = 3, errAtNew = 6;

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 C · 动态比较器：OUT 电压随高-高位对比较跌落（电荷共享）", 30, 24, 15, PAL.white, "left");
    const k = cyc % cycN; // 当前周期 0..7

    // 左：电路状态
    const ox = 40, oy = 60;
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.line; ctx.lineWidth = 2;
    rrect(ctx, ox, oy, 300, 160, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "改进比较器（示意）", ox + 150, oy + 22, 13, PAL.white, "center");
    // OUT/OUTB 节点
    const outV = k < errAtNew ? 1.0 : 0.25; // 第6次后出错 → OUT 跌
    const outbV = k < errAtNew ? 1.0 : 0.9;
    // 电压条
    for (let t = 0; t < 6; t++) {
      const y = oy + 50 + t * 20;
      ctx.fillStyle = "#101c2c"; ctx.fillRect(ox + 20, y, 150, 12);
      ctx.fillStyle = PAL.blue; ctx.fillRect(ox + 20, y, 150 * Math.min(1, outV), 12);
      txt(ctx, t === 0 ? "OUT 电压" : "", ox + 182, y + 6, 11, PAL.gray, "left");
    }
    txt(ctx, "OUT 当前电压 ≈ " + outV.toFixed(2) + " V", ox + 20, oy + 185 - 120, 11, PAL.blue, "left");
    txt(ctx, k < errAtNew ? "✓ 未出错：电荷共享还在容错内" : "✗ 出错！连续高-高比较超过 6 次",
      ox + 20, oy + 210 - 120, 12, k < errAtNew ? PAL.green : PAL.red, "left");

    // 右：波形
    const wx = 380, ww = 560, wy = 60, wh = 160;
    ctx.fillStyle = "#0d1622"; ctx.strokeStyle = PAL.line; ctx.lineWidth = 2;
    rrect(ctx, wx, wy, ww, wh, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "OUT 电压波形（每周期一个高-高位对）", wx + ww / 2, wy + 18, 12.5, PAL.white, "center");
    // 网格与参考线
    for (let i = 0; i <= 8; i++) {
      const x = wx + 30 + i * (ww - 60) / 8;
      ctx.strokeStyle = "#1c2c42"; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x, wy + 30); ctx.lineTo(x, wy + wh - 20); ctx.stroke();
    }
    // 理想：1.0 平线；实际：每周期跌落一点，第6次后大幅跌落
    const x0 = wx + 30, x1 = wx + ww - 30;
    for (let i = 0; i < cycN; i++) {
      const vOld = i < errAtOld ? 1.0 : 0.35;
      const vNew = i < errAtNew ? 1.0 - i * 0.02 : 0.3;
      const xa = x0 + i * (x1 - x0) / 8, xb = x0 + (i + 1) * (x1 - x0) / 8;
      const ya = wy + wh - 25 - vOld * 100, yb = wy + wh - 25 - vOld * 100;
      ctx.strokeStyle = PAL.red; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(xa, ya); ctx.lineTo(xb, yb); ctx.stroke();
      const y2a = wy + wh - 25 - vNew * 100, y2b = wy + wh - 25 - vNew * 100;
      ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(xa, y2a); ctx.lineTo(xb, y2b); ctx.stroke();
      // 标记出错点
      if (i === errAtOld) { txt(ctx, "旧[19]出错", xa, ya - 12, 10, PAL.red, "center"); }
      if (i === errAtNew) { txt(ctx, "改进出错", xa, y2a - 12, 10, PAL.green, "center"); }
      // 当前周期高亮
      if (i === k) {
        ctx.fillStyle = "rgba(240,180,70,0.12)";
        ctx.fillRect(xa, wy + 30, (x1 - x0) / 8, wh - 50);
      }
    }
    // 当前高亮点
    const cxp = x0 + k * (x1 - x0) / 8;
    ctx.fillStyle = PAL.orange;
    ctx.beginPath(); ctx.arc(cxp, wy + wh - 25 - (k < errAtNew ? (1.0 - k * 0.02) : 0.3) * 100, 5, 0, 7); ctx.fill();

    // 图例
    txt(ctx, "红=原设计[19]（3 次后出错） · 绿=改进设计（6 次后出错）· 0.65V 以上无错", 30, 262, 12, PAL.gray, "left");
    txt(ctx, "激活正则化：≤5 个「1」（原≤3）→ 只需 0.9% 激活被正则化（原 15%）→ 精度更高", 30, 288, 12.5, PAL.orange, "left");
    if (stat) stat.textContent = "周期 " + (k + 1) + "：OUT=" + (k < errAtNew ? (1.0 - k * 0.02) : 0.30).toFixed(2) + "V（" + (k < errAtNew ? "正常" : "出错") + "）";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1000); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1000);
  draw();
})();
