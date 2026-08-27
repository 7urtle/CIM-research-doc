/* ============================================================
   两周期 CIM 处理器教学教程 · 交互脚本
   演示 A 乘法分解 · 演示 B Winograd · 演示 C 激活压缩
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
   演示 A · 乘法分解（周期数）
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");
  const schemes = [
    { name: "位串行", cycles: 8, col: PAL.red, per: 1 },
    { name: "Radix4 (Booth)", cycles: 4, col: PAL.purple, per: 3 },
    { name: "Radix16 (本文)", cycles: 2, col: PAL.green, per: 5 },
  ];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "INT8 乘法分解：每周期算的位数 vs 周期数", 30, 24, 15, PAL.white, "left");
    schemes.forEach((s, i) => {
      const y = 60 + i * 70;
      ctx.fillStyle = "#14263c"; ctx.strokeStyle = s.col; ctx.lineWidth = 2;
      rrect(ctx, 60, y, 160, 44, 8); ctx.fill(); ctx.stroke();
      txt(ctx, s.name + "（" + s.per + " bit/周期）", 70, y + 22, 12.5, s.col, "left");
      // 周期脉冲
      for (let k = 0; k < s.cycles; k++) {
        const x = 260 + k * 60;
        const lit = k <= cyc % s.cycles;
        ctx.fillStyle = lit ? s.col : "#1c2838";
        rrect(ctx, x, y + 8, 46, 28, 6); ctx.fill(); ctx.stroke();
        txt(ctx, "周期" + k, x + 23, y + 22, 10, lit ? "#0a1119" : PAL.gray, "center");
      }
      txt(ctx, "共 " + s.cycles + " 周期", 260 + s.cycles * 60 + 14, y + 22, 12.5, s.col, "left");
    });
    txt(ctx, "Radix16 把周期压到 2 → 但每周期加权部分积更复杂 → LUT 救场（动态功耗 −21.7%）", 60, 280, 13, PAL.orange, "left");
    if (stat) stat.textContent = "周期推进：位串行 8 · Radix4 4 · Radix16 2";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
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
   演示 B · Winograd F4（3×3 conv → EWMM 乘法 ÷4）
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
    const k = cyc % 3;
    txt(ctx, "Winograd F4：乘法从 9 次降到 2~4 次（÷4）", 30, 24, 15, PAL.white, "left");
    if (k === 0) {
      // 空间域 3x3 卷积
      txt(ctx, "空间域：3×3 卷积（9 次乘法/输出块）", 60, 60, 13, PAL.red);
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const x = 80 + c * 50, y = 80 + r * 40;
          ctx.fillStyle = "#3c2a26"; ctx.strokeStyle = PAL.red; ctx.lineWidth = 1.5;
          rrect(ctx, x, y, 44, 34, 4); ctx.fill(); ctx.stroke();
        }
      }
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const x = 340 + c * 50, y = 80 + r * 40;
          ctx.fillStyle = "#2a243e"; ctx.strokeStyle = PAL.purple; ctx.lineWidth = 1.5;
          rrect(ctx, x, y, 44, 34, 4); ctx.fill(); ctx.stroke();
        }
      }
      txt(ctx, "激活块 d × 卷积核 g → 9 个乘法", 300, 210, 12.5, PAL.gray, "center");
    } else if (k === 1) {
      txt(ctx, "Winograd 域：变换后做逐元素乘加（EWMM）", 60, 60, 13, PAL.blue);
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const x = 100 + c * 60, y = 90 + r * 34;
          ctx.fillStyle = "#1e3c56"; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 1.5;
          rrect(ctx, x, y, 54, 28, 4); ctx.fill(); ctx.stroke();
          if (r % 3 === 0 && c % 3 === 0) {
            ctx.fillStyle = PAL.orange;
            ctx.beginPath(); ctx.arc(x + 27, y + 14, 5, 0, 6.28); ctx.fill();
          }
        }
      }
      txt(ctx, "F4：4×4 变换块 → 只有 4 个“真正的乘法”（橙点）→ ÷4", 80, 260, 12.5, PAL.orange, "left");
    } else {
      txt(ctx, "逆变换 Aᵀ()A：还原空间域输出（加/减，便宜）", 60, 60, 13, PAL.green);
      for (let r = 0; r < 4; r++) {
        const x = 200 + r * 80;
        ctx.fillStyle = "#1e3c2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
        rrect(ctx, x, 120, 70, 44, 8); ctx.fill(); ctx.stroke();
        txt(ctx, "输出块 " + r, x + 35, 142, 11, PAL.green, "center");
      }
      txt(ctx, "→ 净加速 3.32×（F4）· 混合按层选 → 2.59× 且精度仅 −0.6%", 60, 210, 13.5, PAL.white, "left");
      txt(ctx, "变换矩阵元素为 0/±1/±½ → 变换 = 加/减/移位，几乎不耗“乘法”", 60, 240, 12.5, PAL.gray, "left");
    }
    if (stat) stat.textContent = ["空间域 9 乘法", "Winograd 域 4 乘法（÷4）", "逆变换还原"][k];
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
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
   演示 C · 激活压缩（连续 4 零跳过）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");
  const acts = [5, 0, 0, 0, 0, 3, 0, 0, 0, 0, 7, 1, 0, 0, 0, 0, 2, 6];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "激活压缩：连续 4 个零整组跳过（宏级调度）", 30, 24, 15, PAL.white, "left");
    const shown = Math.min(acts.length, 6 + (cyc % (acts.length - 6)));
    let sent = 0, skipped = 0;
    for (let i = 0; i < shown; i++) {
      const x = 70 + (i % 12) * 70, y = 60 + Math.floor(i / 12) * 60;
      const v = acts[i];
      const inZeroRun = v === 0 && i % 4 !== 0;
      const isSkipGroup = v === 0 && i % 4 === 0;
      ctx.fillStyle = v !== 0 ? "#1e3c2c" : (i % 4 === 0 ? "#3a2620" : "#141c2a");
      ctx.strokeStyle = v !== 0 ? PAL.green : (i % 4 === 0 ? PAL.red : PAL.line);
      ctx.lineWidth = v !== 0 ? 2 : 1.5;
      rrect(ctx, x, y, 60, 40, 6); ctx.fill(); ctx.stroke();
      txt(ctx, v, x + 30, y + 20, 13, PAL.white, "center");
      if (v !== 0) sent++;
      else if (i % 4 === 0) skipped += 4;
      // 跳过标注
      if (v === 0 && i % 4 === 0) txt(ctx, "跳过×4", x + 30, y - 8, 9, PAL.red, "center");
    }
    txt(ctx, "送入宏的有效激活：" + sent + " · 跳过的零：" + skipped, 70, 190, 13.5, PAL.orange, "left");
    txt(ctx, "→ 激活输入周期减少（50% 稀疏时 ~1.84× 能效提升）", 70, 220, 12.5, PAL.gray, "left");
    txt(ctx, "bit-mask 记录稀疏位置 → 计算后 OMB 按掩码写回正确位置", 70, 248, 12.5, PAL.gray, "left");
    if (stat) stat.textContent = "已处理 " + shown + " 个激活 · 有效 " + sent + " · 跳过 " + skipped;
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
