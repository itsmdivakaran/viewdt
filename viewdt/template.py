HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>viewdt</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;line-height:1.4}

:root{
  --bg:#ffffff;--bg2:#f9fafb;--bg3:#f3f4f6;
  --border:#e5e7eb;--text:#111827;--text2:#6b7280;--text3:#9ca3af;
  --accent:#3b82f6;--accent-h:#2563eb;
  --green:#22c55e;--amber:#f59e0b;--red:#ef4444;
  --shadow:0 1px 3px rgba(0,0,0,.1);--shadow-lg:0 4px 24px rgba(0,0,0,.12);
  --row-h:32px;--header-h:80px;--toolbar-h:44px;--status-h:28px;
}
[data-theme=dark]{
  --bg:#111827;--bg2:#1f2937;--bg3:#374151;
  --border:#374151;--text:#f9fafb;--text2:#9ca3af;--text3:#6b7280;
  --shadow:0 1px 3px rgba(0,0,0,.4);--shadow-lg:0 4px 24px rgba(0,0,0,.5);
}

/* ── Layout ── */
#app{display:flex;flex-direction:column;height:100vh;background:var(--bg);color:var(--text)}

/* ── Toolbar ── */
#toolbar{
  height:var(--toolbar-h);display:flex;align-items:center;gap:6px;
  padding:0 12px;border-bottom:1px solid var(--border);
  background:var(--bg2);flex-shrink:0;
}
.brand{font-weight:800;font-size:15px;letter-spacing:-.3px;margin-right:4px;color:var(--accent)}
#search-input{
  flex:1;max-width:300px;padding:5px 10px;
  border:1px solid var(--border);border-radius:6px;
  background:var(--bg);color:var(--text);font-size:13px;outline:none;
  transition:border-color .15s;
}
#search-input:focus{border-color:var(--accent)}
.spacer{flex:1}
.tb-btn{
  padding:5px 10px;border:1px solid var(--border);border-radius:6px;
  background:var(--bg);color:var(--text);font-size:12px;cursor:pointer;
  white-space:nowrap;display:flex;align-items:center;gap:4px;
  transition:background .1s;line-height:1;
}
.tb-btn:hover{background:var(--bg3)}
.tb-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}

/* ── Query Builder ── */
#qb-panel{
  padding:8px 12px;border-bottom:1px solid var(--border);
  background:var(--bg2);flex-shrink:0;display:none;
}
#qb-panel.open{display:block}
.qb-bar{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap}
.qb-row{display:flex;align-items:center;gap:6px;margin-bottom:6px;flex-wrap:wrap}
.qb-select,.qb-input{
  padding:4px 8px;border:1px solid var(--border);border-radius:4px;
  background:var(--bg);color:var(--text);font-size:12px;
}
.qb-remove{
  cursor:pointer;color:var(--text3);padding:0 6px;border:none;
  background:none;font-size:18px;line-height:1;
}
.qb-remove:hover{color:var(--red)}
.logic-toggle{display:flex;border:1px solid var(--border);border-radius:4px;overflow:hidden}
.logic-btn{
  padding:3px 8px;cursor:pointer;font-size:11px;font-weight:600;
  background:var(--bg);border:none;color:var(--text2);
}
.logic-btn.active{background:var(--accent);color:#fff}
.qb-actions{display:flex;gap:6px;margin-top:6px}
.btn-primary{
  padding:5px 12px;border:1px solid var(--accent);border-radius:6px;
  background:var(--accent);color:#fff;font-size:12px;cursor:pointer;
}
.btn-primary:hover{background:var(--accent-h)}
.btn-ghost{
  padding:5px 12px;border:1px solid var(--border);border-radius:6px;
  background:var(--bg);color:var(--text);font-size:12px;cursor:pointer;
}
.btn-ghost:hover{background:var(--bg3)}

/* ── Grid ── */
#grid-wrapper{flex:1;overflow:auto;position:relative}
#grid-inner{min-width:max-content;position:relative}

/* column headers */
#grid-header{
  position:sticky;top:0;z-index:10;
  display:flex;background:var(--bg2);
  border-bottom:2px solid var(--border);
}
.col-header{
  display:flex;flex-direction:column;
  padding:5px 7px 3px;
  border-right:1px solid var(--border);
  cursor:pointer;user-select:none;
  height:var(--header-h);flex-shrink:0;
  transition:background .1s;
}
.col-header:hover{background:var(--bg3)}
.col-header-top{display:flex;align-items:center;gap:4px;margin-bottom:2px}
.type-badge{
  font-size:10px;font-weight:700;padding:1px 4px;border-radius:3px;
  flex-shrink:0;letter-spacing:0;line-height:1.4;
}
.badge-num{background:#dbeafe;color:#1d4ed8}
.badge-str{background:#d1fae5;color:#065f46}
.badge-bool{background:#fef3c7;color:#92400e}
.badge-date{background:#ede9fe;color:#4c1d95}
[data-theme=dark] .badge-num{background:#1e3a5f;color:#93c5fd}
[data-theme=dark] .badge-str{background:#052e16;color:#6ee7b7}
[data-theme=dark] .badge-bool{background:#451a03;color:#fde68a}
[data-theme=dark] .badge-date{background:#2e1065;color:#c4b5fd}
.col-name{font-weight:600;font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;min-width:0}
.col-label-text{font-size:10px;color:var(--text2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-bottom:1px}
.spark-area{flex:1;overflow:hidden;display:flex;align-items:flex-end}
.completeness-bar{height:4px;border-radius:2px;background:var(--border);overflow:hidden;margin-top:3px}
.completeness-fill{height:100%;border-radius:2px;transition:width .3s}
.comp-green{background:var(--green)}
.comp-amber{background:var(--amber)}
.comp-red{background:var(--red)}

/* grid rows */
#vscroll-spacer{position:relative}
.grid-row{
  display:flex;border-bottom:1px solid var(--border);
  position:absolute;left:0;right:0;
}
.grid-row:hover{background:var(--bg2)}
.grid-row.even{background:var(--bg)}
.grid-cell{
  padding:0 8px;height:var(--row-h);display:flex;align-items:center;
  border-right:1px solid var(--border);font-size:12px;
  overflow:hidden;white-space:nowrap;flex-shrink:0;
}
.cell-null{color:var(--text3);font-style:italic}
.cell-num{justify-content:flex-end;font-variant-numeric:tabular-nums;font-size:12px}
.cell-true{color:#16a34a;font-weight:500}
.cell-false{color:#dc2626;font-weight:500}

/* ── Status bar ── */
#status-bar{
  height:var(--status-h);display:flex;align-items:center;
  padding:0 12px;font-size:11px;color:var(--text2);
  border-top:1px solid var(--border);background:var(--bg2);
  flex-shrink:0;gap:10px;
}
.status-dot{color:var(--accent);font-weight:600}

/* ── Insights drawer ── */
#insights-drawer{
  position:fixed;top:0;right:0;bottom:0;width:340px;
  background:var(--bg);border-left:1px solid var(--border);
  box-shadow:var(--shadow-lg);z-index:50;
  display:flex;flex-direction:column;
  transform:translateX(100%);transition:transform .2s ease;
}
#insights-drawer.open{transform:translateX(0)}
.drawer-hdr{
  display:flex;align-items:center;justify-content:space-between;
  padding:12px 16px;border-bottom:1px solid var(--border);
}
.drawer-title{font-weight:700;font-size:14px}
#insights-body{flex:1;overflow-y:auto;padding:14px 16px}
.stat-row{
  display:flex;justify-content:space-between;
  padding:5px 0;font-size:12px;border-bottom:1px solid var(--border);
}
.stat-label{color:var(--text2)}
.stat-val{font-variant-numeric:tabular-nums;font-weight:500}
.section-title{
  font-size:11px;font-weight:700;color:var(--text2);
  letter-spacing:.5px;text-transform:uppercase;
  margin:12px 0 6px;
}
.cat-bar-row{margin-bottom:5px}
.cat-bar-meta{display:flex;justify-content:space-between;font-size:11px;margin-bottom:2px}
.cat-bar-label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}
.cat-bar-count{color:var(--text2);margin-left:8px;flex-shrink:0}
.cat-bar-track{height:6px;background:var(--border);border-radius:3px;overflow:hidden}
.cat-bar-fill{height:100%;border-radius:3px}

/* ── Code modal ── */
#code-overlay{
  position:fixed;inset:0;background:rgba(0,0,0,.5);
  z-index:100;display:none;align-items:center;justify-content:center;
}
#code-overlay.open{display:flex}
#code-modal{
  background:var(--bg);border-radius:10px;width:620px;
  max-width:92vw;max-height:80vh;display:flex;flex-direction:column;
  box-shadow:var(--shadow-lg);
}
.modal-hdr{
  padding:14px 18px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  font-weight:700;font-size:15px;
}
.modal-tabs{display:flex;border-bottom:1px solid var(--border);padding:0 14px}
.modal-tab{
  padding:8px 14px;cursor:pointer;font-size:12px;font-weight:600;
  border-bottom:2px solid transparent;color:var(--text2);margin-bottom:-1px;
}
.modal-tab.active{border-bottom-color:var(--accent);color:var(--text)}
.modal-body{flex:1;padding:14px;overflow:auto}
.code-block{
  background:var(--bg2);border:1px solid var(--border);border-radius:6px;
  padding:14px;font-family:'Cascadia Code','Fira Code','Courier New',monospace;
  font-size:12px;white-space:pre;overflow:auto;color:var(--text);
  min-height:120px;
}
.modal-footer{
  padding:12px 18px;border-top:1px solid var(--border);
  display:flex;justify-content:flex-end;gap:8px;
}

/* ── Column picker ── */
#col-picker-overlay{position:fixed;inset:0;z-index:40;display:none}
#col-picker-overlay.open{display:block}
#col-picker-dropdown{
  position:fixed;background:var(--bg);border:1px solid var(--border);
  border-radius:8px;box-shadow:var(--shadow-lg);z-index:41;
  min-width:210px;max-height:320px;overflow-y:auto;padding:4px 0;
}
.picker-item{
  display:flex;align-items:center;gap:8px;padding:6px 12px;
  cursor:pointer;font-size:12px;
}
.picker-item:hover{background:var(--bg2)}
.picker-sep{height:1px;background:var(--border);margin:4px 0}

/* ── Misc ── */
.close-btn{
  cursor:pointer;background:none;border:none;color:var(--text2);
  font-size:20px;line-height:1;padding:2px 6px;border-radius:4px;
}
.close-btn:hover{background:var(--bg3)}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg2)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--text3)}
</style>
</head>
<body>
<div id="app">
  <!-- Toolbar -->
  <div id="toolbar">
    <span class="brand">viewdt</span>
    <input id="search-input" type="text" placeholder="Search all columns…" autocomplete="off" style="display:none">
    <div class="spacer"></div>
    <button class="tb-btn" id="tb-filter" onclick="toggleQB()" style="display:none">⊞ Filter</button>
    <button class="tb-btn" id="tb-cols" onclick="togglePicker(event)" style="display:none">☰ Columns</button>
    <button class="tb-btn" id="tb-code" onclick="openCode()" style="display:none">⟨/⟩ Code</button>
    <button class="tb-btn" id="tb-theme" onclick="cycleTheme()">◑</button>
  </div>

  <!-- Query Builder -->
  <div id="qb-panel"></div>

  <!-- Grid -->
  <div id="grid-wrapper">
    <div id="grid-inner">
      <div id="grid-header"></div>
      <div id="vscroll-spacer"></div>
    </div>
  </div>

  <!-- Status bar -->
  <div id="status-bar"></div>
</div>

<!-- Insights Drawer -->
<div id="insights-drawer">
  <div class="drawer-hdr">
    <span class="drawer-title" id="insights-title">Column Insights</span>
    <button class="close-btn" onclick="closeInsights()">×</button>
  </div>
  <div id="insights-body"></div>
</div>

<!-- Code Modal -->
<div id="code-overlay" onclick="handleOverlayClick(event)">
  <div id="code-modal">
    <div class="modal-hdr">
      <span>Reproducible Code</span>
      <button class="close-btn" onclick="closeCode()">×</button>
    </div>
    <div class="modal-tabs" id="code-tabs"></div>
    <div class="modal-body"><pre id="code-content" class="code-block"></pre></div>
    <div class="modal-footer">
      <button class="btn-ghost" onclick="closeCode()">Close</button>
      <button class="btn-primary" id="copy-btn" onclick="copyCode()">Copy</button>
    </div>
  </div>
</div>

<!-- Column Picker -->
<div id="col-picker-overlay" onclick="closePicker()">
  <div id="col-picker-dropdown" onclick="event.stopPropagation()"></div>
</div>

<script>
// ════════════════════════════════════════════════════
//  DATA  (injected by Python)
// ════════════════════════════════════════════════════
const VIEWDT_DATA = <<<DATA>>>;

const D    = VIEWDT_DATA;
const cols = D.columns;
const rows = D.rows;
const opts = D.options;
const N    = rows.length;

// index maps
const colIndex = {};   // name -> row-array index
const colMap   = {};   // name -> profile object
cols.forEach((c, i) => { colIndex[c.name] = i; colMap[c.name] = c; });

// ════════════════════════════════════════════════════
//  STATE
// ════════════════════════════════════════════════════
const state = {
  hiddenCols:  new Set(opts.hidden_columns || []),
  filters:     [],
  filterLogic: 'AND',
  searchQuery: '',
  displayed:   [],
  insightCol:  null,
  qbOpen:      false,
  pickerOpen:  false,
  codeOpen:    false,
  codeTab:     'pandas',
};

const ROW_H = 32;
const COL_W = 150;

// ════════════════════════════════════════════════════
//  THEME
// ════════════════════════════════════════════════════
const THEMES = ['auto', 'light', 'dark'];
let themeIdx = THEMES.indexOf(opts.theme);
if (themeIdx < 0) themeIdx = 0;

function applyTheme(t) {
  const dark = t === 'dark' || (t === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
}

function cycleTheme() {
  themeIdx = (themeIdx + 1) % 3;
  applyTheme(THEMES[themeIdx]);
  const icons = ['◑', '☀', '☾'];
  document.getElementById('tb-theme').textContent = icons[themeIdx];
}

// ════════════════════════════════════════════════════
//  COLUMN HELPERS
// ════════════════════════════════════════════════════
function visibleCols() {
  return cols.filter(c => !state.hiddenCols.has(c.name));
}

function totalWidth() {
  return visibleCols().length * COL_W;
}

// ════════════════════════════════════════════════════
//  FILTER ENGINE
// ════════════════════════════════════════════════════
function computeDisplayed() {
  const vcols = visibleCols();
  const result = [];
  const q = state.searchQuery.toLowerCase();

  for (let i = 0; i < N; i++) {
    const row = rows[i];

    if (q) {
      let hit = false;
      for (const c of vcols) {
        const v = row[colIndex[c.name]];
        if (v !== null && v !== undefined && String(v).toLowerCase().includes(q)) { hit = true; break; }
      }
      if (!hit) continue;
    }

    if (state.filters.length > 0) {
      const results = state.filters.map(f => evalFilter(row, f));
      if (state.filterLogic === 'AND' && !results.every(Boolean)) continue;
      if (state.filterLogic === 'OR'  && !results.some(Boolean))  continue;
    }

    result.push(i);
  }

  state.displayed = result;
  updateStatus();
  scheduleRender();
}

function evalFilter(row, f) {
  const val  = row[colIndex[f.col]];
  const meta = colMap[f.col];

  if (f.op === 'is null')  return val === null || val === undefined;
  if (f.op === 'not null') return val !== null && val !== undefined;
  if (val === null || val === undefined) return false;

  if (meta.kind === 'numeric') {
    const n  = Number(val);
    const fv = Number(f.val);
    switch (f.op) {
      case '=':  return n === fv;
      case '≠':  return n !== fv;
      case '<':  return n <  fv;
      case '≤':  return n <= fv;
      case '>':  return n >  fv;
      case '≥':  return n >= fv;
    }
  }

  if (meta.kind === 'character') {
    const s   = String(val).toLowerCase();
    const fv  = String(f.val || '').toLowerCase();
    const fvs = (f.vals || []).map(v => v.toLowerCase());
    switch (f.op) {
      case '=':        return s === fv;
      case '≠':        return s !== fv;
      case 'contains': return s.includes(fv);
      case '!contains':return !s.includes(fv);
      case 'in':       return fvs.includes(s);
      case '!in':      return !fvs.includes(s);
    }
  }

  if (meta.kind === 'logical') {
    const b = val === true || val === 'true' || val === 1;
    if (f.op === 'is true')  return b;
    if (f.op === 'is false') return !b;
  }

  if (meta.kind === 'datetime') {
    const d  = new Date(val);
    const fd = new Date(f.val);
    switch (f.op) {
      case '=':  return d.toDateString() === fd.toDateString();
      case '<':  return d <  fd;
      case '≤':  return d <= fd;
      case '>':  return d >  fd;
      case '≥':  return d >= fd;
    }
  }

  return true;
}

function opsFor(kind) {
  switch (kind) {
    case 'numeric':  return ['=','≠','<','≤','>','≥','is null','not null'];
    case 'character':return ['=','≠','contains','!contains','in','!in','is null','not null'];
    case 'logical':  return ['is true','is false','is null','not null'];
    case 'datetime': return ['=','<','≤','>','≥','is null','not null'];
    default:         return ['=','≠','contains','is null','not null'];
  }
}

// ════════════════════════════════════════════════════
//  CELL FORMATTING
// ════════════════════════════════════════════════════
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function fmtNum(n) {
  if (Number.isInteger(n)) return n.toLocaleString();
  const a = Math.abs(n);
  if (a >= 1e6 || (a < 0.001 && a > 0)) return n.toExponential(3);
  return parseFloat(n.toPrecision(5)).toString();
}

function formatCell(val, col) {
  if (val === null || val === undefined) return `<span class="cell-null">${esc(opts.na_string)}</span>`;

  if (col.kind === 'numeric') {
    const n = Number(val);
    return isNaN(n)
      ? `<span class="cell-null">${esc(opts.na_string)}</span>`
      : fmtNum(n);
  }

  if (col.kind === 'logical') {
    const b = val === true || val === 'true' || val === 1;
    return b ? '<span class="cell-true">TRUE</span>' : '<span class="cell-false">FALSE</span>';
  }

  return esc(String(val));
}

// ════════════════════════════════════════════════════
//  SPARK CHARTS (SVG)
// ════════════════════════════════════════════════════
function sparkHistSVG(counts, w, h) {
  if (!counts || !counts.length) return '';
  const max = Math.max(...counts, 1);
  const bw  = w / counts.length;
  let r = '';
  for (let i = 0; i < counts.length; i++) {
    const bh = Math.max(1, (counts[i] / max) * h);
    r += `<rect x="${(i*bw).toFixed(1)}" y="${(h-bh).toFixed(1)}" width="${Math.max(1,bw-.5).toFixed(1)}" height="${bh.toFixed(1)}" fill="var(--accent)" opacity=".75"/>`;
  }
  return `<svg width="${w}" height="${h}" style="display:block">${r}</svg>`;
}

const CAT_COLORS = ['#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6','#ec4899','#06b6d4','#84cc16','#f97316','#14b8a6'];

function sparkCatSVG(topValues, w, h) {
  if (!topValues || !topValues.length) return '';
  const n = topValues.length;
  const max = Math.max(...topValues.map(v => v.count), 1);
  const bh  = Math.max(2, Math.floor((h - n) / n));
  let r = '', y = 0;
  topValues.forEach((v, i) => {
    const bw = Math.max(1, (v.count / max) * w);
    r += `<rect x="0" y="${y}" width="${bw.toFixed(1)}" height="${bh}" fill="${CAT_COLORS[i % CAT_COLORS.length]}" rx="1"/>`;
    y += bh + 1;
  });
  return `<svg width="${w}" height="${h}" style="display:block">${r}</svg>`;
}

function sparkBoolSVG(nTrue, nFalse, w, h) {
  const tot  = (nTrue + nFalse) || 1;
  const wt   = (nTrue / tot) * w;
  return `<svg width="${w}" height="${h}" style="display:block">
    <rect x="0" y="0" width="${wt.toFixed(1)}" height="${h}" fill="#22c55e" rx="2"/>
    <rect x="${wt.toFixed(1)}" y="0" width="${(w-wt).toFixed(1)}" height="${h}" fill="#ef4444" rx="2"/>
  </svg>`;
}

function bigHistSVG(counts, w, h) {
  if (!counts || !counts.length) return '';
  const max = Math.max(...counts, 1);
  const bw  = w / counts.length;
  let r = '';
  for (let i = 0; i < counts.length; i++) {
    const bh = Math.max(1, (counts[i] / max) * h);
    r += `<rect x="${(i*bw+.5).toFixed(1)}" y="${(h-bh).toFixed(1)}" width="${Math.max(1,bw-1).toFixed(1)}" height="${bh.toFixed(1)}" fill="var(--accent)" opacity=".85" rx="1"/>`;
  }
  return `<svg width="${w}" height="${h}" style="display:block;border:1px solid var(--border);border-radius:6px">${r}</svg>`;
}

// ════════════════════════════════════════════════════
//  COLUMN HEADERS
// ════════════════════════════════════════════════════
function buildHeaders() {
  const hdr   = document.getElementById('grid-header');
  hdr.innerHTML = '';
  const vcols  = visibleCols();
  const sw     = COL_W - 14;
  const sh     = 28;

  vcols.forEach(col => {
    const el  = document.createElement('div');
    el.className = 'col-header';
    el.style.width = COL_W + 'px';
    el.dataset.col = col.name;

    const bk = {numeric:'badge-num',character:'badge-str',logical:'badge-bool',datetime:'badge-date',date:'badge-date'}[col.kind] || 'badge-str';
    const bt = {numeric:'#',character:'A',logical:'T/F',datetime:'⏱',date:'📅'}[col.kind] || '?';

    let spark = '';
    if (opts.histograms) {
      if (col.kind === 'numeric' || col.kind === 'datetime') spark = sparkHistSVG(col.hist_counts, sw, sh);
      else if (col.kind === 'character') spark = sparkCatSVG(col.top_values, sw, sh);
      else if (col.kind === 'logical')   spark = sparkBoolSVG(col.n_true||0, col.n_false||0, sw, sh);
    }

    const comp     = col.completeness * 100;
    const compCls  = comp >= 95 ? 'comp-green' : comp >= 50 ? 'comp-amber' : 'comp-red';
    const badgeHtml = opts.type_badges ? `<span class="type-badge ${bk}">${bt}</span>` : '';
    const labelHtml = opts.show_labels && col.label ? `<div class="col-label-text">${esc(col.label)}</div>` : '';
    const sparkHtml = opts.histograms ? `<div class="spark-area">${spark}</div>` : '';
    const compHtml  = opts.missing_bars
      ? `<div class="completeness-bar" title="${comp.toFixed(1)}% complete">
           <div class="completeness-fill ${compCls}" style="width:${comp.toFixed(1)}%"></div>
         </div>` : '';

    el.innerHTML = `
      <div class="col-header-top">${badgeHtml}<span class="col-name" title="${esc(col.name)}">${esc(col.name)}</span></div>
      ${labelHtml}${sparkHtml}${compHtml}`;

    if (opts.insights) el.addEventListener('click', () => openInsights(col.name));
    hdr.appendChild(el);
  });

  document.getElementById('vscroll-spacer').style.minWidth = totalWidth() + 'px';
}

// ════════════════════════════════════════════════════
//  VIRTUAL SCROLL
// ════════════════════════════════════════════════════
let _rafPending = false;

function scheduleRender() {
  if (!_rafPending) { _rafPending = true; requestAnimationFrame(() => { _rafPending = false; renderRows(); }); }
}

function renderRows() {
  const wrapper  = document.getElementById('grid-wrapper');
  const spacer   = document.getElementById('vscroll-spacer');
  const displayed = state.displayed;
  const totalH   = displayed.length * ROW_H;
  spacer.style.height   = totalH + 'px';
  spacer.style.minWidth = totalWidth() + 'px';

  const scrollTop = wrapper.scrollTop;
  const viewH     = wrapper.clientHeight || window.innerHeight;
  const buf       = 12;
  const start     = Math.max(0, Math.floor(scrollTop / ROW_H) - buf);
  const end       = Math.min(displayed.length, Math.ceil((scrollTop + viewH) / ROW_H) + buf);

  const vcols = visibleCols();
  let html = '';

  for (let i = start; i < end; i++) {
    const ri  = displayed[i];
    const row = rows[ri];
    const top = i * ROW_H;
    let cells = '';
    for (const col of vcols) {
      const val = row[colIndex[col.name]];
      cells += `<div class="grid-cell${col.kind==='numeric'?' cell-num':''}" style="width:${COL_W}px">${formatCell(val, col)}</div>`;
    }
    html += `<div class="grid-row" style="top:${top}px;height:${ROW_H}px">${cells}</div>`;
  }

  spacer.innerHTML = html;
}

function initScroll() {
  const w = document.getElementById('grid-wrapper');
  w.addEventListener('scroll', scheduleRender);
  window.addEventListener('resize', scheduleRender);
}

// ════════════════════════════════════════════════════
//  STATUS BAR
// ════════════════════════════════════════════════════
function updateStatus() {
  const bar    = document.getElementById('status-bar');
  const vcols  = visibleCols();
  const nFilt  = state.displayed.length;
  const active = nFilt < N || state.searchQuery || state.filters.length;
  bar.innerHTML =
    `<span>${nFilt.toLocaleString()} of ${N.toLocaleString()} rows</span>
     <span>•</span>
     <span>${vcols.length} of ${cols.length} columns</span>
     ${active ? '<span class="status-dot">• filtered</span>' : ''}`;
}

// ════════════════════════════════════════════════════
//  TOOLBAR
// ════════════════════════════════════════════════════
function buildToolbar() {
  if (opts.global_search) {
    const si = document.getElementById('search-input');
    si.style.display = '';
    si.addEventListener('input', e => { state.searchQuery = e.target.value; computeDisplayed(); });
  }
  if (opts.query_builder)  document.getElementById('tb-filter').style.display = '';
  if (opts.column_picker)  document.getElementById('tb-cols').style.display   = '';
  if (opts.code_export)    document.getElementById('tb-code').style.display   = '';

  applyTheme(THEMES[themeIdx]);
  const icons = ['◑','☀','☾'];
  document.getElementById('tb-theme').textContent = icons[themeIdx];
}

// ════════════════════════════════════════════════════
//  QUERY BUILDER
// ════════════════════════════════════════════════════
function toggleQB() {
  state.qbOpen = !state.qbOpen;
  document.getElementById('qb-panel').classList.toggle('open', state.qbOpen);
  document.getElementById('tb-filter').classList.toggle('active', state.qbOpen);
}

function addCondition() {
  const c = cols[0];
  state.filters.push({ col: c.name, op: opsFor(c.kind)[0], val: '', vals: [] });
  renderQB();
}

function removeCondition(idx) {
  state.filters.splice(idx, 1);
  renderQB();
  computeDisplayed();
}

function updateCondCol(idx, name) {
  const meta = colMap[name];
  state.filters[idx] = { col: name, op: opsFor(meta.kind)[0], val: '', vals: [] };
  renderQB();
}

function updateCondOp(idx, op) {
  state.filters[idx].op = op;
  renderQB();
}

function setLogic(l) {
  state.filterLogic = l;
  document.querySelectorAll('.logic-btn').forEach(b => b.classList.toggle('active', b.dataset.logic === l));
}

function renderQB() {
  const panel = document.getElementById('qb-panel');
  let html = `<div class="qb-bar">
    <strong style="font-size:12px">Filters</strong>
    <div class="logic-toggle">
      <button class="logic-btn${state.filterLogic==='AND'?' active':''}" data-logic="AND" onclick="setLogic('AND')">AND</button>
      <button class="logic-btn${state.filterLogic==='OR'?' active':''}" data-logic="OR" onclick="setLogic('OR')">OR</button>
    </div>
    <button class="btn-ghost" onclick="addCondition()" style="font-size:11px;padding:3px 8px">+ Condition</button>
  </div>`;

  state.filters.forEach((f, i) => {
    const meta     = colMap[f.col];
    const ops      = opsFor(meta.kind);
    const noVal    = ['is null','not null','is true','is false'].includes(f.op);
    const isInOp   = f.op === 'in' || f.op === '!in';
    const inpType  = meta.kind === 'numeric' ? 'number' : meta.kind === 'datetime' ? 'date' : 'text';

    html += `<div class="qb-row">
      <select class="qb-select" onchange="updateCondCol(${i},this.value)">
        ${cols.map(c=>`<option value="${esc(c.name)}"${c.name===f.col?' selected':''}>${esc(c.name)}</option>`).join('')}
      </select>
      <select class="qb-select" onchange="updateCondOp(${i},this.value)">
        ${ops.map(op=>`<option value="${op}"${op===f.op?' selected':''}>${op}</option>`).join('')}
      </select>
      ${noVal ? '' : isInOp
        ? `<input class="qb-input" style="min-width:160px" placeholder="val1, val2…" value="${esc((f.vals||[]).join(', '))}" onchange="state.filters[${i}].vals=this.value.split(',').map(v=>v.trim()).filter(Boolean)">`
        : `<input class="qb-input" type="${inpType}" value="${esc(f.val||'')}" oninput="state.filters[${i}].val=this.value">`}
      <button class="qb-remove" onclick="removeCondition(${i})">×</button>
    </div>`;
  });

  if (state.filters.length) {
    html += `<div class="qb-actions">
      <button class="btn-primary" onclick="computeDisplayed()">Apply</button>
      <button class="btn-ghost" onclick="resetFilters()">Reset</button>
    </div>`;
  }

  panel.innerHTML = html;
}

function resetFilters() {
  state.filters = [];
  state.searchQuery = '';
  const si = document.getElementById('search-input');
  if (si) si.value = '';
  renderQB();
  computeDisplayed();
}

// ════════════════════════════════════════════════════
//  DATA INSIGHTS DRAWER
// ════════════════════════════════════════════════════
function openInsights(name) {
  state.insightCol = name;
  document.getElementById('insights-drawer').classList.add('open');
  renderInsights();
}

function closeInsights() {
  document.getElementById('insights-drawer').classList.remove('open');
}

function renderInsights() {
  const col  = colMap[state.insightCol];
  if (!col) return;
  document.getElementById('insights-title').textContent = col.name;
  const body = document.getElementById('insights-body');
  const nv   = col.n_total - col.n_missing;

  let h = '';
  h += statRow('Type', {numeric:'Numeric',character:'Text',logical:'Logical',datetime:'Date/Time'}[col.kind] || col.kind);
  h += statRow('Total rows', col.n_total.toLocaleString());
  h += statRow('Missing', `${col.n_missing.toLocaleString()} (${(col.n_missing/col.n_total*100).toFixed(1)}%)`);
  h += statRow('Complete', `${nv.toLocaleString()} (${(col.completeness*100).toFixed(1)}%)`);

  if (col.kind === 'numeric') {
    if (col.min !== null) {
      h += statRow('Min',    fmtNum(col.min));
      h += statRow('Max',    fmtNum(col.max));
      h += statRow('Mean',   fmtNum(col.mean));
      h += statRow('Median', fmtNum(col.median));
      h += statRow('Std Dev',fmtNum(col.std));
    }
    if (col.hist_counts && col.hist_counts.length) {
      h += `<div class="section-title">Distribution</div><div>${bigHistSVG(col.hist_counts, 292, 110)}</div>`;
    }
  } else if (col.kind === 'character') {
    h += statRow('Unique values', (col.n_unique || 0).toLocaleString());
    if (col.top_values && col.top_values.length) {
      h += `<div class="section-title">Top values</div>`;
      const maxC = Math.max(...col.top_values.map(v => v.count), 1);
      col.top_values.forEach((v, i) => {
        const pct  = (v.count / col.n_total * 100).toFixed(1);
        const barW = (v.count / maxC * 100).toFixed(1);
        h += `<div class="cat-bar-row">
          <div class="cat-bar-meta">
            <span class="cat-bar-label">${esc(v.value)}</span>
            <span class="cat-bar-count">${v.count.toLocaleString()} (${pct}%)</span>
          </div>
          <div class="cat-bar-track">
            <div class="cat-bar-fill" style="width:${barW}%;background:${CAT_COLORS[i%CAT_COLORS.length]}"></div>
          </div>
        </div>`;
      });
    }
  } else if (col.kind === 'logical') {
    const nt = col.n_true || 0, nf = col.n_false || 0;
    h += statRow('TRUE',  nt.toLocaleString());
    h += statRow('FALSE', nf.toLocaleString());
    h += `<div style="margin-top:10px">${sparkBoolSVG(nt, nf, 292, 20)}</div>`;
  } else if (col.kind === 'datetime') {
    if (col.min) {
      h += statRow('Earliest', col.min);
      h += statRow('Latest',   col.max);
    }
    if (col.hist_counts && col.hist_counts.length) {
      h += `<div class="section-title">Distribution</div><div>${bigHistSVG(col.hist_counts, 292, 110)}</div>`;
    }
  }

  body.innerHTML = h;
}

function statRow(label, val) {
  return `<div class="stat-row"><span class="stat-label">${label}</span><span class="stat-val">${val}</span></div>`;
}

// ════════════════════════════════════════════════════
//  COLUMN PICKER
// ════════════════════════════════════════════════════
function togglePicker(event) {
  state.pickerOpen = !state.pickerOpen;
  const overlay = document.getElementById('col-picker-overlay');
  overlay.classList.toggle('open', state.pickerOpen);

  if (state.pickerOpen) {
    const btn  = event.currentTarget;
    const rect = btn.getBoundingClientRect();
    const dd   = document.getElementById('col-picker-dropdown');
    dd.style.top   = (rect.bottom + 4) + 'px';
    dd.style.right = (window.innerWidth - rect.right) + 'px';
    renderPicker();
  }
}

function closePicker() {
  state.pickerOpen = false;
  document.getElementById('col-picker-overlay').classList.remove('open');
}

function toggleColVis(name) {
  if (state.hiddenCols.has(name)) state.hiddenCols.delete(name);
  else state.hiddenCols.add(name);
  buildHeaders();
  scheduleRender();
  updateStatus();
  renderPicker();
}

function toggleAllCols() {
  if (state.hiddenCols.size === 0) cols.forEach(c => state.hiddenCols.add(c.name));
  else state.hiddenCols.clear();
  buildHeaders();
  scheduleRender();
  updateStatus();
  renderPicker();
}

function renderPicker() {
  const dd   = document.getElementById('col-picker-dropdown');
  const all  = state.hiddenCols.size === 0;
  const none = state.hiddenCols.size === cols.length;
  const indet = !all && !none;

  let h = `<div class="picker-item" onclick="toggleAllCols()">
    <input type="checkbox" ${all?'checked':''} style="pointer-events:none" id="_picker_all">
    <strong>All columns</strong>
  </div><div class="picker-sep"></div>`;

  cols.forEach(col => {
    const vis  = !state.hiddenCols.has(col.name);
    const bk   = {numeric:'badge-num',character:'badge-str',logical:'badge-bool',datetime:'badge-date'}[col.kind]||'badge-str';
    const bt   = {numeric:'#',character:'A',logical:'T/F',datetime:'⏱'}[col.kind]||'?';
    h += `<div class="picker-item" onclick="toggleColVis('${esc(col.name).replace(/'/g,"\\'")}')">
      <input type="checkbox" ${vis?'checked':''} style="pointer-events:none">
      <span class="type-badge ${bk}" style="font-size:9px;padding:1px 3px">${bt}</span>
      <span>${esc(col.name)}</span>
    </div>`;
  });

  dd.innerHTML = h;
  const allCb = dd.querySelector('#_picker_all');
  if (allCb) allCb.indeterminate = indet;
}

// ════════════════════════════════════════════════════
//  CODE EXPORT
// ════════════════════════════════════════════════════
function openCode() {
  state.codeOpen = true;
  document.getElementById('code-overlay').classList.add('open');
  renderCodeModal();
}

function closeCode() {
  document.getElementById('code-overlay').classList.remove('open');
}

function handleOverlayClick(e) {
  if (e.target.id === 'code-overlay') closeCode();
}

function setCodeTab(tab) {
  state.codeTab = tab;
  document.querySelectorAll('.modal-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.getElementById('code-content').textContent = genCode(tab);
}

function renderCodeModal() {
  const tabs = ['pandas','python','sql'];
  document.getElementById('code-tabs').innerHTML =
    tabs.map(t => `<div class="modal-tab${state.codeTab===t?' active':''}" data-tab="${t}" onclick="setCodeTab('${t}')">${t}</div>`).join('');
  document.getElementById('code-content').textContent = genCode(state.codeTab);
}

function genCode(tab) {
  if (tab === 'pandas') return genPandas();
  if (tab === 'python') return genPython();
  return genSQL();
}

function buildConds(lang) {
  const ds   = D.dataset_name;
  const conds = [];

  if (state.searchQuery && lang !== 'sql') {
    const q    = state.searchQuery.replace(/'/g, "\\'");
    const parts = visibleCols().map(c =>
      lang === 'pandas'
        ? `${ds}['${c.name}'].astype(str).str.contains('${q}', case=False, na=False)`
        : `${ds}['${c.name}'].astype(str).str.contains('${q}', case=False, na=False)`
    );
    if (parts.length) conds.push(`(${parts.join(' | ')})`);
  }

  state.filters.forEach(f => {
    const meta  = colMap[f.col];
    const isStr = meta.kind === 'character';
    let c = '';

    if (lang === 'pandas' || lang === 'python') {
      const col = `${ds}['${f.col}']`;
      const sv  = isStr ? `'${f.val}'` : f.val;
      switch (f.op) {
        case '=':        c = `(${col} == ${sv})`; break;
        case '≠':        c = `(${col} != ${sv})`; break;
        case '<':        c = `(${col} < ${f.val})`; break;
        case '≤':        c = `(${col} <= ${f.val})`; break;
        case '>':        c = `(${col} > ${f.val})`; break;
        case '≥':        c = `(${col} >= ${f.val})`; break;
        case 'contains': c = `(${col}.str.contains('${f.val}', case=False, na=False))`; break;
        case '!contains':c = `(~${col}.str.contains('${f.val}', case=False, na=False))`; break;
        case 'in':       c = `(${col}.isin([${(f.vals||[]).map(v=>`'${v}'`).join(',')}]))`; break;
        case '!in':      c = `(~${col}.isin([${(f.vals||[]).map(v=>`'${v}'`).join(',')}]))`; break;
        case 'is null':  c = `(${col}.isna())`; break;
        case 'not null': c = `(${col}.notna())`; break;
        case 'is true':  c = `(${col} == True)`; break;
        case 'is false': c = `(${col} == False)`; break;
      }
    } else {
      const col = `"${f.col}"`;
      const sv  = isStr ? `'${f.val}'` : f.val;
      switch (f.op) {
        case '=':        c = `${col} = ${sv}`; break;
        case '≠':        c = `${col} <> ${sv}`; break;
        case '<':        c = `${col} < ${f.val}`; break;
        case '≤':        c = `${col} <= ${f.val}`; break;
        case '>':        c = `${col} > ${f.val}`; break;
        case '≥':        c = `${col} >= ${f.val}`; break;
        case 'contains': c = `${col} LIKE '%${f.val}%'`; break;
        case '!contains':c = `${col} NOT LIKE '%${f.val}%'`; break;
        case 'in':       c = `${col} IN (${(f.vals||[]).map(v=>`'${v}'`).join(',')})`; break;
        case '!in':      c = `${col} NOT IN (${(f.vals||[]).map(v=>`'${v}'`).join(',')})`; break;
        case 'is null':  c = `${col} IS NULL`; break;
        case 'not null': c = `${col} IS NOT NULL`; break;
        case 'is true':  c = `${col} = TRUE`; break;
        case 'is false': c = `${col} = FALSE`; break;
      }
    }
    if (c) conds.push(c);
  });

  return conds;
}

function genPandas() {
  const ds     = D.dataset_name;
  const vcols  = visibleCols().map(c => c.name);
  const allVis = vcols.length === cols.length;
  const conds  = buildConds('pandas');
  const op     = state.filterLogic === 'AND' ? ' &\n    ' : ' |\n    ';
  const lines  = [];

  if (conds.length) {
    lines.push(`mask = (\n    ${conds.join(op)}\n)`);
    lines.push(`df = ${ds}[mask]`);
  } else {
    lines.push(`df = ${ds}.copy()`);
  }
  if (!allVis) lines.push(`df = df[${JSON.stringify(vcols)}]`);
  return lines.join('\n');
}

function genPython() {
  const ds     = D.dataset_name;
  const vcols  = visibleCols().map(c => c.name);
  const allVis = vcols.length === cols.length;
  const conds  = buildConds('python');
  const op     = state.filterLogic === 'AND' ? ' &\n    ' : ' |\n    ';
  const lines  = ['import pandas as pd', ''];

  if (conds.length) lines.push(`result = ${ds}[\n    ${conds.join(op)}\n]`);
  else lines.push(`result = ${ds}.copy()`);
  if (!allVis) lines.push(`result = result[${JSON.stringify(vcols)}]`);
  return lines.join('\n');
}

function genSQL() {
  const ds     = D.dataset_name;
  const vcols  = visibleCols().map(c => c.name);
  const allVis = vcols.length === cols.length;
  const sel    = allVis ? '*' : vcols.map(c => `"${c}"`).join(', ');
  const conds  = buildConds('sql');
  const op     = state.filterLogic === 'AND' ? '\n  AND ' : '\n  OR ';

  let sql = `SELECT ${sel}\nFROM "${ds}"`;
  if (conds.length) sql += `\nWHERE ${conds.join(op)}`;
  return sql + ';';
}

function copyCode() {
  const code = document.getElementById('code-content').textContent;
  navigator.clipboard.writeText(code).then(() => {
    const btn = document.getElementById('copy-btn');
    btn.textContent = '✓ Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  }).catch(() => {
    const ta = document.createElement('textarea');
    ta.value = code;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  });
}

// ════════════════════════════════════════════════════
//  INIT
// ════════════════════════════════════════════════════
(function init() {
  buildToolbar();
  renderQB();
  computeDisplayed();
  buildHeaders();
  initScroll();
  scheduleRender();
  updateStatus();
})();
</script>
</body>
</html>"""
