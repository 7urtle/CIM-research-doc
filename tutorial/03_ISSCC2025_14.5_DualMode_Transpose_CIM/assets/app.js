/* ============================================================
   转置 FP-CIM 教学教程 · 交互脚本
   演示 A 转置读取 · 演示 B SFME · 演示 C 精确 vs 近似
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
   演示 A · 转置读取
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let ff = true, cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const col = ff ? PAL.blue : PAL.red;
    txt(ctx, ff ? "FF：读行（A × W）" : "BP：读对角（G × Wᵀ）", 30, 24, 15, col, "left");
    const k = cyc % 6;
    // 6x6 网格
    for (let r = 0; r < 6; r++) {
      for (let c = 0; c < 6; c++) {
        const x = 120 + c * 70, y = 60 + r * 40;
        const active = ff ? (r === k) : (c === k);
        ctx.fillStyle = active ? (ff ? "#1e3c56" : "#3c2a26") : "#141c2a";
        ctx.strokeStyle = active ? col : PAL.line;
        ctx.lineWidth = active ? 3 : 1;
        rrect(ctx, x, y, 64, 34, 5); ctx.fill(); ctx.stroke();
      }
    }
    if (ff) {
      txt(ctx, "高亮第 " + k + " 行 → 权重向量（与激活对齐 → A×W）", 60, 270, 13, col, "left");
    } else {
      txt(ctx, "高亮第 " + k + " 条对角线 → 转置权重向量（G×Wᵀ）", 60, 270, 13, col, "left");
    }
    txt(ctx, "同一存储阵列 + 同一 256b 读口 + 同一套 MAC → FF/BP 复用", 60, 296, 12, PAL.gray, "left");
    if (stat) stat.textContent = ff ? "FF 模式：高亮第 " + k + " 行" : "BP 模式：高亮第 " + k + " 条对角线";
  }

  function tick() { cyc++; draw(); }
  const bFF = document.getElementById("demoA-ff");
  const bBP = document.getElementById("demoA-bp");
  const bPlay = document.getElementById("demoA-play");
  if (bFF) bFF.onclick = function () { ff = true; bFF.classList.add("on"); bBP.classList.remove("on"); draw(); };
  if (bBP) bBP.onclick = function () { ff = false; bBP.classList.add("on"); bFF.classList.remove("on"); draw(); };
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 700); } else clearInterval(timer);
  };
  if (play) timer = setInterval(tick, 700);
  draw();
})();

/* ============================================================
   演示 B · SFME 转换
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
    txt(ctx, "SFME：FP 权重 → 预对齐 → 有符号定点尾数", 30, 24, 15, PAL.white, "left");
    const k = cyc % 4;
    // 三段（符号/指数/尾数）
    const y0 = 70;
    const fields = [
      { name: "符号", w: 90, col: PAL.red, val: k % 2 },
      { name: "指数 E", w: 150, col: PAL.blue, val: 5 + k },
      { name: "尾数 1.M", w: 280, col: PAL.green, val: 10 + k },
    ];
    let x = 120;
    fields.forEach(f => {
      ctx.fillStyle = "#14263c"; ctx.strokeStyle = f.col; ctx.lineWidth = 2;
      rrect(ctx, x, y0, f.w, 44, 8); ctx.fill(); ctx.stroke();
      txt(ctx, f.name + " = " + f.val, x + 10, y0 + 22, 12, f.col, "left");
      x += f.w + 16;
    });
    // 预对齐
    ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(120, y0 + 60); ctx.lineTo(860, y0 + 60); ctx.stroke();
    txt(ctx, "预对齐：Es = Emax − Bias（共享指数）· 隐藏位+尾数 → Mn", 120, y0 + 82, 13, PAL.orange, "left");
    // SFME 结果
    ctx.fillStyle = "#1e3c2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
    rrect(ctx, 120, y0 + 100, 740, 44, 8); ctx.fill(); ctx.stroke();
    txt(ctx, "SFME：Ma = −1ˢ · 0.Mn（有符号定点补码尾数）→ 送进 4b/8b 整数乘法器", 130, y0 + 122, 13, PAL.white, "left");
    txt(ctx, "4b 对齐尾数复用 INT4 通路 · 8b 复用 INT8 通路 → FP 的 MAC 走整数数据通路", 120, y0 + 170, 12.5, PAL.gray, "left");
    txt(ctx, "四模式 4b 乘法器覆盖 8b 2C 的全部 4b 部分积组合 → 一个乘法器服务 4b/8b", 120, y0 + 196, 12.5, PAL.gray, "left");
    if (stat) stat.textContent = "例 " + (k + 1) + "：符号 " + (k % 2) + "，指数 " + (5 + k) + "，尾数 " + (10 + k);
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoB-play");
  const bReset = document.getElementById("demoB-reset");
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
   演示 C · 精确 vs 近似
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
    txt(ctx, "精确 vs 近似（DMBP-MAC）：" + ["精确：全部部分积", "近似：丢右侧 6 个部分和", "近似：低位 OR 代替加法"][k], 30, 24, 15, PAL.white, "left");
    // 部分积网格
    const dropped = k > 0;
    for (let r = 0; r < 6; r++) {
      for (let c = 0; c < 12; c++) {
        const x = 120 + c * 60, y = 60 + r * 30;
        const isDrop = dropped && c >= 9;
        ctx.fillStyle = isDrop ? "#3a2620" : "#1e3c56";
        ctx.strokeStyle = isDrop ? PAL.red : (dropped ? PAL.orange : PAL.green);
        ctx.lineWidth = isDrop ? 2 : 1;
        rrect(ctx, x, y, 54, 24, 4); ctx.fill(); ctx.stroke();
      }
    }
    if (dropped) {
      txt(ctx, "红色 = 近似模式丢弃的部分和（BAM）", 120, 260, 13, PAL.red, "left");
      txt(ctx, "低位加法换成按位 OR（LOA）+ 偏置补偿 → 无偏近似", 120, 286, 12, PAL.gray, "left");
    } else {
      txt(ctx, "全部部分积参与 → 精度最高（训练/精度敏感场景）", 120, 260, 13, PAL.green, "left");
    }
    if (stat) stat.textContent = ["精确：速度基准、功耗基准", "近似：速度 +12%、功耗 −31%", "近似：NMED 5.3%（高斯、均值≈0）"][k];
  }

  function tick() { cyc++; draw(); }
  const bPlay = document.getElementById("demoC-play");
  const bReset = document.getElementById("demoC-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 1300); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 1300);
  draw();
})();
