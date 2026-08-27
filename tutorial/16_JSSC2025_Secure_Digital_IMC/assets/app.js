/* ============================================================
   安全数字 IMC 教学教程 · 交互脚本
   演示 A Boolean 共享 · 演示 B XNOR vs AND · 演示 C CPA
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
   演示 A · Boolean 共享（3 份）
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
    txt(ctx, "演示 A · Boolean 共享：b = b1⊕b2⊕b3（单份看似随机）", 30, 24, 15, PAL.white, "left");
    const k = cyc % 8;
    const b = (k >> 2) & 1;
    const b1 = (k >> 1) & 1, b2 = k & 1;
    const b3 = b1 ^ b2 ^ b;
    const bs = 90, bx = 120, by = 70;
    // three shares
    const shares = [[b1, "b1"], [b2, "b2"], [b3, "b3"]];
    for (let i = 0; i < 3; i++) {
      const x = bx + i * (bs + 20);
      ctx.fillStyle = i === 2 ? "#1c3a2c" : "#122c3c";
      ctx.strokeStyle = i === 2 ? PAL.green : PAL.blue; ctx.lineWidth = 2;
      rrect(ctx, x, by, bs, 60, 8); ctx.fill(); ctx.stroke();
      txt(ctx, shares[i][1] + " = " + shares[i][0], x + bs / 2, by + 30, 16, PAL.white, "center");
    }
    // XOR chain
    txt(ctx, "⊕", bx + bs + 7, by + 30, 18, PAL.orange, "center");
    txt(ctx, "⊕", bx + 2 * (bs + 20) - 6, by + 30, 18, PAL.orange, "center");
    txt(ctx, "→ 恢复 b = " + b, bx + 3 * (bs + 20) + 10, by + 30, 16, PAL.green, "center");
    // power bars
    txt(ctx, "单份功耗（看不出 b）", 140, 170, 12.5, PAL.gray, "center");
    for (let i = 0; i < 3; i++) {
      const x = bx + i * (bs + 20) + 10;
      const hgt = 30 + ((shares[i][0] * 37 + i * 13 + k * 7) % 41);
      ctx.fillStyle = i === 2 ? PAL.green : PAL.blue;
      ctx.fillRect(x, 200 - hgt, bs - 20, hgt);
    }
    txt(ctx, "每份功耗随机波动 → 三者之和也统计无关（非完备性）", 480, 230, 13, PAL.white, "center");
    txt(ctx, "正确性：b1⊕b2⊕b3 = " + (b1 ^ b2 ^ b3) + " = 秘密 b = " + b, 480, 256, 13.5, PAL.green, "center");
    txt(ctx, "非完备性：每个子函数只碰输入份的严格子集 → 子电路功耗与真实数据无关", 480, 284, 12.5, PAL.gray, "center");
    if (stat) stat.textContent = "b=" + b + "，共享 (" + b1 + "," + b2 + "," + b3 + ")，b1⊕b2⊕b3=" + (b1 ^ b2 ^ b3);
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1200); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1200);
  draw();
})();

/* ============================================================
   演示 B · XNOR vs AND（乘法共享）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 B · XNOR 乘法（线性）vs AND 乘法（非线性）", 30, 24, 15, PAL.white, "left");
    const k = cyc % 2;
    // input shares
    const a = k; // activation bit
    const a1 = 1, a2 = 0, a3 = a1 ^ a2 ^ a;  // 0,1 -> shares
    const wv = 1; // weight bit fixed
    const w1 = 0, w2 = 1, w3 = w1 ^ w2 ^ wv; // 0,1 -> shares
    // XNOR result (share-wise): t = XNOR(a,w) computed on each share pair
    const xn = (sh1, sh2) => 1 - (sh1 ^ sh2);
    const t1 = xn(a1, w1), t2 = xn(a2, w2), t3 = xn(a3, w3);
    const xnorRec = t1 ^ t2 ^ t3;
    const andRec = (a1 & w1) ^ (a2 & w2) ^ (a3 & w3);
    const xnorTrue = 1 - (a ^ wv);
    const andTrue = a & wv;
    // left: XNOR
    ctx.fillStyle = "#122c1c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 40, 60, 440, 200, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "XNOR 乘法（线性，本论文）", 60, 84, 14, PAL.green, "left");
    const px = 70, py = 100, bs = 90;
    txt(ctx, "激活份 a1a2a3：", px, py, 12, PAL.gray, "left");
    const av = [a1, a2, a3];
    for (let i = 0; i < 3; i++) {
      const x = px + 130 + i * bs;
      ctx.fillStyle = "#1c3a2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 1.5;
      rrect(ctx, x, py - 12, bs - 10, 26, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(av[i]), x + (bs - 10) / 2, py, 14, PAL.white, "center");
    }
    txt(ctx, "权重份 w1w2w3：", px, py + 34, 12, PAL.gray, "left");
    const wv2 = [w1, w2, w3];
    for (let i = 0; i < 3; i++) {
      const x = px + 130 + i * bs;
      ctx.fillStyle = "#1c3a2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 1.5;
      rrect(ctx, x, py + 22, bs - 10, 26, 4); ctx.fill(); ctx.stroke();
      txt(ctx, String(wv2[i]), x + (bs - 10) / 2, py + 34, 14, PAL.white, "center");
    }
    txt(ctx, "每份独立 XNOR：t1=" + t1 + "，t2=" + t2 + "，t3=" + t3, px, py + 80, 12.5, PAL.white, "left");
    txt(ctx, "恢复：t1⊕t2⊕t3 = " + xnorRec + " = XNOR(" + a + "," + wv + ")=" + xnorTrue + " ✓", px, py + 108, 14, PAL.green, "left");
    txt(ctx, "6 门等效 · 0 随机比特 · 天然均匀+抗毛刺", px, py + 134, 12.5, PAL.gray, "left");

    // right: AND
    ctx.fillStyle = "#2c1a1a"; ctx.strokeStyle = PAL.red; ctx.lineWidth = 2;
    rrect(ctx, 500, 60, 440, 200, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "AND 乘法（非线性，传统）", 520, 84, 14, PAL.red, "left");
    txt(ctx, "同样输入份：", 520, 110, 12, PAL.gray, "left");
    txt(ctx, "AND 共享后：t1⊕t2⊕t3 = " + andRec + "，但真值 AND(" + a + "," + wv + ")=" + andTrue + " ✗", 520, 140, 13, PAL.red, "left");
    txt(ctx, "→ 非线性破坏正确性 → 需要 remask（随机比特）", 520, 166, 12.5, PAL.red, "left");
    txt(ctx, "48 门等效 · 2 随机比特/周期 · 需输出寄存器", 520, 192, 12.5, PAL.gray, "left");
    txt(ctx, "IMC 百万并行 MAC → 随机比特开销反超计算", 520, 216, 12.5, PAL.orange, "left");
    txt(ctx, "→ 不可扩展！", 520, 240, 13, PAL.red, "left");

    txt(ctx, "SV/BV 换算 + 校正因子 → XNOR 也能算多位 MAC（SV=2·BV−(2ⁿ−1)）", 60, 280, 13.5, PAL.orange, "left");
    txt(ctx, "校正：SVout = 2·BVout − (2ⁿᵂ−1)(2ⁿᴬ−1)·r（常量预计算）→ NN 精度零影响", 60, 304, 12.5, PAL.gray, "left");
    if (stat) stat.textContent = "XNOR 恢复=" + xnorRec + " ✓ vs AND 恢复=" + andRec + " ✗";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
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

/* ============================================================
   演示 C · CPA（相关性不可区分）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");
  const nGuess = 16; // 4-bit key guesses

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "演示 C · CPA：正确密钥的相关性是否可区分？（左未保护 / 右保护）", 30, 24, 15, PAL.white, "left");
    const k = cyc % 2;
    // left: unprotected
    ctx.fillStyle = "#1c2838"; ctx.strokeStyle = PAL.red; ctx.lineWidth = 2;
    rrect(ctx, 40, 60, 440, 220, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "未保护：正确密钥（红）相关性最高 → 一击即中", 60, 84, 13, PAL.red, "left");
    // bars: guess correlations
    for (let i = 0; i < nGuess; i++) {
      const x = 60 + i * 26;
      const isCorrect = (i === 5);
      const hgt = isCorrect ? 120 : 20 + ((i * 31 + 7) % 30);
      ctx.fillStyle = isCorrect ? PAL.red : "#3a5a7a";
      ctx.fillRect(x, 240 - hgt, 18, hgt);
      if (isCorrect) txt(ctx, "✓", x + 9, 252, 11, PAL.red, "center");
    }
    txt(ctx, "正确密钥（红）远超其他猜测 → 可被识别", 60, 268, 12, PAL.gray, "left");

    // right: protected
    ctx.fillStyle = "#122c1c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 500, 60, 440, 220, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "保护后：所有猜测相关性混杂 → 不可区分", 520, 84, 13, PAL.green, "left");
    for (let i = 0; i < nGuess; i++) {
      const x = 520 + i * 26;
      const isCorrect = (i === 5);
      const hgt = 30 + ((i * 17 + 11 + k * 5) % 34);
      ctx.fillStyle = isCorrect ? "#3cbe8c" : "#1e5a4a";
      ctx.fillRect(x, 240 - hgt, 18, hgt);
    }
    txt(ctx, "正确密钥（绿）与错误猜测（灰）重叠 → 不可识别", 520, 268, 12, PAL.gray, "left");

    txt(ctx, "CPA 结果：保护后乘法/加法树/累加器/ASCON 全部通过（论文 Fig.9）", 60, 300, 13, PAL.white, "left");
    if (stat) stat.textContent = k === 0 ? "未保护：正确密钥可区分" : "保护后：正确密钥不可区分";
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
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
