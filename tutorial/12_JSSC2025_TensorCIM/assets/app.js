/* ============================================================
   TensorCIM 教学教程 · 交互脚本
   演示 A 冗余采集 · 演示 B 有效操作识别 · 演示 C 利用率
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
   演示 A · 冗余采集（REGM）
   ============================================================ */
(function () {
  const D = cvs("demoA", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoA-stat");
  const features = [
    { name: "f0", cnt: 5 }, { name: "f1", cnt: 3 }, { name: "f2", cnt: 1 },
    { name: "f3", cnt: 4 }, { name: "f4", cnt: 1 }, { name: "f5", cnt: 1 },
  ];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "REGM 冗余消除：高频特征住进 CIM，低频从 DRAM 取", 30, 24, 15, PAL.white, "left");
    features.forEach((f, i) => {
      const x = 60 + i * 145;
      const hot = f.cnt >= 3;
      ctx.fillStyle = hot ? "#1e3c2c" : PAL.panel;
      ctx.strokeStyle = hot ? PAL.green : PAL.line; ctx.lineWidth = 2;
      rrect(ctx, x, 60, 130, 80, 10); ctx.fill(); ctx.stroke();
      txt(ctx, f.name, x + 65, 85, 16, hot ? PAL.green : PAL.gray, "center");
      txt(ctx, "访问 " + f.cnt + " 次", x + 65, 108, 12, PAL.white, "center");
      txt(ctx, hot ? "✓ 在 CIM" : "✗ 需 DRAM", x + 65, 130, 11, hot ? PAL.green : PAL.red, "center");
    });
    // 归约复用
    ctx.fillStyle = "#2a2440"; ctx.strokeStyle = PAL.orange; ctx.lineWidth = 2;
    rrect(ctx, 60, 160, 860, 60, 10); ctx.fill(); ctx.stroke();
    txt(ctx, "归约复用：f0+f3 被反复需要 → 结果存 CIM，直接复用（不重算）", 80, 184, 14, PAL.orange, "left");
    txt(ctx, "未命中才触发 DRAM/跨芯粒访问；低频特征进驱逐 FIFO", 80, 208, 12, PAL.gray, "left");
    txt(ctx, "→ DRAM −1.74× · 跨芯粒 −3.55× · 归约 −1.35×（GCN Pubmed）", 60, 260, 13.5, PAL.green, "left");
    if (stat) stat.textContent = "高频特征（≥3 次）驻留 CIM；低频走 DRAM；归约结果复用";
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
   演示 B · 有效操作识别（EOCI）
   ============================================================ */
(function () {
  const D = cvs("demoB", 980, 300);
  if (!D) return;
  const { ctx } = D;
  let cyc = 0, play = true, timer = null;
  const stat = document.getElementById("demoB-stat");
  const gt = [0, 1, 2, 3, 4, 7];
  const wt = [0, 4, 5, 6, 7];

  function draw() {
    const w = D.w, h = D.h;
    ctx.fillStyle = PAL.bg; ctx.fillRect(0, 0, w, h);
    txt(ctx, "EOCI 有效操作识别：GT 非零列 ∩ WT 非零行", 30, 24, 15, PAL.white, "left");
    // GT 行
    txt(ctx, "GT 非零列", 60, 58, 13, PAL.blue);
    gt.forEach((v, i) => {
      const x = 200 + i * 70;
      const inter = wt.includes(v);
      ctx.fillStyle = inter ? "#3a2a1e" : "#1e3c56";
      ctx.strokeStyle = inter ? PAL.orange : PAL.blue; ctx.lineWidth = 2;
      rrect(ctx, x, 46, 58, 30, 6); ctx.fill(); ctx.stroke();
      txt(ctx, v, x + 29, 61, 13, PAL.white, "center");
    });
    // WT 行
    txt(ctx, "WT 非零行", 60, 108, 13, PAL.purple);
    wt.forEach((v, i) => {
      const x = 200 + i * 70;
      const inter = gt.includes(v);
      ctx.fillStyle = inter ? "#3a2a1e" : "#2a2440";
      ctx.strokeStyle = inter ? PAL.orange : PAL.purple; ctx.lineWidth = 2;
      rrect(ctx, x, 96, 58, 30, 6); ctx.fill(); ctx.stroke();
      txt(ctx, v, x + 29, 111, 13, PAL.white, "center");
    });
    txt(ctx, "相交 ID：{0, 4, 7}（橙色）——只有这些位置存在有效 MAC", 60, 160, 13.5, PAL.orange, "left");
    txt(ctx, "不相交 ID 直接跳过（算也是白算）→ 再按操作数平衡分配 WT 行到各子阵列", 60, 190, 12.5, PAL.gray, "left");
    txt(ctx, "Core0: Row{0,10,4,13} ｜ Core1: Row{7,15,9,16} → 每子阵列 MAC 数相同", 60, 220, 13.5, PAL.green, "left");
    txt(ctx, "→ 利用率 17.6%→95.4%（联合 ILA）· EOCI 面积 +1.96%", 60, 252, 12.5, PAL.gray, "left");
    if (stat) stat.textContent = "相交 {0,4,7} → 有效 MAC 识别 → 平衡分配";
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
   演示 C · 利用率对比（ILA-CIM）
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
    txt(ctx, "ILA-CIM：空闲子阵列前瞻未来输入（利用率对比）", 30, 24, 15, PAL.white, "left");
    const k = cyc % 3;
    const util = [17.6, 33.2, 95.4];
    const labels = ["基线（一次一行）", "ILA-CIM（单独）", "EOCI+ILA（联合）"];
    const cols = [PAL.red, PAL.blue, PAL.green];
    // 子阵列图
    for (let r = 0; r < 3; r++) {
      for (let c = 0; c < 4; c++) {
        const x = 70 + c * 90, y = 60 + r * 40;
        const busy = k === 2 ? true : (r === 0 && c === 0) || (k === 1 && (r + c) % 2 === 0);
        ctx.fillStyle = busy ? (k === 2 ? "#1e3c2c" : (k === 1 ? "#1e3c56" : "#3c2a26")) : "#141c2a";
        ctx.strokeStyle = busy ? cols[k] : PAL.line; ctx.lineWidth = busy ? 2 : 1;
        rrect(ctx, x, y, 82, 34, 5); ctx.fill(); ctx.stroke();
      }
    }
    // 利用率条
    const bw = 240 * (util[k] / 100);
    ctx.fillStyle = "#1c2838"; ctx.strokeStyle = cols[k]; ctx.lineWidth = 2;
    rrect(ctx, 450, 70, 240, 30, 8); ctx.fill(); ctx.stroke();
    ctx.fillStyle = cols[k];
    ctx.fillRect(452, 72, bw, 26);
    txt(ctx, util[k] + "%", 570, 85, 14, PAL.white, "center");
    txt(ctx, labels[k], 450, 125, 14, cols[k], "left");
    txt(ctx, k === 2 ? "→ 总加速 5.28× · 子阵列计算时间几乎相同" : "→ 空闲子阵列白等（利用率低）", 450, 155, 12, PAL.gray, "left");
    txt(ctx, "ILA 三步：输入前瞻 → FP 对齐（指数和归一化）→ 输出合并（写回全局缓冲）", 60, 230, 12.5, PAL.white, "left");
    txt(ctx, "附加逻辑面积仅 +2.64%；稀疏归约复用同一数据通路（不加载特征零）", 60, 258, 12, PAL.gray, "left");
    if (stat) stat.textContent = labels[k] + "（利用率 " + util[k] + "%）";
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
