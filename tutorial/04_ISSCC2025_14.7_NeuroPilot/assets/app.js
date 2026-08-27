/* ============================================================
   NeuroPilot 教学教程 · 交互脚本
   演示 A 波前传播 · 演示 B DDS vs SDS · 演示 C TsCFP
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

/* 网格绘制辅助 */
function gridWaves(ctx, opts) {
  const { gx, gy, cell, rows, cols, cyc, obstacles, start, end, dual } = opts;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = gx + c * cell, y = gy + r * cell;
      const isObs = obstacles.some(o => o[0] === c && o[1] === r);
      const ds = Math.abs(r - start[1]) + Math.abs(c - start[0]);
      let reachedS = ds <= cyc;
      let fill, outline;
      if (isObs) { fill = "#3a2620"; outline = PAL.red; }
      else if (dual) {
        const de = Math.abs(r - end[1]) + Math.abs(c - end[0]);
        const reachedE = de <= cyc;
        if (reachedS && reachedE) { fill = "#3a3a1e"; outline = PAL.orange; }
        else if (reachedS) { fill = "#1e3c2c"; outline = PAL.green; }
        else if (reachedE) { fill = "#3c2a1e"; outline = PAL.red; }
        else { fill = "#141c2a"; outline = PAL.line; }
      } else {
        if (reachedS) { fill = "#1e3c2c"; outline = PAL.green; }
        else { fill = "#141c2a"; outline = PAL.line; }
      }
      ctx.fillStyle = fill; ctx.strokeStyle = outline;
      ctx.lineWidth = reachedS ? 2 : 1;
      rrect(ctx, x, y, cell - 4, cell - 4, 4); ctx.fill(); ctx.stroke();
    }
  }
  // start / end
  ctx.fillStyle = PAL.green;
  ctx.beginPath(); ctx.arc(gx + start[0] * cell + cell / 2, gy + start[1] * cell + cell / 2, 8, 0, 6.28); ctx.fill();
  txt(ctx, "S", gx + start[0] * cell + cell / 2, gy + start[1] * cell + cell / 2, 9, "#0a1119", "center");
  if (end) {
    ctx.fillStyle = PAL.red;
    ctx.beginPath(); ctx.arc(gx + end[0] * cell + cell / 2, gy + end[1] * cell + cell / 2, 8, 0, 6.28); ctx.fill();
    txt(ctx, "E", gx + end[0] * cell + cell / 2, gy + end[1] * cell + cell / 2, 9, "#0a1119", "center");
  }
}

/* ============================================================
   演示 A · 波前传播（SDS）
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");
  const obstacles = [[4, 3], [5, 3], [6, 3], [7, 3], [5, 4], [6, 4], [7, 4]];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "波前传播（SDS）：信号从 START 逐层扩散，绕过障碍", 30, 24, 15, PAL.white, "left");
    gridWaves(ctx, { gx: 90, gy: 50, cell: 30, rows: 8, cols: 12, cyc: cyc % 14, obstacles, start: [1, 6], end: [10, 1], dual: false });
    txt(ctx, "绿色环 = 波前已到达；红色 = 障碍；波前绕行继续扩散", 90, 300 - 8, 12, PAL.gray, "left");
    if (stat) stat.textContent = "扩散距离 " + (cyc % 14) + " · 波前逐层传播（8 邻接）";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 450); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 450);
  draw();
})();

/* ============================================================
   演示 B · DDS vs SDS
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");
  const obstacles = [[5, 2], [6, 2], [7, 2], [5, 3], [6, 3]];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const c = cyc % 12;
    // 左：SDS
    txt(ctx, "SDS 单向（波前覆盖整图）", 180, 26, 14, PAL.red);
    gridWaves(ctx, { gx: 60, gy: 50, cell: 30, rows: 8, cols: 9, cyc: c, obstacles, start: [1, 6], end: null, dual: false });
    // 右：DDS
    txt(ctx, "DDS 双向（各走一半，交汇）", 650, 26, 14, PAL.green);
    gridWaves(ctx, { gx: 530, gy: 50, cell: 30, rows: 8, cols: 9, cyc: c, obstacles, start: [1, 6], end: [7, 1], dual: true });
    txt(ctx, "左：单向波前要铺满大半个图才能到 END", 60, 300 - 8, 11.5, PAL.gray, "left");
    txt(ctx, "右：两股波前各走一半就在中间交汇 → 时间 −2.1×、功耗 −1.13×", 530, 300 - 8, 11.5, PAL.orange, "left");
    if (stat) stat.textContent = "扩散距离 " + c + "：SDS 覆盖 vs DDS 两股波前交汇";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 500); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 500);
  draw();
})();

/* ============================================================
   演示 C · TsCFP
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
    const k = cyc % 3;
    txt(ctx, "TsCFP 三步：" + ["① 生成最小清晰粗图", "② 粗图最短路径（走廊）", "③ 沿走廊求细路径"][k], 30, 24, 15, [PAL.blue, PAL.purple, PAL.green][k], "left");
    if (k === 0) {
      // 粗图网格
      for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 12; c++) {
          const x = 100 + c * 60, y = 60 + r * 34;
          const pass = (r + c) % 5 !== 0;
          ctx.fillStyle = pass ? "#1e3c2c" : "#3a2620";
          ctx.strokeStyle = pass ? PAL.green : PAL.red; ctx.lineWidth = 1;
          rrect(ctx, x, y, 56, 30, 4); ctx.fill(); ctx.stroke();
        }
      }
      txt(ctx, "1024×1024 → 迭代降低分辨率 → 最小清晰粗图（绿=可通行）", 100, 290, 12, PAL.gray, "left");
    } else if (k === 1) {
      for (let kk = 0; kk < 8; kk++) {
        const x0 = 100 + kk * 105;
        ctx.fillStyle = "#242a3e"; ctx.strokeStyle = PAL.purple; ctx.lineWidth = 2;
        rrect(ctx, x0, 90, 95, 110, 8); ctx.fill(); ctx.stroke();
        txt(ctx, "段" + kk, x0 + 47, 112, 12, PAL.purple, "center");
        if (kk > 0) txt(ctx, "→", x0 - 14, 145, 13, PAL.gray, "center");
      }
      ctx.strokeStyle = PAL.orange; ctx.lineWidth = 6;
      ctx.beginPath(); ctx.moveTo(110, 230); ctx.lineTo(920, 230); ctx.stroke();
      txt(ctx, "粗路径 = 走廊（橙色）· 每段由上一段 END + 原图方向决定起点", 100, 290, 12, PAL.orange, "left");
    } else {
      for (let kk = 0; kk < 5; kk++) {
        const x0 = 100 + kk * 170;
        ctx.fillStyle = "#1e3c2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
        rrect(ctx, x0, 80, 160, 180, 8); ctx.fill(); ctx.stroke();
        txt(ctx, "细条带" + kk, x0 + 80, 100, 11, PAL.green, "center");
        ctx.strokeStyle = PAL.green; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(x0 + 20, 180); ctx.lineTo(x0 + 140, 180); ctx.stroke();
      }
      txt(ctx, "沿走廊切细条带 → 逐段精算 → 拼接（旧金山例：373.82ns / 512.5pJ / 1279.8L）", 100, 290, 12, PAL.gray, "left");
    }
    if (stat) stat.textContent = "步骤 " + (k + 1) + "/3：" + ["粗图", "走廊", "细路径"][k];
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1800); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1800);
  draw();
})();
