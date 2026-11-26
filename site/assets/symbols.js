/* Ω42 symbols page: the nine-point figure, the Omega42 loop, the mirror and doubling, each layer switchable. */
(function () {
  var svg = document.getElementById('sym-fig'); if (!svg) return;
  var NS = 'http://www.w3.org/2000/svg', C = 200, R = 150;
  function pt(k) { var a = (-90 + 40 * (k % 9)) * Math.PI / 180; return [C + R * Math.cos(a), C + R * Math.sin(a)]; }
  function path(seq, closed) { return 'M' + seq.map(function (k) { var p = pt(k); return p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' L') + (closed ? ' Z' : ''); }
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); (parent || svg).appendChild(e); return e; }
  var loop = [2, 5, 7, 3, 1, 4, 5, 9, 5, 5, 1, 6, 7, 4, 2, 6, 8, 5, 4, 9, 4, 4, 8, 3];   // the canonical cycle from the seeds (2, 5), Core Part 1.8
  el('circle', {cx: C, cy: C, r: R, 'class': 'rim'});
  el('line', {x1: C, y1: C - R - 22, x2: C, y2: C + R + 22, 'class': 'axis', 'data-layer': 'mirror'});
  var layers = {
    tri: [el('path', {d: path([3, 6, 9], true), 'class': 'L tri', 'data-layer': 'tri'})],
    hex: [el('path', {d: path([1, 4, 2, 8, 5, 7], true), 'class': 'L hex', 'data-layer': 'hex'})],
    loop: [el('path', {d: path(loop.slice(0, 13)), 'class': 'L lpa', 'data-layer': 'loop', pathLength: 1}),
           el('path', {d: path(loop.slice(12).concat([9])), 'class': 'L lpb', 'data-layer': 'loop', pathLength: 1})],
    mirror: [], dbl: [el('path', {d: path([1, 2, 4, 8, 7, 5], true), 'class': 'L dbl', 'data-layer': 'dbl'})]
  };
  [[1, 8], [2, 7], [3, 6], [4, 5]].forEach(function (p) { var a = pt(p[0]), b = pt(p[1]);
    layers.mirror.push(el('line', {x1: a[0], y1: a[1], x2: b[0], y2: b[1], 'class': 'L mir', 'data-layer': 'mirror'})); });
  layers.mirror.push(svg.querySelector('.axis'));
  var walker = el('circle', {r: 7, 'class': 'walker'});
  var nodes = {};
  [9, 1, 2, 3, 4, 5, 6, 7, 8].forEach(function (k) { var p = pt(k), g = el('g', {'class': 'node' + (k % 3 ? '' : ' t')});
    el('circle', {cx: p[0], cy: p[1], r: 16}, g); var t = el('text', {x: p[0], y: p[1] + 5}, g); t.textContent = k; nodes[k] = g; });
  var buttons = document.querySelectorAll('[data-show]'), cap = document.getElementById('sym-cap');
  function show(name) {
    Object.keys(layers).forEach(function (n) { layers[n].forEach(function (e) { e.classList.toggle('on', name === 'all' ? n !== 'mirror' && n !== 'dbl' : n === name); }); });
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-show') === name)); });
    var src = document.querySelector('[data-cap="' + name + '"]'); if (src && cap) cap.innerHTML = src.innerHTML;
    if (name === 'loop' || name === 'all') replay(); else stop();
  }
  var timer = null, still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function place(i) { var p = pt(loop[i % 24]); walker.setAttribute('cx', p[0]); walker.setAttribute('cy', p[1]);
    Object.keys(nodes).forEach(function (k) { nodes[k].classList.toggle('here', +k === loop[i % 24]); });
    var st = document.getElementById('sym-step'); if (st) st.textContent = 'step ' + (i % 24) + ' of 24 · digit ' + loop[i % 24] + ' · twelve steps on: ' + loop[(i + 12) % 24]; }
  function replay() { stop(); walker.style.display = ''; var i = 0; at = 0; place(0); if (pause) { pause.textContent = 'Pause'; pause.setAttribute('aria-pressed', 'false'); } if (still) return; timer = setInterval(function () { at = ++i; place(i); }, 900); }
  function stop() { if (timer) clearInterval(timer); timer = null; walker.style.display = 'none'; Object.keys(nodes).forEach(function (k) { nodes[k].classList.remove('here'); });
    var st = document.getElementById('sym-step'); if (st) st.textContent = ''; }
  buttons.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-show')); }); });
  var pause = document.getElementById('sym-pause'), at = 0;
  if (pause) pause.addEventListener('click', function () {
    if (timer) { clearInterval(timer); timer = null; pause.textContent = 'Play the loop'; pause.setAttribute('aria-pressed', 'true'); }
    else { walker.style.display = ''; pause.textContent = 'Pause'; pause.setAttribute('aria-pressed', 'false');
      if (!still) timer = setInterval(function () { place(++at); }, 900); }
  });
  var box = document.getElementById('sym-node');
  function d9(x) { return ((x % 9) + 9) % 9 || 9; }
  function role(k) {
    var r = k % 9, unit = r % 3 !== 0, inv = null;
    for (var y = 1; y < 9 && unit; y++) if ((r * y) % 9 === 1) inv = y;
    var pos = []; loop.forEach(function (v, i) { if (v === k) pos.push(i); });
    var ant = k === 9 ? '9 is its own Antipode (9 = 0 modulo 9)' : 'Its Antipode is ' + (9 - k) + ', the mirror across the vertical axis';
    return '<b>' + k + '</b> · ' + (unit ? 'a unit modulo 9: on the six-point path; it has an inverse, ' + inv + ' (' + k + ' × ' + inv + ' = ' + (k * inv) + ' = 1 modulo 9)' : 'in the 3-layer: on the triangle; it has no inverse modulo 9') +
      '. Doubled it gives ' + d9(2 * k) + '. ' + ant + '. On the 24-step loop it appears ' + (pos.length ? pos.length + ' times, at steps ' + pos.join(', ') : 'never') + '.';
  }
  Object.keys(nodes).forEach(function (k) { var g = nodes[k]; g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button'); g.setAttribute('aria-label', 'Digit ' + k + ': show its role');
    function pick() { if (box) box.innerHTML = role(+k); Object.keys(nodes).forEach(function (j) { nodes[j].classList.toggle('picked', j === k); }); }
    g.addEventListener('click', pick); g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } }); });
  show('all');
})();
