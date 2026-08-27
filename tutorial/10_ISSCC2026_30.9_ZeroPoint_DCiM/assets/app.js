/* ============================================================
   DCiM 教学教程 · 交互脚本
   包含：进度条/侧栏高亮、测验揭示、5 个 Canvas 仿真
   （A 量化映射 · B Booth 分步 · C 部分积对比 · D 数据流 · E 流水线时空图）
   ============================================================ */
"use strict";

/* ---------- 通用工具 ---------- */
function cvs(id, w, h) {
  const c = document.getElementById(id);
  if (!c) return null;
  c.width = w; c.height = h;
  const ctx = c.getContext("2d");
  return { c, ctx, w, h };
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
function txt(ctx, s, x, y, size, color, align, font) {
  ctx.fillStyle = color || "#dbe6f4";
  ctx.font = (size || 13) + "px " + (font || "'Microsoft YaHei','PingFang SC',sans-serif");
  ctx.textAlign = align || "left";
  ctx.textBaseline = "middle";
  ctx.fillText(s, x, y);
}
const PAL = {
  bg: "#0a1119", panel: "#12202f", line: "#2c4d73",
  blue: "#0f7cb6", green: "#2fae7e", orange: "#e8a33d",
  red: "#e2694f", purple: "#9b6fd6", gray: "#7f93ad", white: "#e8f0fa"
};

/* ---------- 进度条 + 侧栏滚动高亮 ---------- */
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

/* ---------- 测验揭示 ---------- */
function reveal(btn) {
  const ans = btn.nextElementSibling;
  if (ans) ans.classList.add("show");
}

/* ============================================================
   演示 A · 对称 vs 零点量化误差对比
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 330);
  if (!D) return;
  const { ctx } = D;
  let data = { min: -0.5, max: 6.0 };      // 真实数据范围（偏态）
  let play = true, t = 0, auto = true;

  function mse(mode) {
    let s, z, e = 0, n = 0;
    for (let i = 0; i < 400; i++) {
      const r = data.min + Math.random() * (data.max - data.min);
      if (mode === "sym") { s = Math.max(Math.abs(data.min), Math.abs(data.max)) / 127; z = 0; }
      else { s = (data.max - data.min) / 255; z = Math.round(-data.min / s); }
      let q = Math.round(r / s) + z; q = Math.max(0, Math.min(255, q));
      e += (r - s * (q - z)) ** 2; n++;
    }
    return Math.sqrt(e / n);
  }

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const left = 40, right = w - 40, top = 60, bot = 250, span = 260;
    const rmin = data.min, rmax = data.max;

    // 两条数轴
    const modes = [
      { name: "对称量化（symmetric）", col: PAL.red },
      { name: "零点量化（asymmetric）", col: PAL.green }
    ];
    modes.forEach((m, idx) => {
      const y = top + idx * 95;
      ctx.strokeStyle = PAL.gray; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(left, y); ctx.lineTo(right, y); ctx.stroke();
      txt(ctx, m.name + "   r → q → r̂", left, y - 18, 14, m.col, "left");
      const sSym = Math.max(Math.abs(rmin), Math.abs(rmax)) / 127;
      const sAsym = (rmax - rmin) / 255;
      const zAsym = Math.round(-rmin / sAsym);
      // 采样点
      const N = 60;
      for (let i = 0; i <= N; i++) {
        const r = rmin + (rmax - rmin) * i / N;
        let q, s, z;
        if (idx === 0) { s = sSym; z = 0; } else { s = sAsym; z = zAsym; }
        q = Math.round(r / s) + z; q = Math.max(0, Math.min(255, q));
        const rhat = s * (q - z);
        const x = left + (r - rmin) / span * (right - left) * (span / (rmax - rmin) || 1);
        const xr = left + ((r - rmin) / (rmax - rmin || 1)) * (right - left);
        const xh = left + ((rhat - rmin) / (rmax - rmin || 1)) * (right - left);
        ctx.fillStyle = m.col;
        ctx.beginPath(); ctx.arc(xr, y, 2.4, 0, 6.28); ctx.fill();
        ctx.fillStyle = "rgba(226,105,79,0.85)";
        ctx.strokeStyle = "rgba(226,105,79,0.5)"; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(xr, y - 6); ctx.lineTo(xh, y - 16); ctx.stroke();
        ctx.beginPath(); ctx.arc(xh, y - 18, 2.2, 0, 6.28); ctx.fillStyle = PAL.orange; ctx.fill();
      }
      const rm = (rmin + rmax) / 2;
      ctx.fillStyle = PAL.orange; ctx.beginPath();
      ctx.arc(left + ((rm - rmin) / (rmax - rmin || 1)) * (right - left), y - 18, 2.5, 0, 6.28); ctx.fill();
      txt(ctx, "真实值 r（绿底点）", right - 10, y - 32, 12, PAL.green, "right");
      txt(ctx, "量化-反量化 r̂（橙点）", right - 10, y - 18, 12, PAL.orange, "right");
      // 浪费区间高亮（对称时）
      if (idx === 0 && data.min > 0) {
        ctx.fillStyle = "rgba(226,105,79,0.12)";
        ctx.fillRect(left, y - 4, right - left, 8);
        txt(ctx, "← 这一段全被浪费（没有负数数据）→", (left + right) / 2, y + 16, 12, PAL.red, "center");
      }
    });
    // 底部统计
    const eSym = mse("sym"), eAsym = mse("asym");
    txt(ctx, "对称量化 RMSE ≈ " + eSym.toFixed(3) + "　　vs　　零点量化 RMSE ≈ " + eAsym.toFixed(3),
      w / 2, 288, 16, eAsym < eSym ? PAL.green : PAL.red, "center");
    txt(ctx, "（RMSE = 均方根误差，越小越好；随机采样所以每次略有不同）", w / 2, 312, 12, PAL.gray, "center");
  }

  function tick() {
    if (auto) {
      t += 0.02;
      data.min = -0.5 + Math.sin(t * 1.3) * 1.2;
      data.max = 2.5 + Math.abs(Math.sin(t * 0.7)) * 5.5;
      if (data.min > 0.3) data.min = 0.05;
    }
    draw();
  }
  setInterval(tick, 50);

  const btnPlay = document.getElementById("demoA-play");
  const btnShuf = document.getElementById("demoA-shuffle");
  const stat = document.getElementById("demoA-stat");
  if (btnPlay) btnPlay.onclick = function () {
    auto = !auto;
    this.classList.toggle("on", auto);
    if (auto) { stat.textContent = "自动演示中：数据范围随波形变化"; }
    else { stat.textContent = "已暂停（可拖动范围滑块？当前为固定范围演示）"; }
  };
  if (btnShuf) btnShuf.onclick = function () {
    data.min = -Math.random() * 2;
    data.max = Math.random() * 6 + 0.5;
    if (stat) stat.textContent = "随机分布：min=" + data.min.toFixed(2) + " max=" + data.max.toFixed(2);
  };
})();

/* ============================================================
   演示 B · Booth 编码分步
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 360);
  if (!D) return;
  const { ctx } = D;
  let X = 85, Y = 42;
  let step = 0;            // 0=未开始, 1..4=编码组, 5=部分积, 6=求和
  let groups = [];
  let pp = [];

  function toTwos(v, bits) { // v -> 补码字符串
    let x = v < 0 ? (1 << bits) + v : v;
    let s = x.toString(2);
    while (s.length < bits) s = "0" + s;
    return s;
  }
  function boothGroups(y) {
    const bits = [];
    for (let i = 0; i < 8; i++) bits.push((y >> i) & 1); // LSB first
    const res = [];
    const table = {
      "000": 0, "001": 1, "010": 1, "011": 2,
      "100": -2, "101": -1, "110": -1, "111": 0
    };
    let prev = 0;
    for (let i = 0; i < 4; i++) {
      const b0 = bits[2 * i], b1 = bits[2 * i + 1] || 0, bm = prev;
      const key = "" + b1 + b0 + bm;
      const op = table[key];
      const sign = op < 0 ? "-" : "+";
      const mag = Math.abs(op);
      res.push({ key, op, label: (mag === 2 ? "2X" : mag === 1 ? "X" : "0") + (op === 0 ? "" : ""), shift: 2 * i });
      prev = bits[2 * i + 1] || 0;
    }
    return res;
  }

  function compute() {
    groups = boothGroups(Y);
    pp = groups.map(g => ({
      val: g.op * X,
      shift: g.shift,
      width: 9
    }));
  }

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, `Booth 编码乘法：X = ${X}（被乘数） × Y = ${Y}（乘数，8b 补码 ${toTwos(Y, 8)}）`, 30, 26, 16, PAL.white, "left");

    if (step === 0) {
      txt(ctx, "Y 按 Radix-4 每 2 位一组、重叠 1 位 → 4 组 → 4 个部分积", 30, 70, 14, PAL.gray);
      txt(ctx, "点击“▶ 开始 Booth 编码”逐组演示", 30, 100, 14, PAL.orange);
      return;
    }
    // 编码表
    const ty = 62, tx = 30, cw = 210, ch = 36;
    for (let i = 0; i < 4; i++) {
      const g = groups[i];
      const active = step === i + 1;
      ctx.fillStyle = active ? "#1d3a5c" : PAL.panel;
      ctx.strokeStyle = active ? PAL.orange : PAL.line;
      ctx.lineWidth = active ? 2.5 : 1.5;
      rrect(ctx, tx + i * (cw + 14), ty, cw, ch, 8); ctx.fill(); ctx.stroke();
      const bitStr = "组" + (i + 1) + ": " + g.key + " → " + (g.op === 0 ? "0" : (g.op > 0 ? "+" : "") + g.op) + "X";
      txt(ctx, bitStr, tx + i * (cw + 14) + 8, ty + ch / 2, 13, active ? PAL.orange : PAL.white, "left");
    }
    // 部分积区
    const py = 130, pw = 150, ph = 30;
    if (step >= 5) {
      txt(ctx, "生成的 4 个部分积（每个 9b 宽，按移位错开）：", 30, py - 8, 14, PAL.white);
      pp.forEach((p, i) => {
        const active = step === 5 && i === 0 ? false : true;
        const x = 30 + i * (pw + 10);
        ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 1.5;
        rrect(ctx, x, py, pw, ph, 6); ctx.fill(); ctx.stroke();
        const v = p.val * (2 ** p.shift);
        txt(ctx, `PP${i} = ${p.val}X × 2^${p.shift} = ${v}`, x + 8, py + ph / 2, 12.5, PAL.white, "left");
      });
    }
    // 求和区
    if (step >= 6) {
      let acc = 0;
      const sy = 210;
      ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(30, sy - 6); ctx.lineTo(30 + 640, sy - 6); ctx.stroke();
      pp.forEach((p, i) => {
        const v = p.val * (2 ** p.shift);
        acc += v;
        txt(ctx, `${i === 0 ? "" : "+ "}${v}`, 30 + i * 150, sy + 16, 14, PAL.white, "left");
      });
      txt(ctx, "= " + acc + "　（" + X + " × " + Y + " = " + X * Y + "　" + (acc === X * Y ? "✓ 一致" : "✗ 不一致！") + "）",
        30 + 4 * 150 + 10, sy + 16, 16, acc === X * Y ? PAL.green : PAL.red, "left");
    }
    if (step < 6) {
      txt(ctx, "下一步 →", 30, 320, 13, PAL.orange);
    }
  }

  const btnRun = document.getElementById("demoB-run");
  const btnStep = document.getElementById("demoB-step");
  const btnReset = document.getElementById("demoB-reset");
  const inX = document.getElementById("demoB-x");
  const inY = document.getElementById("demoB-y");
  const stat = document.getElementById("demoB-stat");

  function readInputs() {
    const x = parseInt(inX.value, 10), y = parseInt(inY.value, 10);
    if (!isNaN(x) && x >= -127 && x <= 127) X = x;
    if (!isNaN(y) && y >= -127 && y <= 127) Y = y;
    compute();
  }
  if (btnRun) btnRun.onclick = function () {
    readInputs(); step = 1; compute(); draw();
    if (stat) stat.textContent = `开始：X=${X}，Y=${Y}（${toTwos(Y, 8)}₂）`;
  };
  if (btnStep) btnStep.onclick = function () {
    if (step === 0) { readInputs(); step = 1; }
    else if (step < 6) step++;
    draw();
    if (stat) stat.textContent = step <= 4 ? `正在演示第 ${step} 组 Booth 编码` : step === 5 ? "正在生成部分积" : "求和完成";
  };
  if (btnReset) btnReset.onclick = function () {
    step = 0; compute(); draw();
    if (stat) stat.textContent = "已重置";
  };
  compute(); draw();
})();

/* ============================================================
   演示 C · 8b vs 9b 部分积加法树
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let mode8 = true;
  const stat = document.getElementById("demoC-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const nPP = mode8 ? 4 : 5;
    const wid = mode8 ? 9 : 10;
    const title = mode8 ? "8b×8b 有符号：4 个部分积（9b 宽）" : "9b×9b 有符号：5 个部分积（10b 宽）";
    txt(ctx, title, 30, 26, 17, mode8 ? PAL.green : PAL.red, "left");

    // 部分积条
    const y0 = 60, ph = 26, gap = 12, px = 40;
    for (let i = 0; i < nPP; i++) {
      const y = y0 + i * (ph + gap);
      const shift = i * 2;
      ctx.fillStyle = i === nPP - 1 && !mode8 ? "rgba(226,105,79,0.25)" : PAL.panel;
      ctx.strokeStyle = mode8 ? PAL.blue : (i === nPP - 1 ? PAL.red : PAL.purple);
      ctx.lineWidth = 1.5;
      rrect(ctx, px + shift * 4, y, wid * 11 + 10, ph, 6); ctx.fill(); ctx.stroke();
      txt(ctx, `PP${i}`, px + shift * 4 + 6, y + ph / 2, 12, PAL.white, "left");
      // 位格子
      for (let b = 0; b < wid; b++) {
        ctx.fillStyle = "rgba(15,124,182,0.35)";
        ctx.fillRect(px + shift * 4 + 30 + b * 11, y + 5, 9, ph - 10);
      }
    }
    // 加法树级
    const treeY = y0 + nPP * (ph + gap) + 6;
    txt(ctx, "CSA 加法树（按移位对齐合并）：", 40, treeY + 12, 14, PAL.white);
    const levels = mode8 ? [4, 2, 1] : [5, 3, 2, 1];
    const cellW = 40, cellH = 24;
    let lx = 40;
    levels.forEach((cnt, li) => {
      for (let k = 0; k < cnt; k++) {
        const x = lx + k * (cellW + 8);
        ctx.fillStyle = li === levels.length - 1 ? "#3a5c3a" : "#20344d";
        ctx.strokeStyle = PAL.green;
        rrect(ctx, x, treeY + 24 + li * (cellH + 10), cellW, cellH, 5); ctx.fill(); ctx.stroke();
        if (li === levels.length - 1) txt(ctx, "积", x + cellW / 2, treeY + 24 + li * (cellH + 10) + cellH / 2, 12, PAL.white, "center");
      }
      lx += cnt * (cellW + 8) + 18;
    });
    const sumW = mode8 ? 4 * 9 : 5 * 10;
    txt(ctx, "9b×9b 需要 5 个部分积 → 加法树多 1 层、总位宽多 " + (sumW - 36) + "b",
      40, treeY + 24 + levels.length * (cellH + 10) + 12, 13, mode8 ? PAL.gray : PAL.red, "left");
    if (stat) stat.textContent = mode8
      ? "加法树 3 级 · 部分积 4 个 · 每部分积 9b"
      : "加法树 4 级 · 部分积 5 个 · 每部分积 10b（多 1 棵树的成本！）";
  }

  const b8 = document.getElementById("demoC-switch");
  const b9 = document.getElementById("demoC-switch9");
  if (b8) b8.onclick = function () { mode8 = true; b8.classList.add("on"); b9.classList.remove("on"); draw(); };
  if (b9) b9.onclick = function () { mode8 = false; b9.classList.add("on"); b8.classList.remove("on"); draw(); };
  draw();
})();

/* ============================================================
   演示 D · 数据流仿真（一个计算列）
   ============================================================ */
(function () {
  const D = cvs("demoD", 980, 380);
  if (!D) return;
  const { ctx } = D;
  const NACT = 128, NWT = 128;
  let cycle = 0, running = false, timer = null;
  const stat = document.getElementById("demoD-stat");
  const s1 = document.getElementById("demoD-play");
  const s2 = document.getElementById("demoD-step");
  const s3 = document.getElementById("demoD-reset");

  // 状态：数据组在流水线中的位置 (0=输入,1..4=各级,5=输出)
  let wave = null; // { pos, act }
  let weightWrite = 0; // 0..32 后台写入进度（第二个权重组）

  function stepOnce() {
    cycle++;
    if (!wave) wave = { pos: 0 };
    else if (wave.pos < 5) wave.pos++;
    else wave = { pos: 0 };
    weightWrite = (weightWrite + 32 / 32) % 33;
    if (weightWrite > 32) weightWrite = 0;
    if (stat) stat.textContent = `周期 ${cycle} · 数据组位于流水线第 ${wave.pos + 1} 级${wave.pos >= 4 ? "（输出）" : ""}`;
    draw();
  }
  function auto() {
    if (!running) return;
    stepOnce();
    timer = setTimeout(auto, 650);
  }
  if (s1) s1.onclick = function () {
    running = !running;
    this.classList.toggle("on", running);
    this.textContent = running ? "⏸ 暂停" : "▶ 自动运行";
    if (running) { clearTimeout(timer); auto(); }
    else clearTimeout(timer);
  };
  if (s2) s2.onclick = function () { if (!running) stepOnce(); };
  if (s3) s3.onclick = function () { running = false; s1.textContent = "▶ 自动运行"; s1.classList.add("on"); clearTimeout(timer); cycle = 0; wave = null; weightWrite = 0; if (stat) stat.textContent = "周期 0 / 等待开始"; draw(); };

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);

    // 输入（128 个激活条）
    const x0 = 24, y0 = 70, bw = 6, bh = 4, cols = 32;
    txt(ctx, "128 个激活（8b）", x0, 44, 13, PAL.green, "left");
    for (let i = 0; i < 128; i++) {
      const c = i % cols, r = (i / cols) | 0;
      const lit = wave && wave.pos <= 1;
      ctx.fillStyle = lit ? "rgba(47,174,126," + (0.5 + 0.5 * ((i + cycle) % 5) / 4) + ")" : "rgba(47,174,126,0.18)";
      ctx.fillRect(x0 + c * (bw + 3), y0 + r * (bh + 3), bw, bh);
    }

    // 第 1 级
    const s1x = 250, s1y = 40, s1w = 130, s1h = 52;
    ctx.fillStyle = wave && wave.pos === 1 ? "#1d3a5c" : PAL.panel;
    ctx.strokeStyle = wave && wave.pos === 1 ? PAL.orange : PAL.blue; ctx.lineWidth = 2;
    rrect(ctx, s1x, s1y, s1w, s1h, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "第 1 级", s1x + 8, s1y + 18, 13, PAL.white);
    txt(ctx, "转换 ×128", s1x + 8, s1y + 38, 11, PAL.gray);

    // 广播总线
    ctx.strokeStyle = "rgba(15,124,182,0.7)"; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(s1x + s1w, s1y + 26); ctx.lineTo(w - 24, s1y + 26); ctx.stroke();
    txt(ctx, "广播 128 × 8b 有符号激活 → 32 个计算列", w / 2 + 100, s1y + 14, 11, PAL.gray, "center");

    // 4 个 bank（列示意）
    const bankX = [380, 540, 700, 860], bankY = 120, bankW = 110, bankH = 120;
    for (let b = 0; b < 4; b++) {
      const bx = bankX[b];
      ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.purple; ctx.lineWidth = 2;
      rrect(ctx, bx, bankY, bankW, bankH, 8); ctx.fill(); ctx.stroke();
      txt(ctx, `Bank ${b}`, bx + 8, bankY + 16, 12.5, PAL.white);
      txt(ctx, "32 路 CSA", bx + 8, bankY + 36, 11, PAL.gray);
      // 部分积堆
      const active = wave && (wave.pos === 2 || wave.pos === 3);
      for (let k = 0; k < 4; k++) {
        ctx.fillStyle = active ? "rgba(155,111,214,0.75)" : "rgba(155,111,214,0.25)";
        ctx.fillRect(bx + 10, bankY + 48 + k * 16, bankW - 20, 11);
      }
      // bank 输出
      ctx.fillStyle = wave && wave.pos === 3 ? PAL.orange : "rgba(232,163,61,0.2)";
      ctx.fillRect(bx + 10, bankY + 108, bankW - 20, 8);
    }
    txt(ctx, "第 2~3 级：部分积生成 → 32 路 CSA（跨乘数）→ 移位合并", bankX[0], bankY - 14, 13, PAL.purple, "left");

    // 权重存储（双缓冲）
    const wy = 270, wx = 380;
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.green; ctx.lineWidth = 1.5;
    rrect(ctx, wx, wy, 300, 64, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "权重组 A（计算中）", wx + 10, wy + 18, 12.5, PAL.white);
    ctx.fillStyle = "rgba(47,174,126,0.35)";
    for (let i = 0; i < 32; i++) ctx.fillRect(wx + 10 + i * 8.5, wy + 28, 6, 24);
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 1.5;
    rrect(ctx, wx + 320, wy, 300, 64, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "权重组 B（后台写入中）", wx + 330, wy + 18, 12.5, PAL.white);
    ctx.fillStyle = "rgba(232,163,61,0.35)";
    const prog = Math.min(32, weightWrite);
    for (let i = 0; i < prog; i++) ctx.fillRect(wx + 330 + i * 8.5, wy + 28, 6, 24);

    // 第 4 级与输出
    const f4x = 380, f4y = 350;
    ctx.fillStyle = wave && wave.pos === 4 ? "#4a3a1e" : PAL.panel;
    ctx.strokeStyle = wave && wave.pos === 4 ? PAL.orange : PAL.line; ctx.lineWidth = 2;
    rrect(ctx, f4x, f4y, 300, 26, 6); ctx.fill(); ctx.stroke();
    txt(ctx, "第 4 级：Σ 4 bank + 零点修正项 → 输出通道结果", f4x + 10, f4y + 13, 12, PAL.white);
    txt(ctx, `周期 ${cycle}`, w - 80, 24, 14, PAL.orange, "right");
  }
  draw();
})();

/* ============================================================
   演示 E · 流水线时空图
   ============================================================ */
(function () {
  const D = cvs("demoE", 980, 300);
  if (!D) return;
  const { ctx } = D;
  const names = ["A", "B", "C", "D", "E"];
  const colors = [PAL.blue, PAL.green, PAL.orange, PAL.purple, PAL.red];
  let cycle = 0, playing = false, timer = null;
  const stat = document.getElementById("demoE-stat");
  const slider = document.getElementById("demoE-slider");
  const btnPlay = document.getElementById("demoE-play");
  const btnReset = document.getElementById("demoE-reset");

  function posOf(name) { // 数据组 name 在周期 cycle 时位于哪一级 (0..4)，-1 表示还没进，5 表示已出
    const k = names.indexOf(name);
    const entered = cycle - k;   // 第 cycle 周期时已运行了几级
    if (entered < 1) return -1;
    if (entered >= 5) return 5;
    return entered - 1;
  }

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const sx = 60, sw = 200, gap = 12, y0 = 70, sh = 64;
    const stageNames = ["第 1 级 转换", "第 2 级 部分积+CSA", "第 3 级 移位合并", "第 4 级 求和+修正"];
    for (let s = 0; s < 4; s++) {
      ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.line; ctx.lineWidth = 1.5;
      rrect(ctx, sx, y0 + s * (sh + 14), sw, sh, 8); ctx.fill(); ctx.stroke();
      txt(ctx, stageNames[s], sx + 10, y0 + s * (sh + 14) + 16, 12.5, PAL.white);
    }
    txt(ctx, "← 时间", w - 40, y0 + 4 * (sh + 14) + 14, 12, PAL.gray, "right");
    // 数据组
    names.forEach((nm, k) => {
      const p = posOf(nm);
      if (p >= 0 && p < 4) {
        const x = sx + sw + 20 + k * 130;
        const y = y0 + p * (sh + 14) + 10;
        ctx.fillStyle = colors[k];
        rrect(ctx, x, y, 120, sh - 20, 8); ctx.fill();
        txt(ctx, "数据 " + nm, x + 60, y + (sh - 20) / 2, 14, "#0a1119", "center", "'Consolas',monospace");
      }
      if (p === 4) {
        const y = y0 + 4 * (sh + 14) + 2;
        ctx.fillStyle = colors[k];
        rrect(ctx, sx + sw + 20 + k * 130, y, 120, 30, 8); ctx.fill();
        txt(ctx, "数据 " + nm + " 输出 ✓", sx + sw + 20 + k * 130 + 60, y + 15, 12, "#0a1119", "center");
      }
    });
    txt(ctx, "周期 " + (cycle + 1), 60, 28, 15, PAL.orange, "left");
    if (stat) {
      const outCnt = names.filter(n => posOf(n) === 4).length;
      stat.textContent = `周期 ${cycle + 1} · 已输出 ${outCnt} 组 · 单组延迟 4 周期`;
    }
  }

  function setCycle(c) {
    cycle = Math.max(0, Math.min(9, c));
    if (slider) slider.value = cycle;
    draw();
  }
  if (slider) slider.oninput = function () { setCycle(parseInt(this.value, 10)); };
  if (btnPlay) btnPlay.onclick = function () {
    playing = !playing;
    this.classList.toggle("on", playing);
    this.textContent = playing ? "⏸ 暂停" : "▶ 自动播放";
    if (playing) {
      clearInterval(timer);
      timer = setInterval(function () {
        if (cycle >= 9) { playing = false; btnPlay.textContent = "▶ 自动播放"; clearInterval(timer); return; }
        setCycle(cycle + 1);
      }, 700);
    } else clearInterval(timer);
  };
  if (btnReset) btnReset.onclick = function () { playing = false; if (btnPlay) { btnPlay.textContent = "▶ 自动播放"; btnPlay.classList.add("on"); } clearInterval(timer); setCycle(0); };
  draw();
})();
