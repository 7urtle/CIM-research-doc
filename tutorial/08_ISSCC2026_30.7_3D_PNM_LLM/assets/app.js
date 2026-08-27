/* ============================================================
   3D PNM 教学教程 · 交互脚本
   演示 A 3D 堆叠数据路径 · 演示 B GEMM 切分 · 演示 C 缓冲命中
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
   演示 A · 3D 堆叠与数据路径
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 360);
  if (!D) return;
  const { ctx } = D;
  let src = "N";      // N = DRAM_N 直连; F = DRAM_F 穿 TSV
  let playing = true, t = 0, timer = null;
  const stat = document.getElementById("demoA-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "3D 堆叠：Two-DRAM-One-Logic", 30, 24, 15, PAL.white, "left");
    // 三层
    const layers = [
      { name: "DRAM_F（512Mb）", y: 60, col: PAL.green },
      { name: "DRAM_N（512Mb）", y: 160, col: PAL.green },
      { name: "逻辑晶圆（28nm CMOS）", y: 260, col: PAL.blue },
    ];
    layers.forEach(l => {
      ctx.fillStyle = "#14263c"; ctx.strokeStyle = l.col; ctx.lineWidth = 2;
      rrect(ctx, 60, l.y, 500, 70, 10); ctx.fill(); ctx.stroke();
      txt(ctx, l.name, 80, l.y + 35, 14, l.col);
    });
    // HB 线
    ctx.strokeStyle = PAL.green; ctx.lineWidth = 2; ctx.setLineDash([8, 4]);
    ctx.beginPath(); ctx.moveTo(60, 130); ctx.lineTo(560, 130); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(60, 230); ctx.lineTo(560, 230); ctx.stroke();
    ctx.setLineDash([]);
    txt(ctx, "HB", 45, 130, 11, PAL.green, "right");
    txt(ctx, "HB", 45, 230, 11, PAL.green, "right");
    // TSV
    ctx.fillStyle = PAL.orange;
    ctx.fillRect(140, 160, 10, 100);
    ctx.fillRect(460, 160, 10, 100);
    txt(ctx, "mini-TSV ×2", 585, 210, 12, PAL.orange, "left");
    // 右侧说明
    if (src === "N") {
      txt(ctx, "数据源：DRAM_N（直连 HB）", 620, 80, 14, PAL.green);
      txt(ctx, "路径：DRAM_N → HB → 逻辑层", 620, 110, 13, PAL.gray);
      txt(ctx, "一次跳变，最短路径", 620, 136, 12, PAL.gray);
    } else {
      txt(ctx, "数据源：DRAM_F（穿 TSV）", 620, 80, 14, PAL.orange);
      txt(ctx, "路径：DRAM_F → HB → TSV → HB → 逻辑层", 620, 110, 13, PAL.gray);
      txt(ctx, "要穿过 DRAM_N，多两段 HB", 620, 136, 12, PAL.gray);
    }
    // 数据块动画
    if (playing) {
      t = (t + 0.02) % 1;
      if (src === "N") {
        const y = 230 + t * 0; // DRAM_N 行 → 直接到逻辑
        const x = 60 + t * 500;
        ctx.fillStyle = PAL.green;
        ctx.beginPath(); ctx.arc(x, 195, 9, 0, 6.28); ctx.fill();
      } else {
        const seg = Math.floor(t * 3);
        const ft = (t * 3) % 1;
        let x, y;
        if (seg === 0) { x = 60 + ft * 420; y = 95; }
        else if (seg === 1) { x = 480; y = 95 + ft * 140; }
        else { x = 480 - ft * 420; y = 195; }
        ctx.fillStyle = PAL.orange;
        ctx.beginPath(); ctx.arc(x, y, 9, 0, 6.28); ctx.fill();
      }
    }
    if (stat) stat.textContent = src === "N" ? "DRAM_N：信号直连 HB 到逻辑层" : "DRAM_F：信号走 HB-TSV-HB 链穿过 DRAM_N";
  }

  const b1 = document.getElementById("demoA-layer1");
  const b2 = document.getElementById("demoA-layer2");
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  if (b1) b1.onclick = function () { src = "N"; b1.classList.add("on"); b2.classList.remove("on"); draw(); };
  if (b2) b2.onclick = function () { src = "F"; b2.classList.add("on"); b1.classList.remove("on"); draw(); };
  if (bPlay) bPlay.onclick = function () {
    playing = !playing;
    this.classList.toggle("on", playing);
    this.textContent = playing ? "⏸ 暂停" : "▶ 数据流动画";
    if (playing) { clearInterval(timer); timer = setInterval(draw, 50); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { t = 0; draw(); };
  if (playing) timer = setInterval(draw, 50);
  draw();
})();

/* ============================================================
   演示 B · GEMM 切分与 16 ACC 分配
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let k = 0, playing = true, timer = null;
  const stat = document.getElementById("demoB-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "GEMM 切分：M 切 4 × K 切 4 = 16 个子任务 → 8 BG × 2 ACC", 30, 24, 15, PAL.white, "left");
    // 左侧输入矩阵
    txt(ctx, "输入 I (M×N)", 130, 60, 13, PAL.blue, "center");
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const x = 60 + c * 60, y = 76 + r * 56;
        ctx.strokeStyle = PAL.blue; ctx.lineWidth = 1.5;
        ctx.strokeRect(x, y, 56, 52);
        if (r === Math.floor(k / 4)) { ctx.fillStyle = "rgba(30,144,220,0.35)"; ctx.fillRect(x, y, 56, 52); }
      }
    }
    // 右侧权重矩阵
    txt(ctx, "权重 W (N×K)", 370, 60, 13, PAL.red, "center");
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const x = 300 + c * 60, y = 76 + r * 56;
        ctx.strokeStyle = PAL.red; ctx.lineWidth = 1.5;
        ctx.strokeRect(x, y, 56, 52);
        if (c === Math.floor(k / 4)) { ctx.fillStyle = "rgba(230,110,90,0.35)"; ctx.fillRect(x, y, 56, 52); }
      }
    }
    // 16 个 ACC 格子
    txt(ctx, "16 个 ACC（8 BG × 2）", 760, 60, 13, PAL.green, "center");
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const idx = r * 4 + c;
        const x = 640 + c * 60, y = 76 + r * 56;
        ctx.strokeStyle = PAL.green; ctx.lineWidth = 1.5;
        ctx.strokeRect(x, y, 56, 52);
        if (idx === k) {
          ctx.fillStyle = "rgba(60,190,140,0.4)"; ctx.fillRect(x, y, 56, 52);
          ctx.strokeStyle = PAL.orange; ctx.lineWidth = 3; ctx.strokeRect(x, y, 56, 52);
        }
      }
    }
    // 分配信息
    const r = Math.floor(k / 4), c = k % 4;
    const bg = (r * 2 + Math.floor(c / 2)) % 8;
    const acc = (c % 2);
    if (stat) stat.textContent = `I${r}W${c} → BG${bg}/ACC${acc}（每 ACC 只算自己的子矩阵，主机拼接输出，零跨块通信）`;
    // 底部进度
    txt(ctx, `子任务 ${k + 1}/16 · I${r}W${c} → BG${bg}/ACC${acc}`, 60, 300, 13, PAL.orange, "left");
  }

  function tick() { k = (k + 1) % 16; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
  if (bPlay) bPlay.onclick = function () {
    playing = !playing;
    this.classList.toggle("on", playing);
    this.textContent = playing ? "⏸ 暂停" : "▶ 播放";
    if (playing) { clearInterval(timer); timer = setInterval(tick, 450); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { k = 0; draw(); };
  if (playing) timer = setInterval(tick, 450);
  draw();
})();

/* ============================================================
   演示 C · 2048b 缓冲与开放页（buf_hit）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let t = 0, playing = true, timer = null;
  const stat = document.getElementById("demoC-stat");
  const hits = [true, true, false, true, true, true, false, true, true, true, true, false];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "访存优化：2048b 缓冲 + 开放页策略（连续访问命中动画）", 30, 24, 15, PAL.white, "left");
    const idx = Math.floor(t * hits.length) % hits.length;
    const hit = hits[idx];
    // 缓冲区
    ctx.fillStyle = "#14263c"; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
    rrect(ctx, 60, 60, 420, 90, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "2048b 缓冲（最近访问的数据）", 80, 82, 14, PAL.orange);
    for (let i = 0; i < 8; i++) {
      ctx.fillStyle = i === idx % 8 ? "rgba(240,180,70,0.7)" : "rgba(240,180,70,0.2)";
      ctx.fillRect(80 + i * 48, 104, 40, 30);
    }
    txt(ctx, "buf_hit：" + (hit ? "命中！直接从缓冲返回，免 DRAM 访问" : "未命中：走 DRAM（预充电+激活+读）"), 60, 190, 14, hit ? PAL.green : PAL.red);
    // DRAM 访问动画（未命中时）
    if (!hit) {
      const p = (t * 4) % 1;
      const y = 220 + Math.sin(p * 3.14) * 20;
      const x = 60 + p * 500;
      ctx.fillStyle = PAL.red;
      ctx.beginPath(); ctx.arc(x, y, 8, 0, 6.28); ctx.fill();
      txt(ctx, "DRAM 访问（慢）", 620, 260, 13, PAL.red);
    } else {
      const p = (t * 4) % 1;
      const x = 60 + p * 400;
      ctx.fillStyle = PAL.green;
      ctx.beginPath(); ctx.arc(x, 150, 8, 0, 6.28); ctx.fill();
      txt(ctx, "缓冲直接返回（快）", 620, 150, 13, PAL.green);
    }
    // 统计
    let nh = 0;
    for (let i = 0; i < Math.min(idx + 1, hits.length); i++) if (hits[i]) nh++;
    const total = Math.min(idx + 1, hits.length);
    if (stat) stat.textContent = total > 0 ? `命中率 ≈ ${(nh / total * 100).toFixed(0)}%（连续顺序访问命中率高）` : "等待…";
  }

  function tick() { t = (t + 0.02) % 1; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    playing = !playing;
    this.classList.toggle("on", playing);
    this.textContent = playing ? "⏸ 暂停" : "▶ 播放";
    if (playing) { clearInterval(timer); timer = setInterval(tick, 90); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { t = 0; draw(); };
  if (playing) timer = setInterval(tick, 90);
  draw();
})();
