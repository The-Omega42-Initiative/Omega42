/* The Universal Observatory of Existence: interactive instruments over the exact Omega42 mathematics.
   Every number on the page is computed here, in the browser, by exhaustive enumeration. Nothing is sent anywhere. */
(function () {
  'use strict';
  var M = 9, S = [];
  for (var a = 0; a < M; a++) for (var b = 0; b < M; b++) S.push([a, b]);
  function N(x, m) { m = m || M; return [x[1], (x[0] + x[1]) % m]; }
  function key(x) { return x[0] + ',' + x[1]; }
  function jump(x, t) { for (var i = 0; i < t; i++) x = N(x); return x; }
  function $(id) { return document.getElementById(id); }
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function orbitsMod(m) {
    var seen = {}, out = [];
    for (var a = 0; a < m; a++) for (var b = 0; b < m; b++) {
      var x = [a, b]; if (seen[key(x)]) continue;
      var o = [x], y = N(x, m);
      while (key(y) !== key(x)) { o.push(y); y = N(y, m); }
      o.forEach(function (z) { seen[key(z)] = 1; }); out.push(o);
    }
    return out;
  }
  var ORB = orbitsMod(9), orbitOf = {};
  ORB.forEach(function (o, i) { o.forEach(function (x) { orbitOf[key(x)] = i; }); });

  // ---------- I. The Aperture laboratory ----------
  var CERT = [[3,2,1,1,1,0,5,4,3],[3,2,0,2,1,1,1,4,5],[3,3,1,1,5,3,1,6,0],[2,0,1,3,0,4,2,5,3],[3,6,3,5,3,5,0,0,3],
              [6,4,4,3,0,6,2,0,2],[6,2,5,2,4,5,5,6,0],[6,4,5,1,2,4,4,0,2],[5,3,4,5,1,3,3,3,6]];
  var APS = {
    optimal: { name: 'The optimal seven-symbol Aperture (certificate)', h: function (x) { return CERT[x[0]][x[1]]; } },
    a7: { name: 'The obvious seven-symbol view: a mod 7', h: function (x) { return x[0] % 7; } },
    a9: { name: 'The full coordinate a (nine symbols)', h: function (x) { return x[0]; } }
  };
  function trace(h, x, n) { var t = []; for (var i = 0; i < n; i++) { t.push(h(x)); x = N(x); } return t; }
  function apertureLab() {
    var box = $('ap-lab'); if (!box) return;
    var sel = $('ap-which'), sa = $('ap-a'), sb = $('ap-b'), sn = $('ap-n');
    for (var i = 0; i < 9; i++) { sa.add(new Option(i, i)); sb.add(new Option(i, i)); }
    sa.value = 1; sb.value = 8;
    function draw() {
      var h = APS[sel.value].h, x = [+sa.value, +sb.value], n = +sn.value;
      $('ap-n-out').textContent = n;
      var t = trace(h, x, n), cand = S.filter(function (y) { return trace(h, y, n).join() === t.join(); });
      var counts = [];
      for (var k = 1; k <= 8; k++) { var set = {}; S.forEach(function (y) { set[trace(h, y, k).join()] = 1; }); counts.push(Object.keys(set).length); }
      $('ap-trace').textContent = t.join(' · ');
      $('ap-cand').textContent = cand.length === 1 ? 'Exactly one state fits: (' + key(cand[0]) + ') — recognized.' : cand.length + ' states still fit these observations.';
      $('ap-counts').textContent = counts.map(function (c, i) { return (i + 1) + ' obs: ' + c; }).join('   ');
      var g = $('ap-grid'); g.innerHTML = '';
      for (var a = 0; a < 9; a++) for (var b = 0; b < 9; b++) {
        var c = el('span', 'cell'), isC = cand.some(function (y) { return y[0] === a && y[1] === b; });
        c.textContent = h([a, b]);
        if (isC) c.classList.add('on'); if (a === x[0] && b === x[1]) c.classList.add('here');
        c.title = '(' + a + ',' + b + ')'; g.appendChild(c);
      }
    }
    [sel, sa, sb, sn].forEach(function (e) { e.addEventListener('input', draw); });
    draw();
  }

  // ---------- II. Collective observability ----------
  function collectiveLab() {
    var box = $('co-lab'); if (!box) return;
    var ins = [$('co-o1'), $('co-o2'), $('co-o3')], use3 = $('co-use3'), r = $('co-r');
    var h = APS.a7.h;
    function draw() {
      var offs = [+ins[0].value, +ins[1].value].concat(use3.checked ? [+ins[2].value] : []);
      var R = +r.value; $('co-r-out').textContent = R;
      var fib = {};
      S.forEach(function (x) {
        var t = []; offs.forEach(function (o) { for (var i = 0; i < R; i++) t.push(h(jump(x, o + i))); });
        fib[t.join()] = (fib[t.join()] || 0) + 1;
      });
      var classes = Object.keys(fib).length, worst = Math.max.apply(null, Object.keys(fib).map(function (k) { return fib[k]; }));
      var need = 25;
      for (var q = 1; q <= 24; q++) {
        var s2 = {}; S.forEach(function (x) { var t = []; offs.forEach(function (o) { for (var i = 0; i < q; i++) t.push(h(jump(x, o + i))); }); s2[t.join()] = 1; });
        if (Object.keys(s2).length === 81) { need = q; break; }
      }
      $('co-res').textContent = classes + ' of 81 states told apart; the largest group still confused holds ' + worst + '.';
      $('co-need').textContent = need === 25 ? 'These observers never separate every state.' : 'All 81 states are recognized after ' + need + ' round' + (need > 1 ? 's' : '') + ' of joint observation.';
    }
    ins.concat([use3, r]).forEach(function (e) { e.addEventListener('input', draw); });
    $('co-preset').addEventListener('click', function () { ins[0].value = 0; ins[1].value = 2; ins[2].value = 5; use3.checked = true; r.value = 1; draw(); });
    draw();
  }

  // ---------- III. Spectral architecture and the coherence calculus ----------
  function mults() { var m = []; for (var j = 0; j < 24; j++) m.push(3 + (j % 3 === 0 ? 1 : 0) + (j === 0 ? 1 : 0)); return m; }
  function coherenceLab() {
    var box = $('ch-lab'); if (!box) return;
    var al = $('ch-alpha'), svg = $('ch-svg'), m = mults();
    function draw() {
      var A = +al.value; $('ch-alpha-out').textContent = A.toFixed(1);
      var W = 480, H = 160, bw = W / 24, out = '';
      for (var j = 0; j < 24; j++) {
        var c = 1 / (1 + A * Math.pow(Math.sin(Math.PI * j / 24), 2)), h = c * (H - 24);
        out += '<rect x="' + (j * bw + 2) + '" y="' + (H - 16 - h) + '" width="' + (bw - 4) + '" height="' + h + '" class="bar m' + m[j] + '"><title>harmonic ' + j + ': response ' + c.toFixed(3) + ', multiplicity ' + m[j] + '</title></rect>';
        if (j % 3 === 0) out += '<text x="' + (j * bw + bw / 2) + '" y="' + (H - 3) + '" text-anchor="middle">' + j + '</text>';
      }
      svg.innerHTML = out;
      var energyKept = 0; for (var k = 0; k < 24; k++) energyKept += m[k] / (1 + A * Math.pow(Math.sin(Math.PI * k / 24), 2));
      $('ch-c0').textContent = '1.000';
      $('ch-c12').textContent = (1 / (1 + A)).toFixed(3);
      $('ch-avg').textContent = (energyKept / 81).toFixed(3);
    }
    al.addEventListener('input', draw); draw();
  }

  // ---------- IV. Reversible memory ----------
  function memoryLab() {
    var box = $('me-lab'); if (!box) return;
    var sIns = [], wrap = $('me-sums'), lens = ORB.map(function (o) { return o.length; });
    ORB.forEach(function (o, i) {
      var lab = el('label', null, 'Orbit ' + (i + 1) + ' (length ' + o.length + ')'), inp = el('input'); inp.type = 'number'; inp.min = 0; inp.max = 8; inp.value = 0;
      lab.appendChild(inp); wrap.appendChild(lab); sIns.push(inp);
    });
    var state = null, steps = 0;
    function g() { // the canonical representative: put the whole orbit sum on the orbit's first state
      var s = sIns.map(function (e) { return ((+e.value % 9) + 9) % 9; });
      return function (x) { var i = orbitOf[key(x)]; return key(x) === key(ORB[i][0]) ? s[i] : 0; };
    }
    function reset() { var x = [+$('me-a').value, +$('me-b').value]; state = { x: x, m: +$('me-m').value }; steps = 0; show(); }
    function step(dir) {
      var G = g();
      if (dir > 0) { state.m = (state.m + G(state.x)) % 9; state.x = N(state.x); steps++; }
      else { var p = [(state.x[1] - state.x[0] + 9) % 9, state.x[0]]; state.m = (state.m - G(p) + 9) % 9; state.x = p; steps--; }
    }
    function period() {
      var G = g(), x = state.x, m = state.m, n = 0;
      do { m = (m + G(x)) % 9; x = N(x); n++; } while (!(key(x) === key(state.x) && m === state.m));
      return n;
    }
    function show() {
      var i = orbitOf[key(state.x)], s = ((+sIns[i].value % 9) + 9) % 9;
      $('me-state').textContent = '(a, b, m) = (' + state.x[0] + ', ' + state.x[1] + ', ' + state.m + ')';
      $('me-steps').textContent = steps;
      $('me-period').textContent = period();
      $('me-class').textContent = '(' + sIns.map(function (e) { return ((+e.value % 9) + 9) % 9; }).join(', ') + ')';
      $('me-note').textContent = s === 0 ? 'This orbit has sum 0: a full revolution returns the memory unchanged — no winding.' :
        'This orbit has sum ' + s + ': each revolution of ' + lens[i] + ' steps moves the memory by ' + s + '.';
    }
    for (var k = 0; k < 9; k++) { $('me-a').add(new Option(k, k)); $('me-b').add(new Option(k, k)); $('me-m').add(new Option(k, k)); }
    $('me-a').value = 0; $('me-b').value = 1;
    $('me-fwd').addEventListener('click', function () { step(1); show(); });
    $('me-back').addEventListener('click', function () { step(-1); show(); });
    $('me-rev').addEventListener('click', function () { var L = lens[orbitOf[key(state.x)]]; for (var t = 0; t < L; t++) step(1); show(); });
    $('me-reset').addEventListener('click', reset);
    $('me-unit').addEventListener('click', function () { sIns.forEach(function (e) { e.value = 0; }); sIns[orbitOf['0,1']].value = 1; reset(); });
    sIns.concat([$('me-a'), $('me-b'), $('me-m')]).forEach(function (e) { e.addEventListener('input', reset); });
    reset();
  }

  // ---------- V. Depth and renormalization ----------
  function depthLab() {
    var box = $('dp-lab'); if (!box) return;
    var sel = $('dp-k');
    function draw() {
      var k = +sel.value, m = Math.pow(3, k), O = orbitsMod(m), hist = {};
      O.forEach(function (o) { hist[o.length] = (hist[o.length] || 0) + 1; });
      $('dp-sum').textContent = 'ℤ/' + m + ': ' + (m * m) + ' states in ' + O.length + ' orbits (and (3^' + k + ' + 1)/2 = ' + ((m + 1) / 2) + ').';
      $('dp-hist').textContent = Object.keys(hist).sort(function (p, q) { return p - q; }).map(function (L) { return hist[L] + ' × length ' + L; }).join('   ');
      if (k < 5) {
        var Ol = orbitsMod(m / 3 >= 1 ? m : 1), idx = {}; // lift from this depth to the next
        Ol.forEach(function (o, i) { o.forEach(function (x) { idx[key(x)] = i; }); });
        var Oh = orbitsMod(m * 3), t = {};
        Oh.forEach(function (o) { var r = [o[0][0] % m, o[0][1] % m], L0 = Ol[idx[key(r)]].length, kk = L0 + ' → ' + o.length; t[kk] = (t[kk] || 0) + 1; });
        $('dp-lift').textContent = 'Lifting to ℤ/' + (m * 3) + ': ' + Object.keys(t).map(function (kk) { return t[kk] + ' orbit' + (t[kk] > 1 ? 's' : '') + ' ' + kk; }).join(';  ') + '.';
      } else $('dp-lift').textContent = '';
    }
    sel.addEventListener('input', draw); draw();
  }

  function spectralStrip() {
    var s = $('sp-strip'); if (!s) return; var m = mults(), out = '';
    for (var j = 0; j < 24; j++) out += '<span class="m' + m[j] + '" title="harmonic ' + j + ': multiplicity ' + m[j] + '">' + m[j] + '</span>';
    s.innerHTML = out;
  }

  apertureLab(); collectiveLab(); coherenceLab(); memoryLab(); depthLab(); spectralStrip();
})();
