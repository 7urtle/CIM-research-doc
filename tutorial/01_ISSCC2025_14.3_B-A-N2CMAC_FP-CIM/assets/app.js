/* ============================================================
   FP-CIM 教学教程 · 交互脚本
   演示 A 浮点对齐 · 演示 B 串行对齐 · 演示 C 稀疏性对比
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
   演示 A · 浮点对齐
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 330);
  if (!D) return;
  const { ctx } = D;
  let ea = 10, eb = 4, play = true, t = 0, timer = null;
  const stat = document.getElementById("demoA-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "浮点对齐演示：A = 1.1001011₂ × 2^" + ea + "，B = 1.0110000₂ × 2^" + eb, 30, 24, 15, PAL.white, "left");
    const diff = ea - eb;
    // 数 A（基准，红色）
    const ay = 70;
    txt(ctx, "A（指数大，基准）", 30, ay + 8, 13, PAL.red);
    for (let b = 0; b < 16; b++) {
      const on = (b < 8); // 简单示意尾数
      ctx.fillStyle = on ? "rgba(230,110,90,0.55)" : "rgba(230,110,90,0.18)";
      ctx.fillRect(60 + b * 22, ay + 22, 18, 26);
    }
    // 数 B（指数小，右移）
    const by = 140;
    txt(ctx, "B（指数小，右移 " + Math.max(0, diff) + " 位）", 30, by + 8, 13, PAL.blue);
    const shift = Math.max(0, Math.min(diff, 8));
    if (play) t = (t + 0.01) % 1;
    const animShift = Math.round(shift * t);
    for (let b = 0; b < 16; b++) {
      const srcIdx = b - animShift;
      const on = srcIdx >= 0 && srcIdx < 8;
      ctx.fillStyle = on ? "rgba(30,144,220,0.55)" : "rgba(30,144,220,0.18)";
      ctx.fillRect(60 + b * 22, by + 22, 18, 26);
    }
    // 对齐结果
    const ry = 210;
    txt(ctx, "对齐后（指数对齐到 " + ea + "）", 30, ry + 8, 13, PAL.green);
    for (let b = 0; b < 16; b++) {
      const srcIdx = b - shift;
      const on = srcIdx >= 0 && srcIdx < 8;
      ctx.fillStyle = on ? "rgba(60,190,140,0.55)" : "rgba(60,190,140,0.15)";
      ctx.fillRect(60 + b * 22, ry + 22, 18, 26);
    }
    txt(ctx, "□=1 ▨=0（暗格）", 60, ry + 62, 11, PAL.gray);
    if (stat) stat.textContent = "指数差 " + diff + " → B 右移 " + Math.max(0, diff) + " 位（桶形移位器一次完成 vs 本文每周期 2b）";
  }

  const sEa = document.getElementById("demoA-ea");
  const sEb = document.getElementById("demoA-eb");
  const bPlay = document.getElementById("demoA-play");
  if (sEa) sEa.oninput = function () { ea = parseInt(this.value, 10); draw(); };
  if (sEb) sEb.oninput = function () { eb = parseInt(this.value, 10); draw(); };
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放对齐动画";
    if (play) { clearInterval(timer); timer = setInterval(draw, 50); } else clearInterval(timer);
  };
  if (play) timer = setInterval(draw, 50);
  draw();
})();

/* ============================================================
   演示 B · 串行对齐（SDT 倒计时，三个 LC）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");
  const gaps = [4, 2, 0];   // LC 的对齐差距
  const names = ["LC2 差距4", "LC1 差距2", "LC0 差距0"];
  const colors = [PAL.red, PAL.purple, PAL.green];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const maxv = 6;
    const c = cyc % 8;
    txt(ctx, "周期 " + c + " · SDT = " + (maxv - c), 30, 24, 15, PAL.orange, "left");
    // SDT 条
    for (let i = 0; i < 8; i++) {
      const x = 40 + i * 50;
      ctx.fillStyle = i === c ? "#4a3a1e" : PAL.panel;
      ctx.strokeStyle = i === c ? PAL.orange : PAL.line;
      rrect(ctx, x, 44, 44, 30, 6); ctx.fill(); ctx.stroke();
      txt(ctx, (maxv - i), x + 22, 59, 12, i === c ? PAL.orange : PAL.gray, "center");
    }
    // 三个 LC
    gaps.forEach((gap, li) => {
      const y = 100 + li * 72;
      txt(ctx, names[li], 30, y + 16, 13, colors[li]);
      for (let i = 0; i < 8; i++) {
        const x = 130 + i * 100;
        const state = i < gap ? "存" : "移";
        const active = i === c;
        ctx.fillStyle = state === "存" ? "#1e3c2c" : "#3c2c1e";
        ctx.strokeStyle = active ? colors[li] : PAL.line;
        ctx.lineWidth = active ? 2.5 : 1.5;
        rrect(ctx, x, y, 92, 34, 6); ctx.fill(); ctx.stroke();
        txt(ctx, "周期" + i + "·" + state, x + 46, y + 17, 10.5, active ? colors[li] : PAL.gray, "center");
      }
    });
    txt(ctx, "存 = 尾数进入寄存器链；移 = 每周期输出 2b 对齐后的尾数", 40, 312, 12, PAL.gray);
    if (stat) stat.textContent = "SDT 统一节奏：" + (c < 3 ? "LC2 还在存、LC0 已在移" : "全部进入移位态，同步输出");
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 550); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 550);
  draw();
})();

/* ============================================================
   演示 C · 2C vs 符号-数值稀疏性
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let t = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");

  // 权重样本（含负值），8b
  const weights = [85, -37, 120, -64, 12, -90, 55, -7, 100, -48, 30, -15, 70, -23, 95, -81];

  function twos(v) {
    let x = v < 0 ? (1 << 8) + v : v;
    const s = x.toString(2);
    return ("00000000" + s).slice(-8);
  }
  function mag(v) {
    const a = Math.abs(v);
    const s = a.toString(2);
    return (v < 0 ? "1" : "0") + ("0000000" + s).slice(-7);
  }

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "位级稀疏性对比：同一组权重，两种格式（样本 " + weights.length + " 个）", 30, 24, 15, PAL.white, "left");
    const shown = Math.max(4, Math.floor(t * weights.length));
    // 2C
    txt(ctx, "2 的补码", 60, 60, 14, PAL.red);
    let ones2c = 0, onesMag = 0, total = 0;
    for (let i = 0; i < shown; i++) {
      const y = 78 + (i % 10) * 22;
      const col = Math.floor(i / 10);
      const x = 60 + col * 240;
      const s2 = twos(weights[i]);
      const sm = mag(weights[i]);
      for (let b = 0; b < 8; b++) {
        const xb = x + b * 20;
        ctx.fillStyle = s2[b] === "1" ? "rgba(230,110,90,0.7)" : "rgba(230,110,90,0.15)";
        ctx.fillRect(xb, y, 16, 16);
        if (s2[b] === "1") ones2c++;
      }
      // 符号-数值
      const x2 = x + 460;
      for (let b = 0; b < 8; b++) {
        const xb = x2 + b * 20;
        ctx.fillStyle = sm[b] === "1" ? "rgba(60,190,140,0.7)" : "rgba(60,190,140,0.15)";
        ctx.fillRect(xb, y, 16, 16);
        if (sm[b] === "1") onesMag++;
      }
      total += 8;
    }
    txt(ctx, "非零位数: " + ones2c + " / " + total, 60, 78 + Math.min(shown, 10) * 22 + 14, 12.5, PAL.red);
    txt(ctx, "非零位数: " + onesMag + " / " + total, 520, 78 + Math.min(shown, 10) * 22 + 14, 12.5, PAL.green);
    const sp2 = 1 - ones2c / Math.max(1, total);
    const spM = 1 - onesMag / Math.max(1, total);
    if (total > 0) {
      txt(ctx, "稀疏性 2C: " + (sp2 * 100).toFixed(0) + "% · 符号-数值: " + (spM * 100).toFixed(0) + "%",
        60, 276, 13, spM > sp2 ? PAL.green : PAL.white);
    }
    if (stat) stat.textContent = "负权重在 2C 下数值位被取反填 1；符号-数值只翻符号位 → 稀疏性更高（论文实测 1.83×）";
  }

  function tick() { t = Math.min(1, t + 0.03); draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 120); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { t = 0; draw(); };
  if (play) timer = setInterval(tick, 120);
  draw();
})();
