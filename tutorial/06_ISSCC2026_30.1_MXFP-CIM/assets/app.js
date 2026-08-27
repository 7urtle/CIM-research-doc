/* ============================================================
   MXFP-CIM 教学教程 · 交互脚本
   演示 A SDBS 滑动 · 演示 B MXFP 映射 · 演示 C PBW 分配
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
   演示 A · SDBS 滑动乘法
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 320);
  if (!D) return;
  const { ctx } = D;
  const mw = "101101";
  const mn = "101001";
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "SDBS 双位滑动：MIN 每周期右滑 2b，垂直截断", 30, 24, 15, PAL.white, "left");
    // MW
    txt(ctx, "权重 MW（固定）", 60, 60, 13, PAL.green);
    for (let k = 0; k < 6; k++) {
      ctx.fillStyle = "#1e3c2c"; ctx.strokeStyle = PAL.green; ctx.lineWidth = 2;
      rrect(ctx, 260 + k * 44, 48, 36, 26, 5); ctx.fill(); ctx.stroke();
      txt(ctx, mw[k], 260 + k * 44 + 18, 61, 12, PAL.white, "center");
    }
    // MIN
    txt(ctx, "输入 MIN（滑动 " + cyc * 2 + " bit）", 60, 106, 13, PAL.blue);
    const shift = Math.min(cyc, 6);
    for (let k = 0; k < 8; k++) {
      const x0 = 260 + k * 44;
      const has = k >= shift && k - shift < 6;
      ctx.fillStyle = has ? "#18344e" : "#1c2638";
      ctx.strokeStyle = has ? PAL.blue : PAL.line; ctx.lineWidth = 2;
      rrect(ctx, x0, 94, 36, 26, 5); ctx.fill(); ctx.stroke();
      if (has) txt(ctx, mn[k - shift], x0 + 18, 107, 12, PAL.white, "center");
    }
    // 乘积段
    ctx.strokeStyle = PAL.line; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(60, 150); ctx.lineTo(w - 60, 150); ctx.stroke();
    // 已滑出的部分积（垂直截断示意）
    const activeCols = Math.max(1, shift + 1);
    for (let k = 0; k < 6; k++) {
      const x0 = 80 + k * 130;
      const active = k < activeCols;
      ctx.fillStyle = active ? "#2a2440" : PAL.panel;
      ctx.strokeStyle = active ? PAL.purple : PAL.line; ctx.lineWidth = 1.5;
      rrect(ctx, x0, 170, 110, 70, 8); ctx.fill(); ctx.stroke();
      txt(ctx, "部分积 " + k, x0 + 55, 190, 11, active ? PAL.purple : PAL.gray, "center");
      txt(ctx, active ? "（整列，无无效位）" : "（待滑动）", x0 + 55, 212, 10, active ? PAL.gray : PAL.gray, "center");
    }
    txt(ctx, "PBW = 周期数：低 PBW 少滑几步（快），高 PBW 多滑几步（准）", 60, 270, 13, PAL.orange, "left");
    txt(ctx, "ESUM 大的输入先滑 → 高位优先对齐", 60, 296, 12, PAL.gray, "left");
    if (stat) stat.textContent = "周期 " + cyc + " · MIN 已滑 " + cyc * 2 + " bit · 已产出 " + activeCols + " 个垂直截断部分积";
  }

  function tick() { cyc = Math.min(8, cyc + 1); draw(); }
  const bPlay = document.getElementById("demoA-play");
  const bReset = document.getElementById("demoA-reset");
  if (bPlay) bPlay.onclick = function () {
    play = !play;
    this.classList.toggle("on", play);
    this.textContent = play ? "⏸ 暂停" : "▶ 播放";
    if (play) { clearInterval(timer); timer = setInterval(tick, 700); } else clearInterval(timer);
  };
  if (bReset) bReset.onclick = function () { cyc = 0; draw(); };
  if (play) timer = setInterval(tick, 700);
  draw();
})();

/* ============================================================
   演示 B · MXFP8 / MXFP6 映射
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 320);
  if (!D) return;
  const { ctx } = D;
  let m8 = true;
  const stat = document.getElementById("demoB-stat");

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    const col = m8 ? PAL.blue : PAL.purple;
    txt(ctx, m8 ? "MXFP8（E4M3）：9 个数 / 子阵列" : "MXFP6（E2M3）：12 个数 / 子阵列", 30, 24, 15, col, "left");
    // 子阵列网格 6 行 x 12 列（示意）
    for (let r = 0; r < 6; r++) {
      const even = r % 2 === 0;
      for (let c = 0; c < 12; c++) {
        const x = 80 + c * 58, y = 60 + r * 36;
        let used;
        if (m8) {
          // 9 个数：占用 9 个尾数槽（偶数行）与 9 个指数槽（奇数行）
          used = (r < 4 && c < 10) || (r === 4 && c < 8);
        } else {
          used = r < 6 && c < 12;
        }
        ctx.fillStyle = even ? "#1e3a56" : "#3a2c1e";
        ctx.strokeStyle = used ? (even ? col : PAL.orange) : PAL.line;
        ctx.lineWidth = used ? 2 : 1;
        rrect(ctx, x, y, 50, 30, 5); ctx.fill(); ctx.stroke();
        if (r === 0 && c === 0) txt(ctx, even ? "符号+尾数" : "指数", x + 25, y + 15, 8.5, PAL.white, "center");
      }
    }
    txt(ctx, m8 ? "9 × 8b = 72b → 子阵列满用" : "12 × 6b = 72b → 子阵列满用（奇数行并排 2 个指数）", 80, 270, 13, PAL.green, "left");
    txt(ctx, "隐藏位 MW[3] 不占存储（写时全局预解码、算时本地恢复）→ 解码器面积 −63.1%", 80, 296, 12, PAL.gray, "left");
    if (stat) stat.textContent = m8 ? "MXFP8：偶数行=符号+尾数，奇数行=4b 指数，9 数/阵列" : "MXFP6：偶数行=符号+尾数，奇数行=2 个指数并排，12 数/阵列";
  }

  const b8 = document.getElementById("demoB-8");
  const b6 = document.getElementById("demoB-6");
  if (b8) b8.onclick = function () { m8 = true; b8.classList.add("on"); b6.classList.remove("on"); draw(); };
  if (b6) b6.onclick = function () { m8 = false; b6.classList.add("on"); b8.classList.remove("on"); draw(); };
  draw();
})();

/* ============================================================
   演示 C · PBW 分配（层 / 组）
   ============================================================ */
(function () {
  const D = cvs("demoC", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoC-stat");
  const layers = [
    { name: "层1 embedding", pbw: 5, sens: 0.2 },
    { name: "层2 attn", pbw: 11, sens: 0.8 },
    { name: "层3 mlp", pbw: 13, sens: 0.9 },
    { name: "层4 attn", pbw: 11, sens: 0.75 },
    { name: "层5 mlp", pbw: 13, sens: 0.85 },
    { name: "层6 head", pbw: 9, sens: 0.4 },
  ];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "层级 CGA：按敏感度分配 PBW（不敏感层低位宽、敏感层高位宽）", 30, 24, 15, PAL.orange, "left");
    layers.forEach((L, i) => {
      const x = 60 + i * 145;
      const active = (cyc % layers.length) === i;
      ctx.fillStyle = active ? "#4a3a26" : PAL.panel;
      ctx.strokeStyle = active ? PAL.orange : PAL.line; ctx.lineWidth = active ? 2.5 : 1.5;
      rrect(ctx, x, 60, 130, 130, 10); ctx.fill(); ctx.stroke();
      txt(ctx, L.name, x + 65, 82, 11.5, PAL.white, "center");
      // PBW 条
      const bw = 26 * (L.pbw / 15);
      ctx.fillStyle = "#1e3c2c"; ctx.strokeStyle = PAL.green;
      rrect(ctx, x + 15, 100, 100, 16, 5); ctx.fill(); ctx.stroke();
      ctx.fillStyle = PAL.green;
      ctx.fillRect(x + 17, 102, bw, 12);
      txt(ctx, "PBW " + L.pbw + "b", x + 65, 132, 12, active ? PAL.orange : PAL.green, "center");
      txt(ctx, "敏感度 " + (L.sens * 100).toFixed(0) + "%", x + 65, 152, 10, PAL.gray, "center");
      txt(ctx, "周期 " + Math.max(2, Math.round(L.pbw / 2)) + " 个", x + 65, 172, 10, PAL.gray, "center");
    });
    txt(ctx, "CGA 平均 PBW 较固定高精度：−14.8%（LLaMA-3.1 8B，精度无损）", 60, 224, 13, PAL.green, "left");
    txt(ctx, "组级 FGA 再按共享尺度 SS 微调：SS 大的组多算、SS 小的组少算 → 再 −29.3%", 60, 250, 13, PAL.orange, "left");
    txt(ctx, "→ 精度-效率甜点：vs 固定 19b 吞吐 +1.20~1.43×；vs 固定 11b 精度 +1.49×", 60, 278, 12, PAL.gray, "left");
    if (stat) stat.textContent = "正在查看：" + layers[cyc % layers.length].name + "（PBW " + layers[cyc % layers.length].pbw + "b）";
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
