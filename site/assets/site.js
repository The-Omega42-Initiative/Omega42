/* Ω42 portal: theme toggle, the ring, copy buttons and the views that read the open record from api/*.json. */
(function () {
  var O = window.O42 || {base: '', repo: ''};
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  function load(p) { return fetch(O.base + p).then(function (r) { if (!r.ok) throw new Error(p); return r.json(); }); }
  O.esc = esc; O.load = load;

  var tb = $('#theme-toggle');
  if (tb) tb.addEventListener('click', function () {
    var cur = document.documentElement.getAttribute('data-theme');
    var dark = cur ? cur === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
    var next = dark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('o42-theme', next); } catch (e) {}
  });

  /* the canonical loop with its mirrors */
  var SEQ = [2,5,7,3,1,4,5,9,5,5,1,6,7,4,2,6,8,5,4,9,4,4,8,3];
  $$('svg.ring').forEach(function (svg) {
    var ns = 'http://www.w3.org/2000/svg', cx = 180, cy = 180, r = 140, chords = [], dots = [];
    function pt(i, rad) { var a = i / 24 * 2 * Math.PI - Math.PI / 2; return [cx + rad * Math.cos(a), cy + rad * Math.sin(a)]; }
    for (var i = 0; i < 12; i++) {
      var p = pt(i, r - 14), q = pt(i + 12, r - 14), l = document.createElementNS(ns, 'line');
      l.setAttribute('x1', p[0]); l.setAttribute('y1', p[1]); l.setAttribute('x2', q[0]); l.setAttribute('y2', q[1]);
      l.setAttribute('class', 'chord'); svg.appendChild(l); chords.push(l);
    }
    function sel(i) {
      chords.forEach(function (c, j) { c.setAttribute('class', j === i % 12 ? 'chord on' : 'chord'); });
      dots.forEach(function (d, j) { d.setAttribute('class', (j === i || j === (i + 12) % 24) ? 'dot on' : 'dot'); });
    }
    SEQ.forEach(function (v, i) {
      var g = document.createElementNS(ns, 'g'); g.setAttribute('class', 'pos'); g.setAttribute('tabindex', '0');
      g.setAttribute('aria-label', 'P' + i + ', value ' + v + '; mirror P' + ((i + 12) % 24) + ', value ' + SEQ[(i + 12) % 24]);
      var p = pt(i, r), c = document.createElementNS(ns, 'circle'), t = document.createElementNS(ns, 'text');
      c.setAttribute('cx', p[0]); c.setAttribute('cy', p[1]); c.setAttribute('r', 13); c.setAttribute('class', 'dot');
      t.setAttribute('x', p[0]); t.setAttribute('y', p[1] + 4.5); t.setAttribute('text-anchor', 'middle');
      if (v % 3 === 0) t.setAttribute('class', 'crown');
      t.textContent = v; g.appendChild(c); g.appendChild(t); svg.appendChild(g); dots.push(c);
      ['mouseenter', 'focus', 'click'].forEach(function (e) { g.addEventListener(e, function () { sel(i); }); });
    });
    sel(0);
  });

  /* copy buttons: data-copy="#id" copies that element's text; data-copy-url fetches text first */
  $$('[data-copy], [data-copy-url]').forEach(function (b) {
    b.addEventListener('click', function () {
      var label = b.textContent;
      var get = b.dataset.copyUrl ? fetch(O.base + b.dataset.copyUrl).then(function (r) { return r.text(); })
                                  : Promise.resolve(($(b.dataset.copy) || {}).textContent || '');
      get.then(function (txt) { return navigator.clipboard.writeText(txt); })
        .then(function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = label; }, 1600); })
        .catch(function () { b.textContent = 'Select and copy manually'; });
    });
  });

  /* live numbers */
  var stats = $('#live-stats');
  if (stats) Promise.all([load('api/library.json'), load('api/register.json'), load('api/prior-art.json'), load('api/contributors.json')])
    .then(function (d) {
      var nav = d[0].items.filter(function (i) { return i.kind === 'navigation'; }).length;
      stats.innerHTML = [[nav, 'navigations'], [d[1].domains.length, 'domains in the register'], [d[1].same_state.length + d[1].mirror.length, 'meetings on the structure'],
        [d[2].length, 'prior-art disclosures'], [d[3].length, 'credited contributors']]
        .map(function (s) { return '<div><b>' + s[0] + '</b><span>' + s[1] + '</span></div>'; }).join('');
    }).catch(function () {});

  /* library */
  var lib = $('#library');
  if (lib) load('api/library.json').then(function (d) {
    var q = $('#lib-q'), k = $('#lib-kind'), a = $('#lib-area');
    d.areas.forEach(function (x) { a.insertAdjacentHTML('beforeend', '<option value="' + esc(x.slug) + '">' + esc(x.name) + '</option>'); });
    function draw() {
      var s = (q.value || '').toLowerCase();
      var rows = d.items.filter(function (i) {
        return (!k.value || i.kind === k.value) && (!a.value || i.area === a.value) &&
               (!s || (i.title + ' ' + i.by + ' ' + (i.navigator || '') + ' ' + i.id).toLowerCase().indexOf(s) >= 0);
      });
      lib.innerHTML = rows.length ? rows.map(function (i) {
        var c = i.coordinate ? '<span class="chip gold">P' + i.coordinate.anchor + ' ' + esc(i.coordinate.name) + '</span>' : '';
        return '<tr><td class="num">' + esc(i.id) + '</td><td><a href="https://github.com/' + O.repo + '/blob/main/' + esc(i.path) + '">' + esc(i.title) + '</a><div class="row">' +
          '<span class="chip">' + esc(i.kind) + '</span><span class="chip">' + esc(i.area) + '</span>' + c + '</div></td><td>' + esc(i.by) +
          (i.navigator ? '<div class="note">' + esc(i.navigator) + '</div>' : '') + '</td><td class="num">' + esc(i.date) + '</td></tr>';
      }).join('') : '<tr><td colspan="4" class="muted">Nothing matches. Clear the filters to see the whole record.</td></tr>';
      $('#lib-count').textContent = rows.length + ' of ' + d.items.length;
    }
    [q, k, a].forEach(function (e) { e.addEventListener('input', draw); });
    draw();
  }).catch(function () { lib.innerHTML = '<tr><td colspan="4">The record could not be loaded.</td></tr>'; });

  /* register */
  var reg = $('#register');
  if (reg) load('api/register.json').then(function (d) {
    function pairs(list, word) { return list.map(function (p) { return '<tr><td>' + esc(p[0]) + '</td><td class="muted">' + word + '</td><td>' + esc(p[1]) + '</td></tr>'; }).join(''); }
    reg.innerHTML = pairs(d.same_state, 'same place as') + pairs(d.mirror, 'mirrors');
    $('#register-note').textContent = d.domains.length + ' domains. Expected by chance: ' + d.expected.same_state.toFixed(2) + ' shared places and ' +
      d.expected.mirror.toFixed(2) + ' mirror pairs; found ' + d.same_state.length + ' and ' + d.mirror.length + '.';
  }).catch(function () {});

  /* prior art */
  var pa = $('#prior-art');
  if (pa) load('api/prior-art.json').then(function (d) {
    pa.innerHTML = d.length ? d.map(function (e) {
      return '<tr><td class="num">' + esc(e.id) + '</td><td><a href="https://github.com/' + O.repo + '/blob/main/' + esc(e.path) + '">' + esc(e.title) + '</a><div class="note">' + esc(e.contributor) + ' · ' + esc(e.area) +
        '</div></td><td class="num">' + esc(e.disclosed_utc) + '</td><td class="num" title="' + esc(e.sha256) + '">' + esc(e.sha256.slice(0, 12)) + '…</td></tr>';
    }).join('') : '<tr><td colspan="4" class="muted">No disclosures yet. The first one you publish appears here with its date and hash.</td></tr>';
  }).catch(function () {});

  /* research areas */
  var ar = $('#areas');
  if (ar) load('api/research-areas.json').then(function (d) {
    ar.innerHTML = d.map(function (a) {
      var t = a.primary ? '<span class="chip gold">primary inquiry</span>' : (a.optional ? '<span class="chip">optional programme</span>' : '');
      return '<div class="card"><div class="row"><h3>' + esc(a.name) + '</h3>' + t + '</div><p>' + esc(a.about) + '</p><p class="note">' + a.count + ' item(s) in the record</p>' +
        '<a class="go" href="https://github.com/' + O.repo + '/tree/main/research/' + esc(a.slug) + '">Open questions and how to contribute →</a></div>';
    }).join('');
  }).catch(function () {});

  /* contributors and professionals */
  var co = $('#contributors');
  if (co) load('api/contributors.json').then(function (d) {
    co.innerHTML = d.length ? d.slice(0, 50).map(function (c) {
      return '<tr><td>' + esc(c.name) + ' <span class="note mono">@' + esc(c.handle) + '</span></td><td class="num">' + c.points + '</td><td>' + esc(c.level) + '</td><td class="num">' + c.contributions.length + '</td></tr>';
    }).join('') : '<tr><td colspan="4" class="muted">The first accepted contribution opens this table.</td></tr>';
  }).catch(function () {});
  var db = $('#dashboard');
  if (db) load('api/dashboard.json').then(function (d) {
    var val = function (v) { return typeof v === 'object' ? Object.keys(v).map(function (k) { return esc(k) + ' ' + esc(v[k]); }).join(' · ') : esc(v); };
    db.innerHTML = d.figures.map(function (f) {
      return '<tr><td>' + esc(f.label) + '</td><td class="num">' + val(f.value) + '</td><td class="num">' + (f.expected_by_chance == null ? '—' : esc(f.expected_by_chance)) +
        '</td><td class="note">Counts ' + esc(f.counts) + '. Does not count ' + esc(f.does_not_count) + '.</td></tr>';
    }).join('');
  }).catch(function () {});
  var pr = $('#professionals');
  if (pr) load('api/professionals.json').then(function (d) {
    pr.innerHTML = d.length ? d.map(function (p) {
      return '<div class="card"><span class="k">' + esc(p.id) + ' · verified ' + esc(p.verified_utc) + '</span><h3>' + esc(p.name) + '</h3><p>' + esc(p.title) + ', ' + esc(p.field) +
        '</p><p class="note">' + esc(p.statement) + '</p>' + (p.link ? '<a class="go" href="' + esc(p.link) + '">Profile →</a>' : '') + '</div>';
    }).join('') : '<p class="muted">No verified professionals yet. Be the first: use the verification form below.</p>';
  }).catch(function () {});
})();

/* Living Frontier: the question of the day fills the ask box on this page. */
(function () {
  document.querySelectorAll('[data-ask]').forEach(function (a) {
    a.addEventListener('click', function (e) { var box = document.getElementById('ask-q'); if (!box) return; e.preventDefault();
      box.value = a.getAttribute('data-ask'); box.scrollIntoView({behavior: 'smooth', block: 'center'}); box.focus(); });
  });
})();

/* Ask Omega42 (home page): hand the question to the Strike app in this tab's session storage, so it never appears in a URL;
   if storage is unavailable, in the URL fragment, which browsers never send to a server. The form has no action and no field names. */
(function () {
  var f = document.getElementById('ask-form'); if (!f) return;
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = document.getElementById('ask-q').value.trim(); if (!q) { document.getElementById('ask-q').focus(); return; }
    var data = {q: q, mode: document.getElementById('ask-mode').value, present: document.getElementById('ask-present').value};
    try { sessionStorage.setItem('o42-ask', JSON.stringify(data)); location.href = 'strike.html#from=home'; }
    catch (err) { location.href = 'strike.html#' + new URLSearchParams(data).toString(); }
  });
})();

/* Back to top: shown after the first screen of scrolling. */
(function () { var t = document.querySelector('.totop'); if (!t) return;
  function f() { t.classList.toggle('show', window.scrollY > window.innerHeight * 1.2); }
  window.addEventListener('scroll', f, {passive: true}); f();
  t.addEventListener('click', function (e) { e.preventDefault(); window.scrollTo({top: 0, behavior: window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); }); })();
/* The emblem: the white walker brightens each number as it arrives (Co-Builder branch emblem-facet-pulse). */
(function () {
  var svg = document.querySelector('svg.emblem');
  if (!svg || !window.matchMedia || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var walker = svg.querySelector('.walker'); if (!walker) return;
  var nodes = Array.prototype.map.call(svg.querySelectorAll('.node'), function (g) {
    var c = g.querySelector('circle'); return { g: g, x: +c.getAttribute('cx'), y: +c.getAttribute('cy') };
  });
  var id = 0;
  function tick() {
    id = 0; if (document.hidden) return;
    var m = walker.getCTM && walker.getCTM();
    if (m) {
      var best = null, d = Infinity;
      nodes.forEach(function (n) { var t = Math.hypot(m.e - n.x, m.f - n.y); if (t < d) { d = t; best = n; } });
      nodes.forEach(function (n) { n.g.classList.toggle('arriving', n === best && d <= 19); });
    }
    id = requestAnimationFrame(tick);
  }
  function start() { if (!document.hidden && !id) id = requestAnimationFrame(tick); }
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { if (id) cancelAnimationFrame(id); id = 0; nodes.forEach(function (n) { n.g.classList.remove('arriving'); }); } else start();
  });
  start();
})();
/* The emblem's pause control. */
(function () {
  var b = document.querySelector('.emb-pause'), svg = document.querySelector('svg.emblem');
  if (!b || !svg) return;
  b.addEventListener('click', function () {
    var p = !svg.classList.contains('paused');
    svg.classList.toggle('paused', p);
    try { p ? svg.pauseAnimations() : svg.unpauseAnimations(); } catch (e) {}
    b.setAttribute('aria-pressed', String(p)); b.textContent = p ? '▶ play' : '❚❚ pause';
    b.setAttribute('aria-label', p ? 'Play the emblem animation' : 'Pause the emblem animation');
  });
})();
// Today's wonder: one verified fact, question or reflection, chosen by the visitor's local date
(function () {
  var t = document.getElementById('wonder-text'), l = document.getElementById('wonder-link'); if (!t || !l) return;
  var W = [
    ['Twelve steps on, every state of the eighty-one meets its own negative. Zero alone is its own negative.', 'paper.html'],
    ['Eighty-one states, five loops: three of 24, one of 8, and a single still point.', 'paper.html'],
    ['The world never ends: at depth k there are 9^k states and (3^k + 1)/2 loops, and every loop lifts to three loops three times as long.', 'paper.html'],
    ['You can hear the shape of Omega42: the spectrum alone tells you exactly which loops the world is made of.', 'geometria.html'],
    ['Three readings of a seven-symbol view can tell all 81 states apart. Two readings never can.', 'paper.html'],
    ['Open question: can six readers, each seeing a mod 7, tell apart all 59,049 states at depth 5? Seven can.', 'research.html'],
    ['Square the Omega42 law and you get Arnold’s cat map, the classic picture of chaos. The 81 states are its ninth-points.', 'geometria.html'],
    ['After 24 steps, exactly 103,680 points of the golden torus come home. The 81 states are 1 in every 1,280 of them.', 'geometria.html'],
    ['The quantity a² + ab − b² flips its sign at every step, and yet its square never changes.', 'philosophy.html'],
    ['Of all hyperbolic triangles with angles π/p, π/q, π/r, the smallest has area π/42.', 'paper.html'],
    ['Two things can sound the same and live in different worlds: harmonic resonance 1, orbit resonance 0.', 'paper.html'],
    ['A memory that only relabels records nothing. Remembering a, the first coordinate, is such a memory.', 'paper.html'],
    ['Reflection: if a limited observer can see the whole by joining others, what does seeing alone leave out?', 'philosophy.html'],
    ['In the canonical loop the digits 3, 6 and 9 arrive exactly every fourth step.', 'symbols.html']
  ];
  var d = new Date(), n = Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 864e5), w = W[n % W.length];
  t.textContent = w[0]; l.href = w[1];
})();
/* Living Questions (HRP-04): every section heading of a reading page, and any element with data-question, opens as a question
   in the Strike app. The question carries its source (page, section, release) and travels in session storage, never in a URL. */
(function () {
  var V = (document.querySelector('meta[name="o42-version"]') || {}).content || 'V335 Rev.450 STABLE';
  function go(q, mode) {
    var data = {q: q, mode: mode || 'explore', present: 'ere', go: '0'};
    try { sessionStorage.setItem('o42-ask', JSON.stringify(data)); location.href = 'strike.html#from=living'; }
    catch (err) { location.href = 'strike.html#' + new URLSearchParams(data).toString(); }
  }
  var page = document.title.replace(/\s*[·|—-]\s*(Ω42|Omega42).*$/, '');
  document.querySelectorAll('article.paper h2, article.paper h3, .companion article h2, .lq-scope h2, .lq-scope h3').forEach(function (h) {
    var t = h.textContent.replace(/^§\s*/, '').replace(/\s+/g, ' ').trim(); if (!t || t.length < 4 || h.querySelector('.lq')) return;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'lq'; b.textContent = 'Ask about this ↗';
    b.setAttribute('aria-label', 'Explore "' + t + '" with the Navigator');
    b.addEventListener('click', function () {
      go('What does "' + t + '" open up: what rests beneath it, what does it hide, and where does it lead? (from ' + page + ', Omega42 ' + V + ')');
    });
    h.appendChild(document.createTextNode(' ')); h.appendChild(b);
  });
  document.querySelectorAll('[data-question]').forEach(function (el) {
    el.classList.add('lq-link'); el.setAttribute('role', 'button'); el.tabIndex = 0;
    var fire = function () { go(el.getAttribute('data-question'), el.getAttribute('data-mode')); };
    el.addEventListener('click', fire); el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fire(); } });
  });
})();
// Language preference: opens the public page in machine translation; the English text stays authoritative
(function () {
  var sel = document.getElementById('lang-pick'); if (!sel) return;
  sel.addEventListener('change', function () {
    var tl = sel.value; if (!tl) return;
    var u = location.href.split('#')[0];
    if (/^https?:\/\/(localhost|127\.)/.test(u)) { sel.value = ''; return; }
    location.href = 'https://translate.google.com/translate?sl=en&tl=' + encodeURIComponent(tl) + '&u=' + encodeURIComponent(u);
  });
})();
