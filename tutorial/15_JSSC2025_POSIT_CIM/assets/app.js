/* ============================================================
   POSIT CIM (PD-CIM) 教学教程 · 交互脚本
   演示 A POSIT 位结构 · 演示 B 双位 MAC · 演示 C OR 累加
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
   演示 A · POSIT 位结构（S/R/E/M 动态分配）
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");
  const examples = [
    { bits: "0110101", desc: "R=2b(11,+1) · E=0 · M=101(3b) → 大尾数", reg: 2, man: 3 },
    { bits: "01111001", desc: "R=5b(11110,+4) · E=1 · M=01(1b) → 大范围", reg: 5, man: 1 },
    { bits: "0101011", desc: "R=1b(1,0) · E=0 · M=1011(4b) → 最大尾数", reg: 1, man: 4 },
    { bits: "0000101", desc: "R=4b(0001,-3) · E=1 · M=01(1b) → 负大范围", reg: 4, man: 1 },
  ];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 A · POSIT(8,1) 位结构：R 与 M 的位宽动态变化", 30, 24, 15, PAL.white, "left");
    const k = cyc % examples.length;
    const ex = examples[k];
    const bits = ex.bits;
    // S bit
    const bs = 70, bx = 90, by = 70;
    ctx.fillStyle = "#3c2222"; ctx.strokeStyle = PAL.red; ctx.lineWidth = 2;
    rrect(ctx, bx, by, bs, 56, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "S", bx + bs / 2, by + 20, 12, PAL.red, "center");
    txt(ctx, bits[0], bx + bs / 2, by + 40, 18, PAL.white, "center");
    // R bits
    let x = bx + bs;
    for (let i = 1; i <= ex.reg; i++) {
      ctx.fillStyle = "#3c2c1a"; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
      rrect(ctx, x, by, bs, 56, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "R", x + bs / 2, by + 20, 12, PAL.orange, "center");
      txt(ctx, bits[i], x + bs / 2, by + 40, 18, PAL.white, "center");
      x += bs;
    }
    // E bit
    const exIdx = 1 + ex.reg;
    ctx.fillStyle = "#1c3a2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, x, by, bs, 56, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "E", x + bs / 2, by + 20, 12, PAL.green, "center");
    txt(ctx, bits[exIdx], x + bs / 2, by + 40, 18, PAL.white, "center");
    x += bs;
    // M bits
    for (let i = exIdx + 1; i < bits.length; i++) {
      ctx.fillStyle = "#2c2240"; ctx.strokeStyle = PAL.purple; ctx.lineWidth = 2;
      rrect(ctx, x, by, bs, 56, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "M", x + bs / 2, by + 20, 12, PAL.purple, "center");
      txt(ctx, bits[i], x + bs / 2, by + 40, 18, PAL.white, "center");
      x += bs;
    }
    txt(ctx, "位宽：S=1 + R=" + ex.reg + " + E=1 + M=" + ex.man + " = " + bits.length, 90, 150, 13, PAL.white, "left");
    txt(ctx, ex.desc, 90, 180, 14, PAL.orange, "left");
    // R value
    const rstr = bits.slice(1, 1 + ex.reg);
    let rval;
    if (rstr[0] === "1") rval = (rstr.match(/1/g) || []).length - 1;
    else rval = -((rstr.match(/0/g) || []).length);
    txt(ctx, "R 温度计码 '" + rstr + "' → 十进制 R=" + rval + " → 指数 (2^1)^" + rval, 90, 214, 13.5, PAL.green, "left");
    // FP16 comparison
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 2;
    rrect(ctx, 90, 240, 800, 52, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "同样的 8 位：FP8 固定 (1,5,2) 指数范围 [−14,15] → 覆盖不了梯度 [−66,−10]（69.3% 变 0）", 100, 262, 12.5, PAL.blue, "left");
    txt(ctx, "POSIT8 动态分配 → 范围/精度按需 → ≈FP16 精度 · 省 6.25× 能耗", 100, 284, 13.5, PAL.green, "left");
    if (stat) stat.textContent = ex.desc + "（R=" + rval + "）";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1600); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1600);
  draw();
})();

/* ============================================================
   演示 B · 双位 MAC（CPCS）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");
  const Wb = [1, 0, 1]; // 3-bit weight W=101
  const crit = Wb[1] & (Wb[0] & Wb[2]); // S[1] = 0

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 B · CPCS 双位 MAC：W×A[n] + W×A[n+2]（W=101）", 30, 24, 15, PAL.white, "left");
    const k = cyc % 4;
    const a2 = (k >> 1) & 1, a0 = k & 1;
    const an = a2 * 2 + a0;
    // 4-bit CIM unit
    const bs = 80, bx = 90, by = 70;
    for (let i = 0; i < 3; i++) {
      ctx.fillStyle = "#1c3a2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
      rrect(ctx, bx + i * bs, by, bs - 8, 52, 6); ctx.fill(); ctx.stroke();
      txt(ctx, "W[" + i + "]=" + Wb[i], bx + i * bs + (bs - 8) / 2, by + 26, 14, PAL.white, "center");
    }
    ctx.fillStyle = "#3c2a1a"; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
    rrect(ctx, bx + 3 * bs, by, bs - 8, 52, 6); ctx.fill(); ctx.stroke();
    txt(ctx, "关键位 S[1]=" + crit, bx + 3 * bs + (bs - 8) / 2, by + 26, 12, PAL.orange, "center");
    txt(ctx, "空闲单元存预计算关键位（加载时算好）", 90, 146, 12.5, PAL.orange, "left");

    // A bits
    txt(ctx, "输入激活：A[n+2]=" + a2 + "，A[n]=" + a0 + "（组合 " + an + "）", 90, 178, 14, PAL.white, "left");
    // partial product & result
    const P = Wb[0] & a0;
    let outStr, outVal;
    if (an === 0 || an === 1) { outStr = "O = P[2:0] = " + P; outVal = P; }
    else if (an === 2) { outStr = "O = P[2:0]≪2 = " + (P << 2); outVal = P << 2; }
    else { outStr = "O = P[2:0]+P[2:0]≪2（关键位 S[1] 参与）"; outVal = P + (P << 2); }
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 2;
    rrect(ctx, 90, 200, 800, 52, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "部分积 P = W×A[n] = " + Wb[0] + "×" + a0 + " = " + P, 100, 222, 13, PAL.white, "left");
    txt(ctx, outStr, 100, 246, 13.5, PAL.green, "left");
    // throughput comparison
    txt(ctx, "vs 单位串行：每周期 1 个 MAC → 双位 MAC 每周期 2 个 → 吞吐 +38.2%（3b 尾数）", 90, 276, 13, PAL.orange, "left");
    txt(ctx, "2–4b 关联（借位）再 +24.7% · 3b 优先分区（POSIT16）+1.34× · 预计算开销仅 1.6%", 90, 300, 12, PAL.gray, "left");
    if (stat) stat.textContent = "A 组合 " + an + "：" + outStr;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1400); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1400);
  draw();
})();

/* ============================================================
   演示 C · OR 累加（CASU）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 C · CASU：无重叠位用 OR 替代加法（X+0 = X|0）", 30, 24, 15, PAL.white, "left");
    const k = cyc % 3;
    // case 0: no overlap -> OR
    // case 1: overlap both 1 -> need adder
    // case 2: cyclical shift -> make no overlap
    const cases = [
      { A: "1011000", B: "0000101", mode: "纯 OR（无重叠）", ok: true },
      { A: "1011000", B: "0011100", mode: "重叠位有 11 → 需加法器", ok: false },
      { A: "1011000", B: "0000101", mode: "循环交替调度 → 制造无重叠", ok: true },
    ];
    const c = cases[k];
    const bs = 46, bx = 150, by = 70;
    txt(ctx, "模式：" + c.mode, 60, 54, 13.5, c.ok ? PAL.green : PAL.red, "left");
    txt(ctx, "A", 120, by + 14, 12, PAL.blue, "right");
    for (let i = 0; i < 7; i++) {
      const x = bx + i * bs;
      ctx.fillStyle = "#1e3a5c"; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 1;
      rrect(ctx, x, by, bs - 4, 28, 4); ctx.fill(); ctx.stroke();
      txt(ctx, c.A[i], x + (bs - 4) / 2, by + 14, 13, PAL.white, "center");
    }
    txt(ctx, "B", 120, by + 42, 12, PAL.orange, "right");
    for (let i = 0; i < 7; i++) {
      const x = bx + i * bs;
      ctx.fillStyle = "#3c2a1a"; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 1;
      rrect(ctx, x, by + 28, bs - 4, 28, 4); ctx.fill(); ctx.stroke();
      txt(ctx, c.B[i], x + (bs - 4) / 2, by + 42, 13, PAL.white, "center");
    }
    // overlap highlight
    if (k === 1) {
      ctx.strokeStyle = PAL.red; ctx.lineWidth = 3;
      ctx.strokeRect(bx + 2 * bs - 3, by - 3, bs * 2 + 2, 62);
      txt(ctx, "重叠位含 11 → 加法不可省", bx + 2 * bs + bs, by + 80, 11.5, PAL.red, "center");
    }
    // result row
    let res = "";
    for (let i = 0; i < 7; i++) res += (parseInt(c.A[i]) | parseInt(c.B[i])).toString();
    txt(ctx, "A|B = " + res, 150, by + 78, 13.5, PAL.green, "left");
    if (k === 0) {
      txt(ctx, "A+B = " + res + "（无重叠 → 加法=OR）", 150, by + 102, 13.5, PAL.green, "left");
      txt(ctx, "16b 加法器 174.38 nW vs 16b OR 29.75 nW → 省 82.9%", 150, by + 128, 12.5, PAL.gray, "left");
    } else if (k === 1) {
      txt(ctx, "A+B ≠ A|B（有进位）→ 必须加法器 → 进入循环调度", 150, by + 102, 13.5, PAL.red, "left");
      txt(ctx, "但 0&lt;重叠&lt;4 且非全 1 时提前检测仍可用 OR（省 36.1% 加法器）", 150, by + 128, 12.5, PAL.gray, "left");
    } else {
      txt(ctx, "循环移位 A0 的位串行顺序：A0[1..n],A0[0] → 与 A1 无重叠", 150, by + 102, 13.5, PAL.green, "left");
      txt(ctx, "n 次加法 → (n−1) OR + 1 加法 · 无重叠率 +36.4% · 功率 −31.3%", 150, by + 128, 12.5, PAL.orange, "left");
    }
    // summary
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.purple; ctx.lineWidth = 2;
    rrect(ctx, 60, 232, 860, 60, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "CASU 控制：重叠≤0 → 纯 OR ｜ 0~4 → 查替代条件 ｜ &gt;4 → 循环调度加法", 80, 254, 13.5, PAL.white, "left");
    txt(ctx, "加法树功耗占比 23.4%→12.3% · 面积开销仅 2.3% → POSIT16 系统能效 27.61 TFLOPS/W（2.08×）", 80, 278, 12.5, PAL.green, "left");
    if (stat) stat.textContent = c.mode;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1500); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1500);
  draw();
})();
