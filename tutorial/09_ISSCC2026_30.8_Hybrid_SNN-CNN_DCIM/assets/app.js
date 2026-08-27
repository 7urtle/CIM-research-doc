/* ============================================================
   混合 SNN-CNN DCIM 教学教程 · 交互脚本
   演示 A 膜电位仿真 · 演示 B INT4/INT8 双模 · 演示 C 数据映射对比
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
  ctx.arcTo(x + w, y + h, x, y + h, r);
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

/* ---------- 进度条 + 侧栏 ---------- */
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
   演示 A · 膜电位仿真（IF / LIF / IQIF）
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 360);
  if (!D) return;
  const { ctx } = D;
  const NS = 64;
  let mode = "IF", th = 8, playing = true, step = 0, timer = null;
  const stat = document.getElementById("demoA-stat");

  // 生成输入脉冲序列（固定种子效果）
  const spikes = [];
  for (let i = 0; i < NS; i++) spikes.push((i * 7) % 11 < 4 ? 1 : 0);

  function stepModel(mode, mp) {
    if (mode === "IF") {
      return mp;
    } else if (mode === "LIF") {
      return Math.max(0, mp - 1);
    } else { // IQIF
      const pdeth = 3, rest = 2, alpha = 3, beta = 2, thresh = th;
      const iq = mp < pdeth ? ((alpha * rest - mp) >> 3) : ((beta * (mp - thresh)) >> 3);
      return Math.max(0, mp + iq);
    }
  }

  function traj() {
    let mp = 0; const out = [];
    for (let s = 0; s < NS; s++) {
      mp = stepModel(mode, mp) + spikes[s];
      if (mp >= th) { mp = 0; out.push({ mp: 0, fire: true }); }
      else out.push({ mp, fire: false });
    }
    return out;
  }

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const col = { IF: PAL.blue, LIF: PAL.purple, IQIF: PAL.green }[mode];
    txt(ctx, mode + " 模式 · 阈值 = " + th + " · 播放到时间步 " + step, 30, 24, 15, col, "left");

    const x0 = 60, y0 = 60, x1 = w - 40, y1 = 260;
    ctx.fillStyle = "#0e1826";
    ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
    const thy = y0 + 70;
    ctx.strokeStyle = PAL.red; ctx.lineWidth = 2; ctx.setLineDash([6, 4]);
    ctx.beginPath(); ctx.moveTo(x0, thy); ctx.lineTo(x1, thy); ctx.stroke(); ctx.setLineDash([]);
    txt(ctx, "阈值 θ = " + th, x1 - 8, thy - 12, 12, PAL.red, "right");

    const t = traj();
    // 曲线
    const pts = [];
    for (let s = 0; s <= step && s < NS; s++) {
      const px = x0 + s * (x1 - x0) / (NS - 1);
      const py = y1 - 12 - t[s].mp * ((y1 - y0 - 80) / (th + 3));
      pts.push([px, py]);
    }
    if (pts.length > 1) {
      ctx.strokeStyle = col; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
      for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
      ctx.stroke();
    }
    // 脉冲条与发放标记
    for (let s = 0; s <= step && s < NS; s++) {
      const px = x0 + s * (x1 - x0) / (NS - 1);
      if (spikes[s]) {
        ctx.fillStyle = PAL.orange;
        ctx.fillRect(px - 3, y1 - 10, 6, 8);
      }
      if (t[s].fire) {
        ctx.fillStyle = col;
        ctx.beginPath(); ctx.arc(px, y0 + 14, 4, 0, 6.28); ctx.fill();
      }
    }
    txt(ctx, "橙色小条 = 输入脉冲；曲线上的圆点 = 该步发放（清零）", x0, y1 + 20, 12, PAL.gray, "left");
    txt(ctx, "LIF 注意看：无输入时曲线回落（泄漏）；IQIF 注意看：阈值附近加速", x0, y1 + 42, 12, PAL.gray, "left");
    txt(ctx, "当前膜电位 MP = " + (step < NS ? t[Math.min(step, NS - 1)].mp : t[NS - 1].mp), x1, y1 + 42, 13, col, "right");
  }

  function tick() { step = Math.min(NS - 1, step + 1); draw(); }

  const bIf = document.getElementById("demoA-if");
  const bLif = document.getElementById("demoA-lif");
  const bIq = document.getElementById("demoA-iqif");
  const sTh = document.getElementById("demoA-th");
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");

  function setMode(m) {
    mode = m; step = 0;
    [bIf, bLif, bIq].forEach((b, i) => b.classList.toggle("on", ["IF", "LIF", "IQIF"][i] === m));
    if (stat) stat.textContent = m + " 模式 · " + (playing ? "播放中" : "暂停");
    draw();
  }
  if (bIf) bIf.onclick = () => setMode("IF");
  if (bLif) bLif.onclick = () => setMode("LIF");
  if (bIq) bIq.onclick = () => setMode("IQIF");
  if (sTh) sTh.oninput = function () { th = parseInt(this.value, 10); step = 0; draw(); };
  if (bPlay) bPlay.onclick = function () {
    playing = !playing;
    this.classList.toggle("on", playing);
    this.textContent = playing ? "⏸ 暂停" : "▶ 播放";
    if (playing) { clearInterval(timer); timer = setInterval(tick, 160); }
    else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { step = 0; draw(); };
  if (playing) timer = setInterval(tick, 160);
  draw();
})();

/* ============================================================
   演示 B · INT4/INT8 双模权重映射
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let i8 = false;
  const stat = document.getElementById("demoB-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const col = i8 ? PAL.blue : PAL.green;
    txt(ctx, (i8 ? "INT8 模式：2 个 8b MAC（W0+W2 → A，W1+W3 → B）" : "INT4 模式：4 个 4b MAC（W0→A，W1→B，W2→C，W3→D）"),
      30, 26, 16, col, "left");
    // 4 槽
    const x0 = 60, y0 = 70, cw = 170, ch = 60, gap = 24;
    const slots = ["W0", "W1", "W2", "W3"];
    const labels = i8
      ? ["A[3:0]\n(A 低 4 位)", "B[3:0]\n(B 低 4 位)", "A[7:4]\n(A 高 4 位)", "B[7:4]\n(B 高 4 位)"]
      : ["A[3:0]\n4b 权重", "B[3:0]\n4b 权重", "C[3:0]\n4b 权重", "D[3:0]\n4b 权重"];
    const pairCol = i8 ? [PAL.blue, PAL.blue, "#0a5f8c", "#0a5f8c"] : [PAL.green, PAL.green, "#2a8f6a", "#2a8f6a"];
    for (let i = 0; i < 4; i++) {
      const x = x0 + i * (cw + gap);
      ctx.fillStyle = "#14263c"; ctx.strokeStyle = pairCol[i]; ctx.lineWidth = 2;
      rrect(ctx, x, y0, cw, ch, 10); ctx.fill(); ctx.stroke();
      txt(ctx, slots[i], x + 12, y0 + 20, 14, PAL.white, "left");
      const ls = labels[i].split("\n");
      txt(ctx, ls[0], x + 12, y0 + 42, 12, pairCol[i], "left");
      if (ls[1]) txt(ctx, ls[1], x + 12, y0 + 56 - 8, 10, PAL.gray, "left");
    }
    // 乘法器与结果
    const my = 190;
    txt(ctx, "MUL0", x0, my + 14, 14, PAL.white);
    txt(ctx, "MUL1", x0 + cw + gap, my + 14, 14, PAL.white);
    ctx.strokeStyle = PAL.line; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(x0 + 30, y0 + ch); ctx.lineTo(x0 + 30, my); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x0 + cw + gap + 30, y0 + ch); ctx.lineTo(x0 + cw + gap + 30, my); ctx.stroke();
    const res = i8 ? "每周期 2 个 8b×8b MAC" : "每周期 4 个 4b×4b MAC";
    const res2 = i8 ? "（TR 开启：拼接高低位时消除冗余翻转）" : "（TR 关闭：四路独立并行）";
    txt(ctx, res, x0, my + 44, 16, col);
    txt(ctx, res2, x0, my + 70, 12, PAL.gray);
    if (stat) stat.textContent = i8 ? "INT8：W0/W1=低4位，W2/W3=高4位 → 2 个 8b MAC" : "INT4：W0–W3 独立 → 4 个 4b MAC";
  }

  const b4 = document.getElementById("demoB-i4");
  const b8 = document.getElementById("demoB-i8");
  if (b4) b4.onclick = function () { i8 = false; b4.classList.add("on"); b8.classList.remove("on"); draw(); };
  if (b8) b8.onclick = function () { i8 = true; b8.classList.add("on"); b4.classList.remove("on"); draw(); };
  draw();
})();

/* ============================================================
   演示 C · 数据映射对比（权重更新能耗 vs PSUM 存储）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let t = 0, playing = true, timer = null;
  const stat = document.getElementById("demoC-stat");

  const schemes = [
    { name: "① TS-first", w: 1.0, p: 0.12, col: PAL.red, note: "权重每 TS 重载 · PSUM 小" },
    { name: "② 复用-first", w: 0.12, p: 0.95, col: PAL.purple, note: "权重只读一次 · PSUM 巨大" },
    { name: "③ PS-WR-ODM", w: 0.4, p: 0.4, col: PAL.green, note: "块内复用 · 两边均衡" },
  ];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "数据映射对比：权重更新能耗（红） vs PSUM 存储（蓝），柱越高越差", 30, 26, 15, PAL.white, "left");
    const bw = 150, gap = 60, x0 = 70, yBase = 250, maxH = 170;
    schemes.forEach((s, i) => {
      const x = x0 + i * (bw + gap);
      // 权重能耗（随时间增长，模拟运行）
      const wv = s.w * (0.4 + 0.6 * t);
      // PSUM 柱
      ctx.fillStyle = "rgba(30,144,220,0.85)";
      ctx.fillRect(x, yBase - s.p * maxH, bw / 2 - 8, s.p * maxH);
      ctx.strokeStyle = PAL.blue; ctx.strokeRect(x, yBase - s.p * maxH, bw / 2 - 8, s.p * maxH);
      // 权重柱
      ctx.fillStyle = "rgba(230,110,90,0.85)";
      ctx.fillRect(x + bw / 2 + 8, yBase - wv * maxH, bw / 2 - 8, wv * maxH);
      ctx.strokeStyle = PAL.red; ctx.strokeRect(x + bw / 2 + 8, yBase - wv * maxH, bw / 2 - 8, wv * maxH);
      // 标签
      txt(ctx, s.name, x + bw / 2, yBase + 20, 14, s.col, "center");
      txt(ctx, s.note, x + bw / 2, yBase + 42, 11, PAL.gray, "center");
      txt(ctx, "PSUM " + (s.p * 100).toFixed(0) + "%", x + bw / 4 - 4, yBase - s.p * maxH - 10, 11, PAL.blue, "center");
      txt(ctx, "权重 " + (wv * 100).toFixed(0) + "%", x + bw * 3 / 4 + 4, yBase - wv * maxH - 10, 11, PAL.red, "center");
    });
    if (stat) stat.textContent = "PS-WR-ODM：以少量 PSUM 开销（约 40%）换取权重更新能耗大幅下降（约 40%）";
  }

  function tick() { t = Math.min(1, t + 0.01); draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    playing = !playing;
    this.classList.toggle("on", playing);
    this.textContent = playing ? "⏸ 暂停" : "▶ 播放";
    if (playing) { clearInterval(timer); timer = setInterval(tick, 80); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { t = 0; draw(); };
  if (playing) timer = setInterval(tick, 80);
  draw();
})();
