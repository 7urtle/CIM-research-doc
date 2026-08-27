/* ============================================================
   HUNBN 数字 CIM SoC 教学教程 · 交互脚本
   演示 A PE vs DIMC · 演示 B 1bitx2bit 乘法 · 演示 C 同步时序
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
   演示 A · PE vs DIMC（权重搬移 vs 就地）
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 A · 数字 PE vs DIMC：权重从哪里来？", 30, 24, 15, PAL.white, "left");
    const k = cyc % 2;
    // ---- PE side ----
    txt(ctx, "数字 PE 阵列", 150, 58, 14, PAL.red, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.red; ctx.lineWidth = 2;
    rrect(ctx, 40, 72, 220, 60, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "权重 SRAM（片外）", 150, 92, 12.5, PAL.red, "center");
    txt(ctx, "每周期都要读", 150, 112, 11, PAL.gray, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.line; ctx.lineWidth = 2;
    rrect(ctx, 300, 72, 180, 60, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "PE（乘法器+加法树）", 390, 92, 12.5, PAL.white, "center");
    txt(ctx, "本地寄存器存权重副本", 390, 112, 11, PAL.gray, "center");
    // moving weight animation
    const t = (cyc % 10) / 10;
    const mx = 262 + t * 36;
    ctx.fillStyle = PAL.red;
    ctx.beginPath(); ctx.arc(mx, 102, 6, 0, 7); ctx.fill();
    txt(ctx, "权重每周期搬一次", 150, 160, 12, PAL.red, "center");
    txt(ctx, "搬移能耗 ≫ 计算能耗 → 瓶颈", 150, 186, 11.5, PAL.gray, "center");
    txt(ctx, "寄存器副本多 → 面积/能耗大", 150, 212, 11.5, PAL.gray, "center");
    txt(ctx, "▲ 高能耗", 390, 160, 13, PAL.red, "center");
    ctx.fillStyle = "#1c2838"; ctx.fillRect(60, 240, 380, 22);
    ctx.fillStyle = PAL.red; ctx.fillRect(60, 240, 380, 22);
    txt(ctx, "权重搬移占比大（示意）", 250, 284, 12, PAL.red, "center");

    // ---- DIMC side ----
    txt(ctx, "DIMC（本论文）", 650, 58, 14, PAL.green, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 540, 72, 180, 60, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "6T SRAM（存权重）", 630, 92, 12.5, PAL.green, "center");
    txt(ctx, "权重就地存储", 630, 112, 11, PAL.gray, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 750, 72, 180, 60, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "本地 MAC 单元", 840, 92, 12.5, PAL.green, "center");
    txt(ctx, "就地乘加", 840, 112, 11, PAL.gray, "center");
    ctx.strokeStyle = PAL.green; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(724, 102); ctx.lineTo(746, 102); ctx.stroke();
    txt(ctx, "权重零搬移 → 省 28% 功耗 [23]", 650, 160, 12.5, PAL.green, "center");
    txt(ctx, "前提：整模型装得进阵列", 650, 186, 12, PAL.gray, "center");
    txt(ctx, "HUNBN：508 kB/mm² → 2.36M 权重", 650, 212, 12, PAL.green, "center");
    ctx.fillStyle = "#1c2838"; ctx.fillRect(560, 240, 380, 22);
    ctx.fillStyle = PAL.green; ctx.fillRect(560, 240, 300, 22);
    txt(ctx, "权重搬移≈0（示意）", 750, 284, 12, PAL.green, "center");

    if (stat) stat.textContent = k === 0 ? "PE：权重每周期从 SRAM 搬入（红色动画）" : "DIMC：权重就地存储，只有开机一次性加载";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 900); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 900);
  draw();
})();

/* ============================================================
   演示 B · 1-bit × 2-bit 乘法（BL/BLB 双线）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");
  const wbits = [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1]; // 12 sample weight bits
  const i2 = [3, 2, 1, 3, 0, 2]; // 6x 2-bit activations (values 0..3)

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 B · 1-bit×2-bit 乘法：BL 算 bit0、BLB 算 bit1", 30, 24, 15, PAL.white, "left");
    txt(ctx, "同权位权重组（24 位，示例 12 位）", 60, 54, 12.5, PAL.blue, "left");
    const bs = 52, bx = 60, by = 66;
    for (let i = 0; i < 12; i++) {
      const x = bx + i * bs;
      ctx.fillStyle = wbits[i] ? "#1e4a76" : "#101c2c";
      ctx.strokeStyle = PAL.line; ctx.lineWidth = 1;
      rrect(ctx, x, by, bs - 6, 30, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(wbits[i]), x + (bs - 6) / 2, by + 15, 13, PAL.white, "center");
    }
    txt(ctx, "W（BL）", bx + bs * 12 + 10, by + 15, 11, PAL.blue, "left");
    txt(ctx, "WB（BLB）", bx + bs * 12 + 10, by + 45, 11, PAL.orange, "left");
    for (let i = 0; i < 12; i++) {
      const x = bx + i * bs;
      ctx.fillStyle = wbits[i] ? "#3c2a1e" : "#2a1e14";
      ctx.strokeStyle = PAL.orange; ctx.lineWidth = 1;
      rrect(ctx, x, by + 30, bs - 6, 30, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(wbits[i] ? 0 : 1), x + (bs - 6) / 2, by + 45, 13, PAL.white, "center");
    }
    txt(ctx, "2-bit 输入激活（示例 6 组）", 60, 142, 12.5, PAL.purple, "left");
    const k = cyc % 6;
    for (let i = 0; i < 6; i++) {
      const x = bx + i * bs;
      ctx.fillStyle = i === k ? "#3a2a1e" : "#1c2838";
      ctx.strokeStyle = i === k ? PAL.orange : PAL.line; ctx.lineWidth = i === k ? 3 : 1;
      rrect(ctx, x, by + 44, bs - 6, 30, 4); ctx.fill(); ctx.stroke();
      txt(ctx, "I=" + i2[i], x + (bs - 6) / 2, by + 59, 11, PAL.white, "center");
    }
    const wb = wbits[k], inv = wb ? 0 : 1;
    const a1 = (i2[k] >> 1) & 1, a0 = i2[k] & 1;
    const p0 = wb & a0, p1 = inv & a1;
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 60, 200, 860, 60, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "组" + k + "：W=" + wb + "（BL），WB=" + inv + "（BLB）；I[1:0]=" + i2[k].toString(2).padStart(2, "0"),
      70, 224, 14, PAL.white, "left");
    txt(ctx, "部分积 BL 支路 = W×I[0] = " + wb + "×" + a0 + " = " + p0 +
      "　　·　　部分积 BLB 支路 = WB×I[1] = " + inv + "×" + a1 + " = " + p1,
      70, 248, 13.5, PAL.green, "left");
    txt(ctx, "2-bit 串行重复 → 4b×4b MAC 只需 2 周期（比传统位串行快 2 倍）", 60, 290, 13.5, PAL.orange, "left");
    if (stat) stat.textContent = "组" + k + "：W×I[0]=" + p0 + "，WB×I[1]=" + p1;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1300); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1300);
  draw();
})();

/* ============================================================
   演示 C · 同步时序（pe/re 分周期 + 刷新）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");
  const ncyc = 8;

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 C · 同步 DIMC 操作：预充（pe）与读（re）分周期 → 免延迟线", 30, 24, 15, PAL.white, "left");
    const k = cyc % ncyc;
    const x0 = 80, x1 = 900, y0 = 60, y1 = 240;
    const cw = (x1 - x0) / ncyc;
    ctx.strokeStyle = "#1c2c42"; ctx.lineWidth = 1;
    for (let i = 0; i <= ncyc; i++) {
      const x = x0 + i * cw;
      ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, y1); ctx.stroke();
    }
    function yv(v, hi) { return y1 - 30 - (v / hi) * (y1 - y0 - 60); }
    txt(ctx, "CLK", x0 - 12, y0 + 12, 11, PAL.white, "right");
    for (let i = 0; i < ncyc; i++) {
      const x = x0 + i * cw;
      ctx.strokeStyle = "#4a6a8a"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x, yv(1, 1)); ctx.lineTo(x + cw / 2, yv(1, 1)); ctx.lineTo(x + cw / 2, yv(0, 1)); ctx.lineTo(x + cw, yv(0, 1)); ctx.stroke();
    }
    txt(ctx, "pe", x0 - 12, y0 + 48, 11, PAL.blue, "right");
    for (let i = 0; i < ncyc; i++) {
      const x = x0 + i * cw;
      const on = (i % 2 === 0);
      ctx.strokeStyle = on ? PAL.blue : "#1c2c42"; ctx.lineWidth = on ? 2.5 : 1.5;
      ctx.beginPath();
      ctx.moveTo(x, yv(0, 1));
      ctx.lineTo(x + cw * 0.15, yv(0, 1));
      ctx.lineTo(x + cw * 0.15, yv(on ? 1 : 0, 1));
      ctx.lineTo(x + cw * 0.5, yv(on ? 1 : 0, 1));
      ctx.lineTo(x + cw * 0.5, yv(0, 1));
      ctx.lineTo(x + cw, yv(0, 1));
      ctx.stroke();
    }
    txt(ctx, "re", x0 - 12, y0 + 82, 11, PAL.orange, "right");
    for (let i = 0; i < ncyc; i++) {
      const x = x0 + i * cw;
      const on = (i % 2 === 1);
      ctx.strokeStyle = on ? PAL.orange : "#1c2c42"; ctx.lineWidth = on ? 2.5 : 1.5;
      ctx.beginPath();
      ctx.moveTo(x, yv(0, 1));
      ctx.lineTo(x + cw * 0.25, yv(0, 1));
      ctx.lineTo(x + cw * 0.25, yv(on ? 1 : 0, 1));
      ctx.lineTo(x + cw * 0.6, yv(on ? 1 : 0, 1));
      ctx.lineTo(x + cw * 0.6, yv(0, 1));
      ctx.lineTo(x + cw, yv(0, 1));
      ctx.stroke();
    }
    txt(ctx, "计算", x0 - 12, y0 + 118, 11, PAL.green, "right");
    for (let i = 1; i < ncyc; i += 2) {
      const x = x0 + i * cw;
      ctx.fillStyle = "rgba(60,190,140,0.15)";
      ctx.fillRect(x + cw * 0.6, y0 + 100, cw * 1.4, 24);
    }
    txt(ctx, "读后连续多周期计算（SUM=BL×不同输入）", x0 + 10, y0 + 128, 11, PAL.green, "left");
    txt(ctx, "刷新", x0 - 12, y0 + 156, 11, PAL.purple, "right");
    for (let i = 2; i < ncyc; i += 4) {
      const x = x0 + i * cw + cw * 0.8;
      ctx.strokeStyle = PAL.purple; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x, yv(0, 1)); ctx.lineTo(x + 4, yv(1, 1)); ctx.lineTo(x + 12, yv(1, 1)); ctx.lineTo(x + 16, yv(0, 1)); ctx.stroke();
    }
    ctx.fillStyle = "rgba(240,180,70,0.12)";
    ctx.fillRect(x0 + k * cw, y0, cw, y1 - y0);
    ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
    ctx.strokeRect(x0 + k * cw, y0, cw, y1 - y0);
    const phase = k % 2 === 0 ? "预充周期（pe）" : "读+计算周期（re）";
    txt(ctx, "周期 " + (k + 1) + "：" + phase, 60, 270, 14, PAL.orange, "left");
    txt(ctx, "Φ 与 WL 永远不同周期 → 无破坏性读 → 免延迟线", 60, 294, 13, PAL.white, "left");
    txt(ctx, "→ 读临界路径缩短 · MAC 逻辑不在临界路径 → 可降电压省能", 60, 318, 12, PAL.gray, "left");
    if (stat) stat.textContent = "周期 " + (k + 1) + "：" + phase;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 900); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 900);
  draw();
})();
