/* ============================================================
   TCL-CIM 教学教程 · 交互脚本
   演示 A TCL 数沿 · 演示 B 10 相时序 · 演示 C 稀疏对比
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
   演示 A · TCL 数沿
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let bits = [1, 1, 0, 0, 1, 0, 0, 1];
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const c = cyc % 8;
    txt(ctx, "TCL 数沿演示 · 位积 = [" + bits.join(",") + "]", 30, 24, 15, PAL.white, "left");
    // MMU 链
    let level = 1;
    for (let k = 0; k < 8; k++) {
      const x0 = 90 + k * 100;
      const active = k === c;
      const col = bits[k] === 1 ? PAL.red : PAL.gray;
      ctx.fillStyle = active ? "#3a2a26" : PAL.panel;
      ctx.strokeStyle = col; ctx.lineWidth = active ? 2.5 : 1.5;
      rrect(ctx, x0, 70, 88, 80, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "MMU" + k, x0 + 44, 90, 12, col, "center");
      txt(ctx, "P=" + bits[k], x0 + 44, 110, 12, PAL.white, "center");
      if (active) {
        txt(ctx, bits[k] ? "取反!" : "直通", x0 + 44, 132, 11, bits[k] ? PAL.orange : PAL.gray, "center");
      }
      if (k > 0) {
        ctx.strokeStyle = PAL.line; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(x0 - 12, 110); ctx.lineTo(x0, 110); ctx.stroke();
      }
    }
    // 起点 VDD 与终点 CNT
    ctx.strokeStyle = PAL.green; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(70, 110); ctx.lineTo(90, 110); ctx.stroke();
    txt(ctx, "VDD", 45, 100, 11, PAL.green, "center");
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
    rrect(ctx, 890, 70, 70, 80, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "CNT", 925, 110, 12, PAL.orange, "center");
    // 当前电平与计数
    const seen = bits.slice(0, c + 1);
    const cnt = seen.filter(b => b === 1).length;
    const parity = cnt % 2;
    ctx.strokeStyle = PAL.blue; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(90 + c * 100 + 44, 60); ctx.lineTo(90 + c * 100 + 44, 175); ctx.stroke();
    txt(ctx, "电平（VDD 起点，每遇 1 取反）：" + (parity === 0 ? "高" : "低"), 90, 190, 14, PAL.blue, "left");
    txt(ctx, "CNT 已数到 " + cnt + " 个沿 = 前 " + (c + 1) + " 位中 1 的个数", 90, 216, 14, PAL.orange, "left");
    txt(ctx, "完整 8 位列和 = " + bits.reduce((a, b) => a + b, 0), 90, 242, 15, PAL.green, "left");
    txt(ctx, "0 的 MMU 直通不翻转 → 稀疏自适应省电", 90, 270, 12.5, PAL.gray, "left");
    if (stat) stat.textContent = "列和 " + bits.reduce((a, b) => a + b, 0) + " · 非零位 " + bits.reduce((a, b) => a + b, 0) + " 个";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  const bSparse = document.getElementById("demoA-sparse");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 500); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (bSparse) bSparse.onclick = function () {
    bits = [1, 0, 0, 0, 1, 0, 0, 0];
    cyc = 0; draw();
  };
  if (play) timer = setInterval(tick, 500);
  draw();
})();

/* ============================================================
   演示 B · 10 相时序
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const cur = cyc % 10;
    txt(ctx, "10 相发生器 · 当前相位 Ph" + cur, 30, 24, 15, PAL.orange, "left");
    for (let k = 0; k < 10; k++) {
      const x0 = 60 + k * 88;
      const active = k === cur;
      const col = k < 8 ? PAL.red : (k === 8 ? PAL.green : PAL.blue);
      ctx.fillStyle = active ? "#4a3826" : PAL.panel;
      ctx.strokeStyle = active ? col : PAL.line;
      ctx.lineWidth = active ? 2.5 : 1.5;
      rrect(ctx, x0, 60, 78, 70, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "Ph" + k, x0 + 39, 82, 13, active ? col : PAL.gray, "center");
      const role = k < 8 ? "MMU" + k : (k === 8 ? "合并加" : "加法树");
      txt(ctx, role, x0 + 39, 104, 11, PAL.white, "center");
    }
    // 波形
    for (let k = 0; k < 10; k++) {
      const x0 = 60 + k * 88;
      ctx.fillStyle = k <= cur ? PAL.orange : "#28384e";
      ctx.fillRect(x0 + 8, 170, 70, 10);
    }
    const phaseInfo = cur < 8
      ? "Ph" + cur + "：使能 MMU" + cur + "，边沿向链尾推进一格（乘法）"
      : cur === 8 ? "Ph8：打开合并加法器（此前输入强制接地，无毛刺）" : "Ph9：打开块内加法树 → 生成 16b 乘积";
    txt(ctx, phaseInfo, 60, 210, 14, PAL.white, "left");
    txt(ctx, "加法器只在 Ph8/Ph9 工作 → 其余时间零翻转 → 能效 +42%", 60, 238, 13, PAL.green, "left");
    txt(ctx, "对比：传统方案加法器全程开闸，乘法阶段的毛刺白烧电", 60, 262, 12, PAL.gray, "left");
    if (stat) stat.textContent = "周期 " + (cyc + 1) + " · 相位 Ph" + cur;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 600); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 600);
  draw();
})();

/* ============================================================
   演示 C · 稀疏对比（无符号/有符号示例）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const c = cyc % 12;
    // 两种权重示例
    const twosW = [1, 1, 1, 1, 1, 0, 0, 1];       // -7 in 2C
    const magW = [1, 0, 0, 0, 0, 1, 1, 1];         // -7 in sign-mag (1 000 0111)
    txt(ctx, "同一权重 −7 的两种存储格式（位级稀疏性对比）", 30, 24, 15, PAL.white, "left");
    txt(ctx, "2 的补码：1111 1001（数值位几乎全 1）", 60, 60, 13, PAL.red);
    for (let k = 0; k < 8; k++) {
      const x0 = 380 + k * 42;
      ctx.fillStyle = twosW[k] ? "rgba(230,110,90,0.75)" : "rgba(230,110,90,0.15)";
      ctx.fillRect(x0, 48, 34, 26);
      txt(ctx, twosW[k], x0 + 17, 61, 11, PAL.white, "center");
    }
    txt(ctx, "符号-数值：1 000 0111（只有符号位+数值）", 60, 110, 13, PAL.green);
    for (let k = 0; k < 8; k++) {
      const x0 = 380 + k * 42;
      ctx.fillStyle = magW[k] ? "rgba(60,190,140,0.75)" : "rgba(60,190,140,0.15)";
      ctx.fillRect(x0, 98, 34, 26);
      txt(ctx, magW[k], x0 + 17, 111, 11, PAL.white, "center");
    }
    const ones2c = twosW.reduce((a, b) => a + b, 0);
    const onesMag = magW.reduce((a, b) => a + b, 0);
    txt(ctx, "2C 非零位：" + ones2c + "/8", 60, 160, 14, PAL.red);
    txt(ctx, "符号-数值非零位：" + onesMag + "/8", 60, 188, 14, PAL.green);
    txt(ctx, "→ 2C 的负权重把位“填满”→ 加法树/MMU 翻转多；符号-数值保持稀疏 → TCL 链上 0 直通、更省电", 60, 230, 13, PAL.gray);
    txt(ctx, "（论文实测：符号-数值比 2C 的负权重位级稀疏性提升 1.83×，见 01 号论文 §6）", 60, 256, 12, PAL.gray);
    if (stat) stat.textContent = "2C 非零位 " + ones2c + " vs 符号-数值 " + onesMag + "（本例 −7）";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 800); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 800);
  draw();
})();
