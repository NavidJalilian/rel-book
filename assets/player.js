/* Shared player for every chapter explainer.
   A chapter page provides: <script type="application/json" id="meta">…</script> and <div class="stage" id="stage"> with <section class="scene"> children.
   Scene attributes: data-t (seconds), data-sec (index into meta.sections), data-title (Persian scene name). */
(() => {
  const meta = JSON.parse(document.getElementById('meta').textContent);
  const stage = document.getElementById('stage');
  const scenes = [...stage.querySelectorAll(':scope > .scene')];
  const SECS = meta.sections;
  const fa = s => String(s).replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
  const el = (tag, attrs = {}, html = '') => { const e = document.createElement(tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (html) e.innerHTML = html; return e; };

  // ---- chrome ----
  const app = el('div', { class: 'app', dir: 'rtl', lang: 'fa' });
  const top = el('header', { class: 'top' });
  const home = el('a', { class: 'home', href: meta.home || '../../index.html', 'aria-label': 'بازگشت به کتابخانه', title: 'کتابخانه' },
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4z"/><path d="M20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/></svg>');
  const bk = el('div', { class: 'bk' }); const bkB = el('b'); bkB.textContent = meta.book; const bkS = el('span'); bkS.textContent = meta.author + ' · ' + meta.chapter; bk.append(bkB, bkS);
  const now = el('div', { class: 'now', id: 'now' });
  const menuBtn = el('button', { class: 'menuBtn', type: 'button', 'aria-expanded': 'false', 'aria-controls': 'menu' }); menuBtn.textContent = 'فهرست بخش‌ها';
  const menu = el('div', { class: 'menu', id: 'menu' }); menu.hidden = true; const list = el('ol'); menu.appendChild(list);
  top.append(home, bk, now, menuBtn, menu);
  const wrap = el('div', { class: 'wrap' });
  const ctrl = el('div', { class: 'ctrl' });
  const chev = d => `<svg viewBox="0 0 24 24"><path d="${d}" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const prev = el('button', { class: 'ib', type: 'button', 'aria-label': 'صحنه‌ی قبل' }, chev('M9 5l7 7-7 7'));
  const playBtn = el('button', { class: 'ib play', type: 'button', 'aria-label': 'توقف' }, '<svg viewBox="0 0 24 24"></svg>');
  const next = el('button', { class: 'ib', type: 'button', 'aria-label': 'صحنه‌ی بعد' }, chev('M15 5l-7 7 7 7'));
  const segBox = el('div', { class: 'segs' });
  const time = el('div', { class: 'time' });
  ctrl.append(prev, playBtn, next, segBox, time);
  app.append(top, wrap, ctrl);
  document.body.prepend(app);
  wrap.appendChild(stage);
  stage.setAttribute('role', 'region');
  stage.setAttribute('aria-label', 'پخش‌کننده‌ی ویدئوی آموزشی ' + meta.chapter);

  // end-of-chapter buttons
  const last = scenes[scenes.length - 1];
  let endbar = last.querySelector('.endbar');
  if (!endbar) { endbar = el('div', { class: 'endbar a', style: '--d:5' }); last.appendChild(endbar); }
  const btns = el('div', { class: 'endbtns' });
  const replay = el('button', { class: 'btn ghost', type: 'button' }); replay.textContent = 'پخش دوباره';
  btns.appendChild(replay);
  if (meta.next) { const a = el('a', { class: 'btn', href: meta.next }); a.textContent = 'فصل بعد ←'; btns.appendChild(a); }
  else { const a = el('a', { class: 'btn', href: meta.home || '../../index.html' }); a.textContent = 'بازگشت به کتابخانه'; btns.appendChild(a); }
  endbar.appendChild(btns);

  // ---- fit ----
  let forced = null;
  function fit() {
    const r = wrap.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const portrait = forced ? forced === 'portrait' : r.width / r.height < 1;
    const W = portrait ? 720 : 1280, H = portrait ? 1280 : 720;
    stage.classList.toggle('portrait', portrait);
    stage.style.width = W + 'px'; stage.style.height = H + 'px';
    stage.style.transform = `translate(-50%,-50%) scale(${Math.min(r.width / W, r.height / H)})`;
  }
  new ResizeObserver(() => fit()).observe(wrap); fit();

  // ---- timeline + menu ----
  const durs = scenes.map(s => (+s.dataset.t || 12) * 1000);
  const total = durs.reduce((a, b) => a + b, 0);
  const fmt = ms => { const s = Math.floor(ms / 1000); return fa(Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0')); };
  const segs = scenes.map((s, k) => {
    const b = el('button', { class: 'seg', type: 'button', 'aria-label': s.dataset.title, title: s.dataset.title });
    b.style.flex = `${durs[k]} 1 0`;
    if (k && scenes[k - 1].dataset.sec !== s.dataset.sec) b.classList.add('newsec');
    b.appendChild(el('i'));
    b.addEventListener('click', () => go(k));
    segBox.appendChild(b);
    return b;
  });
  const subBtns = [];
  SECS.forEach(([name, en], si) => {
    const idx = scenes.map((s, k) => +s.dataset.sec === si ? k : -1).filter(k => k >= 0);
    if (!idx.length) return;
    const li = el('li', { class: 'sec' });
    const h = el('button', { type: 'button' }, '<b></b><span class="en"></span>');
    h.querySelector('b').textContent = fa(si + 1) + '. ' + name;
    h.querySelector('.en').textContent = en || '';
    h.addEventListener('click', () => { go(idx[0]); closeMenu(); });
    const ul = el('ol', { class: 'sub' });
    idx.forEach(k => {
      const sb = el('button', { type: 'button' }); sb.textContent = scenes[k].dataset.title;
      sb.addEventListener('click', () => { go(k); closeMenu(); });
      subBtns[k] = sb;
      const l2 = el('li'); l2.appendChild(sb); ul.appendChild(l2);
    });
    li.append(h, ul); list.appendChild(li);
  });
  function closeMenu() { menu.hidden = true; menuBtn.setAttribute('aria-expanded', 'false'); }
  menuBtn.addEventListener('click', e => { e.stopPropagation(); menu.hidden = !menu.hidden; menuBtn.setAttribute('aria-expanded', String(!menu.hidden)); });
  document.addEventListener('click', e => { if (!menu.hidden && !menu.contains(e.target)) closeMenu(); });

  // ---- playback ----
  let cur = 0, elapsed = 0, playing = true, lastT = performance.now();
  function setPlaying(p) {
    playing = p; lastT = performance.now();
    stage.classList.toggle('paused', !p);
    playBtn.setAttribute('aria-label', p ? 'توقف' : 'پخش');
    playBtn.firstChild.innerHTML = p ? '<rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor"/>' : '<path d="M7 4.5v15l12-7.5z" fill="currentColor"/>';
  }
  function go(k) {
    k = Math.max(0, Math.min(scenes.length - 1, k));
    scenes[cur].classList.remove('on');
    cur = k;
    void scenes[cur].offsetWidth;
    scenes[cur].classList.add('on');
    elapsed = 0; lastT = performance.now();
    subBtns.forEach((b, i) => b && b.setAttribute('aria-current', String(i === cur)));
    const sec = SECS[+scenes[cur].dataset.sec] || [''];
    now.textContent = '';
    const nb = el('b'); nb.textContent = sec[0];
    now.append(nb, document.createTextNode(' · ' + scenes[cur].dataset.title));
    paint();
  }
  function paint() {
    const p = Math.min(1, elapsed / durs[cur]);
    segs.forEach((b, k) => { b.firstChild.style.transform = `scaleX(${k < cur ? 1 : k > cur ? 0 : p})`; });
    const done = durs.slice(0, cur).reduce((a, b) => a + b, 0) + Math.min(elapsed, durs[cur]);
    time.textContent = fmt(done) + ' / ' + fmt(total);
  }
  function tick(t) {
    if (playing) {
      elapsed += t - lastT;
      if (elapsed >= durs[cur]) {
        if (cur < scenes.length - 1) go(cur + 1);
        else { elapsed = durs[cur]; setPlaying(false); }
      }
    }
    lastT = t; paint();
    requestAnimationFrame(tick);
  }
  function toggle() {
    if (!playing && cur === scenes.length - 1 && elapsed >= durs[cur]) { go(0); setPlaying(true); return; }
    setPlaying(!playing);
  }
  playBtn.addEventListener('click', toggle);
  prev.addEventListener('click', () => go(cur - 1));
  next.addEventListener('click', () => go(cur + 1));
  replay.addEventListener('click', e => { e.stopPropagation(); go(0); setPlaying(true); });
  stage.addEventListener('click', e => { if (!e.target.closest('button,a')) toggle(); });
  document.addEventListener('keydown', e => {
    if (e.target.closest && e.target.closest('input,textarea')) return;
    if (e.key === ' ' || e.key === 'k') { e.preventDefault(); toggle(); }
    else if (e.key === 'ArrowLeft') go(cur + 1);   // RTL: left = forward
    else if (e.key === 'ArrowRight') go(cur - 1);
    else if (e.key === 'Escape') closeMenu();
  });

  // ---- layout self-check: open the page with ?check ----
  async function check() {
    stage.classList.add('checking');
    setPlaying(false);
    try { await document.fonts.ready; } catch (e) {}
    const issues = [];
    const BOXES = '.txt,.vis,.cols,.duo,.grid,.eras,.chain,.card,.term,.node,.step,.steps,.eq,.chip,.q,.scholars,.talk,.say';
    for (const mode of ['landscape', 'portrait']) {
      forced = mode; fit();
      const sr = stage.getBoundingClientRect(); const sc = sr.width / (mode === 'portrait' ? 720 : 1280);
      scenes.forEach((s, k) => {
        go(k);
        const tag = `${mode} scene ${k + 1} «${s.dataset.title}»`;
        s.querySelectorAll('*').forEach(n => {
          if (n.closest('.bgmtn') || n.closest('defs') || n.tagName === 'clipPath') return;
          const r = n.getBoundingClientRect(); if (!r.width && !r.height) return;
          const o = 3 * sc;
          if (r.left < sr.left - o || r.right > sr.right + o || r.top < sr.top - o || r.bottom > sr.bottom + o) {
            if (n.tagName === 'text' || n.matches(BOXES + ',header') || n.children.length === 0)
              issues.push(`${tag}: <${n.tagName.toLowerCase()}${n.className && typeof n.className === 'string' ? '.' + n.className.split(' ')[0] : ''}> outside the stage: «${(n.textContent || '').trim().slice(0, 40)}»`);
          }
        });
        s.querySelectorAll(BOXES).forEach(n => {
          if (n.clientHeight && (n.scrollHeight > n.clientHeight + 3 || n.scrollWidth > n.clientWidth + 3)) issues.push(`${tag}: .${n.className.split(' ')[0] || n.tagName} content overflows its box: «${n.textContent.trim().slice(0, 40)}»`);
        });
        s.querySelectorAll('svg').forEach(svg => {
          const gone = t => { const x = t.closest('.x'); return x && /gone|fly/.test(getComputedStyle(x).getPropertyValue('--xk')); };
          const ts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && !gone(t)).map(t => [t, t.getBoundingClientRect()]);
          for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) {
            const a = ts[i][1], b = ts[j][1];
            const w = Math.min(a.right, b.right) - Math.max(a.left, b.left), h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
            if (w > 2 * sc && h > 4 * sc && w * h > 0.15 * Math.min(a.width * a.height, b.width * b.height))
              issues.push(`${tag}: SVG labels overlap: «${ts[i][0].textContent.trim()}» / «${ts[j][0].textContent.trim()}»`);
          }
        });
      });
    }
    forced = null; fit(); go(0);
    const out = el('pre', { id: 'check-result' }); out.textContent = JSON.stringify({ scenes: scenes.length, seconds: total / 1000, issues });
    out.hidden = true; document.body.appendChild(out);
    console.log('[check]', issues.length ? issues.join('\n') : 'no layout issues');
    return issues;
  }
  window.__check = check;

  const startAt = /^#s(\d+)$/.exec(location.hash);
  go(startAt ? +startAt[1] - 1 : 0);
  if (/[?&]check\b/.test(location.search)) { check(); return; }
  setPlaying(true);
  requestAnimationFrame(tick);
})();
