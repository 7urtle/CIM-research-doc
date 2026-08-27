/* ============================================================
   SpikeRAM 教学教程 · 交互脚本
   演示 A 事件驱动卷积 · 演示 B 移位相加 · 演示 C 格雷码更新
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
   演示 A · 事件驱动卷积
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");
  // 事件位置（稀疏）
  const events = [[1, 1], [3, 0], [4, 2], [2, 4], [5, 5], [0, 3], [6, 1], [3, 3]];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "事件驱动卷积：只有事件到达的位置才计算", 30, 24, 15, PAL.white, "left");
    const e = cyc % events.length;
    const ev = events[e];
    // 网格
    const gx = 80, gy = 60, cell = 34;
    for (let r = 0; r < 7; r++) {
      for (let c = 0; c < 7; c++) {
        const x = gx + c * cell, y = gy + r * cell;
        const isEv = events.some(p => p[0] === c && p[1] === r);
        const inWin = Math.abs(c - ev[0]) <= 1 && Math.abs(r - ev[1]) <= 1;
        ctx.fillStyle = inWin ? "#2a2440" : (isEv ? "#3a2a26" : "#141c2a");
        ctx.strokeStyle = inWin ? PAL.purple : (isEv ? PAL.red : PAL.line);
        ctx.lineWidth = inWin ? 2 : 1.5;
        rrect(ctx, x, y, cell - 4, cell - 4, 5); ctx.fill(); ctx.stroke();
        if (isEv) {
          ctx.fillStyle = PAL.red;
          ctx.beginPath(); ctx.arc(x + (cell - 4) / 2, y + (cell - 4) / 2, 5, 0, 6.28); ctx.fill();
        }
      }
    }
    // 当前窗口高亮
    const x0 = gx + ev[0] * cell - 2, y0 = gy + ev[1] * cell - 2;
    ctx.strokeStyle = PAL.orange; ctx.lineWidth = 3;
    ctx.strokeRect(x0, y0, cell * 3, cell * 3);
    txt(ctx, "当前事件 (" + ev[0] + "," + ev[1] + ") → 只算 3×3 核窗口", 60, gy + 7 * cell + 16, 13, PAL.orange, "left");
    txt(ctx, "其余位置（空白）全部跳过 → 稀疏自适应", 60, gy + 7 * cell + 40, 12, PAL.gray, "left");
    txt(ctx, "事件 " + (e + 1) + "/" + events.length + " · 窗口内事件数 " + events.filter(p => Math.abs(p[0] - ev[0]) <= 1 && Math.abs(p[1] - ev[1]) <= 1).length, 60, gy + 7 * cell + 62, 12, PAL.blue, "left");
    if (stat) stat.textContent = "事件 " + (e + 1) + "：" + "只计算 3×3 窗口（其余跳过）";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
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
   演示 B · 移位相加（无乘法）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 300);
  if (!D) return;
  const { ctx } = D;
  const spikes = [1, 0, 1, 0, 1, 1, 0, 1];
  const weights = [12, -7, 25, 3, -15, 8, -4, 20];
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "移位相加：脉冲=1 就把权重加进 Vmem（无乘法器）", 30, 24, 15, PAL.white, "left");
    let vmem = 0;
    for (let i = 0; i <= Math.min(cyc, spikes.length - 1); i++) {
      if (spikes[i]) vmem += weights[i];
    }
    // 输入脉冲与权重
    for (let i = 0; i < 8; i++) {
      const x = 60 + i * 105;
      ctx.fillStyle = spikes[i] ? "#4a2a1e" : PAL.panel;
      ctx.strokeStyle = spikes[i] ? PAL.orange : PAL.line; ctx.lineWidth = 2;
      rrect(ctx, x, 60, 90, 40, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "脉冲 " + spikes[i], x + 45, 78, 12, spikes[i] ? PAL.orange : PAL.gray, "center");
      ctx.fillStyle = spikes[i] && i <= cyc ? "#1e3c2c" : "#141c2a";
      ctx.strokeStyle = PAL.green; ctx.lineWidth = 1.5;
      rrect(ctx, x, 108, 90, 34, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "W=" + weights[i], x + 45, 125, 11, spikes[i] && i <= cyc ? PAL.green : PAL.gray, "center");
      if (spikes[i] && i <= cyc) {
        ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(x + 45, 142); ctx.lineTo(x + 45, 170); ctx.stroke();
      }
    }
    // Vmem
    ctx.fillStyle = "#14263c"; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 2;
    rrect(ctx, 60, 180, 860, 60, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "Vmem = " + vmem + "（阈值 40 → " + (vmem >= 40 ? "发放!" : "未发放") + "）", 80, 205, 18, vmem >= 40 ? PAL.orange : PAL.blue, "left");
    // 进度条
    ctx.fillStyle = "#1c2838";
    ctx.fillRect(80, 228, 820, 8);
    ctx.fillStyle = PAL.blue;
    ctx.fillRect(80, 228, Math.min(820, 820 * vmem / 60), 8);
    txt(ctx, "已累加 " + Math.min(cyc + 1, 8) + "/8 个脉冲（其中 " + spikes.slice(0, Math.min(cyc + 1, 8)).reduce((a, b) => a + b, 0) + " 个为 1）", 80, 258, 12, PAL.gray, "left");
    if (stat) stat.textContent = "Vmem=" + vmem + " · 无乘法，只有选通+加法";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 700); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = -1; draw(); };
  if (play) timer = setInterval(tick, 700);
  cyc = -1;
  draw();
})();

/* ============================================================
   演示 C · 二进制 vs 格雷码
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");

  function toBin(v) {
    const s = v.toString(2);
    return ("0000" + s).slice(-4);
  }
  function toGray(v) {
    return toBin(v ^ (v >> 1));
  }
  function diffBits(a, b) {
    let d = 0;
    for (let i = 0; i < 4; i++) if (((a >> i) & 1) !== ((b >> i) & 1)) d++;
    return d;
  }

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "同一次权重更新（±1）：二进制 vs 格雷码，翻几位？", 30, 24, 15, PAL.white, "left");
    const cases = [[7, 8], [3, 4], [10, 9], [5, 6], [12, 11], [1, 2]];
    const [v1, v2] = cases[cyc % cases.length];
    // 二进制
    txt(ctx, "二进制 " + v1 + " → " + v2, 60, 70, 14, PAL.red);
    for (let k = 0; k < 4; k++) {
      const x = 280 + k * 46;
      const changed = ((v1 >> (3 - k)) & 1) !== ((v2 >> (3 - k)) & 1);
      ctx.fillStyle = changed ? "#4a2a1e" : "#1c2838";
      ctx.strokeStyle = changed ? PAL.red : PAL.line; ctx.lineWidth = 2;
      rrect(ctx, x, 58, 38, 26, 5); ctx.fill(); ctx.stroke();
      txt(ctx, toBin(v1)[k], x + 19, 71, 12, PAL.white, "center");
      rrect(ctx, x, 92, 38, 26, 5);
      ctx.fillStyle = changed ? "#4a2a1e" : "#1c2838";
      ctx.fill(); ctx.stroke();
      txt(ctx, toBin(v2)[k], x + 19, 105, 12, PAL.white, "center");
    }
    txt(ctx, "翻转 " + diffBits(v1, v2) + " 位", 500, 90, 14, PAL.red);
    // 格雷码
    txt(ctx, "格雷码 " + parseInt(toGray(v1), 2) + " → " + parseInt(toGray(v2), 2), 60, 160, 14, PAL.green);
    const g1 = v1 ^ (v1 >> 1), g2 = v2 ^ (v2 >> 1);
    for (let k = 0; k < 4; k++) {
      const x = 280 + k * 46;
      const changed = ((g1 >> (3 - k)) & 1) !== ((g2 >> (3 - k)) & 1);
      ctx.fillStyle = changed ? "#1e3c2c" : "#1c2838";
      ctx.strokeStyle = changed ? PAL.green : PAL.line; ctx.lineWidth = 2;
      rrect(ctx, x, 148, 38, 26, 5); ctx.fill(); ctx.stroke();
      txt(ctx, toGray(v1)[k], x + 19, 161, 12, PAL.white, "center");
      ctx.fillStyle = changed ? "#1e3c2c" : "#1c2838";
      rrect(ctx, x, 182, 38, 26, 5); ctx.fill(); ctx.stroke();
      txt(ctx, toGray(v2)[k], x + 19, 195, 12, PAL.white, "center");
    }
    txt(ctx, "翻转 " + diffBits(g1, g2) + " 位（恒为 1！）", 500, 180, 14, PAL.green);
    txt(ctx, "→ 格雷码 ±1 更新只写 1 个 eNVM 器件 → 写次数与磨损最小化", 60, 250, 13, PAL.orange, "left");
    txt(ctx, "三值梯度 {−1,0,+1} 保证更新步长恒为 ±1 → 每次最多翻 1 位", 60, 276, 12, PAL.gray, "left");
    if (stat) stat.textContent = "例：" + v1 + "→" + v2 + " · 二进制翻 " + diffBits(v1, v2) + " 位，格雷码翻 1 位";
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
