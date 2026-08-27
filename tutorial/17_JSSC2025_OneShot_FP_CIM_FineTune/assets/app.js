/* ============================================================
   One-Shot FP CIM 引擎教学教程 · 交互脚本
   演示 A one-shot 流水 · 演示 B ParMS 比较 · 演示 C ODFC 恢复
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
   演示 A · One-Shot 流水（8 周期 vs 1 周期）
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
    txt(ctx, "演示 A · One-Shot 流水：INT 尾数 MAC 从 8 周期 → 1 周期", 30, 24, 15, PAL.white, "left");
    const k = cyc % 12;
    // left: conventional pipeline (11 cycles total)
    txt(ctx, "传统（位串行）：总 11 周期", 160, 54, 13, PAL.red, "center");
    for (let c = 0; c < 11; c++) {
      const x = 40 + c * 24;
      const busy = (c >= 2 && c < 10) ? (c === k ? "#5a2a22" : "#3c2a26") : (c === k ? "#2a4a6a" : "#12202f");
      ctx.fillStyle = busy; ctx.strokeStyle = (c >= 2 && c < 10) ? PAL.red : PAL.blue; ctx.lineWidth = 1;
      rrect(ctx, x, 64, 20, 30, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(c + 1), x + 10, 79, 9, PAL.white, "center");
    }
    txt(ctx, "步骤③ 8 周期位串行（红框）→ ①②④ 电路闲置 87.5%", 160, 112, 11.5, PAL.red, "center");
    // mantissa bits being processed one at a time
    const bit = k >= 2 && k < 10 ? (k - 2) : -1;
    const mbits = [1, 0, 1, 1, 0, 1, 0, 1];
    for (let b = 0; b < 8; b++) {
      const x = 80 + b * 40;
      ctx.fillStyle = b === bit ? "#5a2a22" : "#12202f";
      ctx.strokeStyle = b === bit ? PAL.red : PAL.line; ctx.lineWidth = b === bit ? 2 : 1;
      rrect(ctx, x, 126, 32, 26, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(mbits[b]), x + 16, 139, 12, PAL.white, "center");
    }
    txt(ctx, bit >= 0 ? "第 " + (bit + 1) + "/8 位（每周期 1 位）" : "步骤③等待…", 160, 172, 11.5, PAL.red, "center");

    // right: one-shot pipeline (3 stages, 1 cycle each)
    txt(ctx, "One-Shot：3 级流水各 1 周期", 700, 54, 13, PAL.green, "center");
    const stages = ["输入对齐\n(ManAU)", "最小选择\n(CIM core)", "INT→FP\n(ITFU)"];
    for (let s = 0; s < 3; s++) {
      const x = 500 + s * 150;
      const active = (k % 3 === s);
      ctx.fillStyle = active ? "#1e3c2c" : "#12202f";
      ctx.strokeStyle = PAL.green; ctx.lineWidth = active ? 3 : 1.5;
      rrect(ctx, x, 64, 130, 46, 8); ctx.fill(); ctx.stroke();
      const lines = stages[s].split("\n");
      txt(ctx, lines[0], x + 65, 78, 12.5, active ? PAL.green : PAL.white, "center");
      txt(ctx, lines[1], x + 65, 96, 10.5, PAL.gray, "center");
    }
    // 8 mantissa bits all at once
    for (let b = 0; b < 8; b++) {
      const x = 520 + b * 40;
      ctx.fillStyle = mbits[b] ? "#1e4a76" : "#101c2c";
      ctx.strokeStyle = PAL.blue; ctx.lineWidth = 1;
      rrect(ctx, x, 126, 32, 26, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(mbits[b]), x + 16, 139, 12, PAL.white, "center");
    }
    txt(ctx, "8 位并行最小选择 → 1 周期完成（吞吐 8×）", 700, 172, 12, PAL.green, "center");
    txt(ctx, "Σ|xi−wi| = Σxi + Σwi − 2Σmin（最小选择比乘法简单得多）", 700, 202, 11.5, PAL.gray, "center");
    txt(ctx, "→ 100% 硬件利用率 · 位并行利用 MSB 相关性降翻转率", 700, 228, 11.5, PAL.orange, "center");
    if (stat) stat.textContent = "传统位串行：步骤③第 " + (bit + 1) + "/8 位 vs One-Shot：3 级流水各 1 周期";
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
   演示 B · ParMS 8-bit 比较（MSB 优先）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");
  const Wb = [1, 0, 1, 1, 0, 1, 0, 1]; // W = 0xB5 = 181
  const Xb = [1, 0, 1, 1, 0, 0, 1, 0]; // X = 0xB2 = 178 -> W > X -> min = X

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 B · ParMS：8-bit 并行最小选择（W vs X，MSB 优先比较）", 30, 24, 15, PAL.white, "left");
    const k = cyc % 9;
    const step = k; // 0..8
    const bs = 64, bx = 120, by = 60;
    txt(ctx, "W", 90, by + 15, 13, PAL.orange, "right");
    for (let c = 0; c < 8; c++) {
      const x = bx + c * bs;
      ctx.fillStyle = "#3c2a1a"; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 1;
      rrect(ctx, x, by, bs - 8, 30, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(Wb[c]), x + (bs - 8) / 2, by + 15, 14, PAL.white, "center");
    }
    txt(ctx, "X", 90, by + 45, 13, PAL.blue, "right");
    for (let c = 0; c < 8; c++) {
      const x = bx + c * bs;
      ctx.fillStyle = "#1e3a5c"; ctx.strokeStyle = PAL.blue; ctx.lineWidth = 1;
      rrect(ctx, x, by + 28, bs - 8, 30, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(Xb[c]), x + (bs - 8) / 2, by + 43, 14, PAL.white, "center");
    }
    // highlight current comparison bit (MSB first: index 7-step)
    let cmpBit = -1;
    if (step < 8) {
      cmpBit = 7 - step;
      const x = bx + cmpBit * bs;
      ctx.strokeStyle = PAL.orange; ctx.lineWidth = 3;
      ctx.strokeRect(x - 3, by - 3, bs - 2, 64);
    }
    // compute comparison
    let msg;
    if (step === 0) {
      msg = "MSB：W[7]=1 vs X[7]=1 → 相等，继续";
    } else {
      // find first differing bit from MSB
      let diff = -1;
      for (let i = 7; i >= 0; i--) { if (Wb[i] !== Xb[i]) { diff = i; break; } }
      if (step > 7 - diff) {
        msg = "第 " + (8 - diff) + " 位分出胜负：W=" + Wb[diff] + " vs X=" + Xb[diff] + " → W" + (Wb[diff] > Xb[diff] ? ">" : "<") + "X";
      } else {
        msg = "比较第 " + (step + 1) + " 位（MSB 起）：W=" + Wb[cmpBit] + " vs X=" + Xb[cmpBit] + (Wb[cmpBit] === Xb[cmpBit] ? " → 相等，继续" : " → 分出胜负！");
      }
    }
    txt(ctx, msg, 60, 128, 13.5, PAL.orange, "left");
    // result
    let min = "";
    for (let i = 0; i < 8; i++) min += (Wb[i] <= Xb[i] ? Wb[i] : Xb[i]).toString();
    txt(ctx, "min(W,X) = " + min + "（逐位取较小者，由 LESS 信号控制选择单元）", 60, 154, 13, PAL.green, "left");
    // G/P logic
    txt(ctx, "编码器并行生成：G⟨i⟩=W⟨i⟩&XB⟨i⟩ · P⟨i⟩=WB⟨i⟩|XB⟨i⟩（XB、WB 为反相）", 60, 184, 11.5, PAL.gray, "left");
    txt(ctx, "比较树：LESS = G⟨7:4⟩ + P⟨7:4⟩G⟨3:0⟩（三级嵌套，免反相器）", 60, 208, 11.5, PAL.gray, "left");
    txt(ctx, "vs INT8 乘法器：面积 −11.5× · 能耗 −8.2× ｜ 三态门控 → 加法树 −44%", 60, 240, 12.5, PAL.orange, "left");
    if (stat) stat.textContent = msg;
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
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

/* ============================================================
   演示 C · ODFC 精度恢复
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 C · ODFC 片上微调：环境变化掉精度 → 微调恢复", 30, 24, 15, PAL.white, "left");
    const k = cyc % 12;
    const epoch = k; // 0..11
    // curve: train 99.1, test 13.8, fine-tune 1..10 -> 84.3
    const x0 = 90, x1 = 900, y0 = 70, y1 = 220;
    ctx.strokeStyle = "#1c2c42"; ctx.lineWidth = 1;
    for (let gx = x0; gx <= x1; gx += 81) { ctx.beginPath(); ctx.moveTo(gx, y0); ctx.lineTo(gx, y1); ctx.stroke(); }
    for (let gy = y0; gy <= y1; gy += 30) { ctx.beginPath(); ctx.moveTo(x0, gy); ctx.lineTo(x1, gy); ctx.stroke(); }
    function yv(a) { return y1 - (a / 100) * (y1 - y0); }
    // points
    const pts = [{ x: x0 + 30, a: 99.1 }, { x: x0 + 130, a: 13.8 }];
    for (let e = 1; e <= 10; e++) {
      const acc = 13.8 + (84.3 - 13.8) * (1 - Math.pow(1 - e / 10, 2.2));
      pts.push({ x: x0 + 130 + e * (x1 - x0 - 160) / 10, a: acc });
    }
    for (let j = 1; j < pts.length; j++) {
      ctx.strokeStyle = j === 1 ? PAL.red : PAL.green; ctx.lineWidth = j === 1 ? 2 : 3;
      ctx.beginPath();
      ctx.moveTo(pts[j - 1].x, yv(pts[j - 1].a));
      ctx.lineTo(pts[j].x, yv(pts[j].a));
      ctx.stroke();
    }
    // current point
    let cur;
    if (epoch === 0) cur = pts[0];
    else if (epoch === 1) cur = pts[1];
    else cur = pts[Math.min(1 + epoch, pts.length - 1)];
    ctx.fillStyle = PAL.orange;
    ctx.beginPath(); ctx.arc(cur.x, yv(cur.a), 6, 0, 7); ctx.fill();
    // labels
    txt(ctx, "99.1%", x0 + 30, yv(99.1) - 12, 10, PAL.green, "center");
    txt(ctx, "13.8%", x0 + 130, yv(13.8) + 14, 10, PAL.red, "center");
    txt(ctx, "84.3%", x1 - 8, yv(84.3) - 12, 10, PAL.green, "right");
    txt(ctx, "训练", x0 + 30, y1 + 14, 10, PAL.gray, "center");
    txt(ctx, "MNIST-M 测试", x0 + 130, y1 + 14, 10, PAL.gray, "center");
    txt(ctx, "ODFC 微调 epochs →", x1 - 120, y1 + 14, 10, PAL.gray, "center");
    // current status
    const status = epoch === 0 ? "训练集：99.1%" : epoch === 1 ? "环境变化（MNIST-M）：13.8%！" : "ODFC 微调 " + (epoch - 1) + " epochs：≈" + (13.8 + (84.3 - 13.8) * (1 - Math.pow(1 - (epoch - 1) / 10, 2.2))).toFixed(1) + "%";
    txt(ctx, status, 60, 248, 14, epoch === 1 ? PAL.red : PAL.green, "left");
    // ODFC notes
    ctx.fillStyle = PAL.panel; ctx.strokeStyle = PAL.purple; ctx.lineWidth = 2;
    rrect(ctx, 60, 272, 860, 40, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "ODFC：128 轮顺序更新权重（每轮 16 个）· 时分复用（面积 −10%）· 保损失 FP 加法 · 2.88 GOPS @180MHz", 80, 292, 12.5, PAL.white, "left");
    if (stat) stat.textContent = status;
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
