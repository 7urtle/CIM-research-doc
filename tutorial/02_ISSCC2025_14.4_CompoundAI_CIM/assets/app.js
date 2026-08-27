/* ============================================================
   Compound AI CIM 教学教程 · 交互脚本
   演示 A MantissaEE · 演示 B 预对齐 vs 后对齐 · 演示 C 2:4 稀疏
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
   演示 A · MantissaEE 转换
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let e = 2;
  const mantissa = "1101101010"; // 10b 尾数（示例）
  const stat = document.getElementById("demoA-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "MantissaEE 转换：尾数按 E[1:0] 右移后拼成 16b（示例尾数 " + mantissa + "）", 30, 24, 15, PAL.white, "left");
    // 原始尾数
    txt(ctx, "尾数 M（10b）", 60, 60, 13, PAL.green);
    for (let k = 0; k < 10; k++) {
      const x = 220 + k * 30;
      ctx.fillStyle = "#1e3c2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 1.5;
      rrect(ctx, x, 48, 26, 26, 5); ctx.fill(); ctx.stroke();
      txt(ctx, mantissa[k], x + 13, 61, 12, PAL.white, "center");
    }
    // 移位后
    txt(ctx, "右移 E[1:0]=" + e + " 位后", 60, 110, 13, PAL.orange);
    for (let k = 0; k < 10; k++) {
      const x = 220 + k * 30;
      const has = k + e < 10;
      const ch = has ? mantissa[k + e] : "0";
      ctx.fillStyle = has ? "#3c2e1a" : "#1c2638";
      ctx.strokeStyle = has ? PAL.orange : PAL.line; ctx.lineWidth = 1.5;
      rrect(ctx, x, 98, 26, 26, 5); ctx.fill(); ctx.stroke();
      txt(ctx, ch, x + 13, 111, 12, PAL.white, "center");
    }
    // MantissaEE
    txt(ctx, "MantissaEE（16b）", 60, 160, 13, PAL.purple);
    for (let k = 0; k < 16; k++) {
      const x = 220 + k * 30;
      const shifted = k + e < 10;
      const ch = shifted ? mantissa[k + e] : "0";
      ctx.fillStyle = shifted ? "#2a2440" : "#141c2a";
      ctx.strokeStyle = PAL.purple; ctx.lineWidth = 1.5;
      rrect(ctx, x, 148, 26, 26, 5); ctx.fill(); ctx.stroke();
      txt(ctx, ch, x + 13, 161, 11, PAL.white, "center");
    }
    txt(ctx, "→ 对齐所需的指数位宽变小（低位已折进尾数）→ 后续对齐移位量小、截断损失小", 60, 210, 13, PAL.gray, "left");
    txt(ctx, "同一 16b 宽度兼容 FP16 / FP8（E4M3）/ INT8", 60, 238, 13, PAL.blue, "left");
    if (stat) stat.textContent = "E[1:0]=" + e + " → 尾数右移 " + e + " 位，空位补 0";
  }

  const sE = document.getElementById("demoA-e");
  if (sE) sE.oninput = function () { e = parseInt(this.value, 10); draw(); };
  draw();
})();

/* ============================================================
   演示 B · 预对齐 vs 后对齐
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
    txt(ctx, "误差累积对比：预对齐（红）vs 后乘积对齐（绿）", 30, 24, 15, PAL.white, "left");
    const n = Math.min(cyc, 12);
    // 预对齐：每个乘积都带误差
    ctx.fillStyle = "#2a1e1e"; ctx.strokeStyle = PAL.red; ctx.lineWidth = 2;
    rrect(ctx, 60, 60, 420, 120, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "预对齐：误差注入每个乘积", 80, 82, 14, PAL.red);
    let preErr = 0;
    for (let k = 0; k < n; k++) {
      preErr += 1; // 每个乘积都累积一份误差
      const x = 80 + k * 30;
      ctx.fillStyle = "rgba(230,110,90,0.5)";
      ctx.fillRect(x, 105, 22, 22);
    }
    txt(ctx, "总误差 ≈ " + preErr + " × 单次截断误差（放大 N 倍）", 80, 152, 12.5, PAL.red);
    // 后对齐：误差只出现一次
    ctx.fillStyle = "#1e2e26"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 500, 60, 420, 120, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "后乘积对齐：误差只出现一次", 520, 82, 14, PAL.green);
    for (let k = 0; k < n; k++) {
      const x = 520 + k * 30;
      ctx.fillStyle = "rgba(60,190,140,0.5)";
      ctx.fillRect(x, 105, 22, 22);
    }
    txt(ctx, "总误差 ≈ 1 × 单次对齐误差（不放大）", 520, 152, 12.5, PAL.green);
    txt(ctx, "对比：FP16-MAC 最大误差 < 2⁻³⁰（前作 2⁻¹）· SER 60.1 dB（3.14×）", 60, 220, 14, PAL.orange, "left");
    txt(ctx, "复合模型上精度损失平均降低 11.07×", 60, 248, 12.5, PAL.gray, "left");
    if (stat) stat.textContent = "已处理 " + n + " 个乘积：预对齐误差 ×" + n + "，后对齐误差 ×1";
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
   演示 C · 2:4 稀疏路由
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");
  const groups = [
    [1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1], [0, 1, 0, 1]
  ];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "NIM 静态 2:4 稀疏路由：4 个权重选 2 个有效", 30, 24, 15, PAL.white, "left");
    const g = groups[cyc % groups.length];
    // 4 个权重
    for (let k = 0; k < 4; k++) {
      const x = 90 + k * 120;
      const valid = g[k] === 1;
      ctx.fillStyle = valid ? "#3c2a1a" : "#141c2a";
      ctx.strokeStyle = valid ? PAL.orange : PAL.line; ctx.lineWidth = 2;
      rrect(ctx, x, 70, 100, 60, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "W" + k + "=" + g[k], x + 50, 92, 13, valid ? PAL.orange : PAL.gray, "center");
      txt(ctx, valid ? "有效 → 路由" : "剪枝跳过", x + 50, 114, 11, valid ? PAL.green : PAL.gray, "center");
    }
    // 路由结果
    ctx.strokeStyle = PAL.green; ctx.lineWidth = 2.5;
    let routed = [];
    g.forEach((v, i) => { if (v) routed.push(i); });
    routed.forEach((i, k) => {
      const x = 90 + i * 120;
      ctx.beginPath(); ctx.moveTo(x + 50, 130); ctx.lineTo(200 + k * 150, 190); ctx.stroke();
    });
    ctx.fillStyle = "#1e3c2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 200, 190, 250, 60, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "有效项 " + routed.map(r => "W" + r).join(" + ") + " → Booth 编码乘法", 325, 220, 12, PAL.green, "center");
    // 排除路径
    txt(ctx, "排除 2 条不可能路径 → 网络复杂度降低", 560, 220, 12, PAL.gray, "left");
    txt(ctx, "静态稀疏 ≈ 2× 加速（配合动态启动器共 5.30×，达理论上限 92.6%）", 60, 272, 13, PAL.orange, "left");
    if (stat) stat.textContent = "组 " + (cyc % groups.length + 1) + "：有效项 " + routed.map(r => "W" + r).join(" + ");
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
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
