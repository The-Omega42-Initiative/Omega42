/* Ω42 playground: the four operations on the Antipodes, and the 81-state explorer. Everything is computed in the page. */
(function () {
  var $ = function (id) { return document.getElementById(id); };
  function mod(x) { return ((x % 9) + 9) % 9; }
  function inv(x) { for (var y = 1; y < 9; y++) if (mod(x * y) === 1) return y; return null; }
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function frac(p, q) { if (q === 0) return 'undefined'; var g = gcd(p, q); p /= g; q /= g; if (q < 0) { p = -p; q = -q; } return q === 1 ? String(p) : p + '/' + q; }
  // ---- Antipodes
  var ax = $('ap-x'), am = $('ap-mode');
  function antipodes() {
    if (!ax) return;
    var x = +ax.value, m = am.value, rows, notes;
    if (m === 'int') {
      var a = 9 - x;
      rows = [['Antipode', 'A(' + x + ') = 9 − ' + x, a], ['Addition', x + ' + ' + a, x + a], ['Subtraction', x + ' − ' + a, x - a],
              ['Division', x + ' ÷ ' + a, frac(x, a) + (a ? ' ≈ ' + (x / a).toFixed(4) : '')], ['Multiplication', x + ' × ' + a, x * a]];
      notes = 'Exact identity: x(9 − x) = 81/4 − (x − (9 − x))²/4 → ' + (x * a) + ' = 81/4 − ' + Math.pow(x - a, 2) + '/4. The product rises as the separation falls; no whole number sits at the balance point 4.5.';
    } else {
      var b = mod(-x), i = inv(b);
      rows = [['Antipode', 'A(' + x + ') = −' + x + ' mod 9', b + (x === 0 ? ' (0 is its own Antipode)' : '')], ['Addition', x + ' + ' + b + ' mod 9', mod(x + b)],
              ['Subtraction', x + ' − ' + b + ' = 2 × ' + x + ' mod 9', mod(x - b)], ['Division', x + ' × ' + b + '⁻¹ mod 9', i === null ? 'undefined: ' + b + ' has no inverse modulo 9' : mod(x * i) + ' (= −1)'],
              ['Multiplication', x + ' × ' + b + ' = −' + x + '² mod 9', mod(x * b)]];
      notes = 'Modulo 9, the half is 5 (2 × 5 = 10 = 1) and minus the half is 4: the central pair (4, 5) is (−1/2, +1/2), one unit apart. The ratio of a digit to its Antipode is −1 for every digit with an inverse (1, 2, 4, 5, 7, 8) and undefined for 0, 3, 6.';
    }
    $('ap-out').innerHTML = rows.map(function (r) { return '<tr><td>' + r[0] + '</td><td class="mono">' + r[1] + '</td><td class="num">' + r[2] + '</td></tr>'; }).join('');
    $('ap-note').textContent = notes;
  }
  if (ax) { ax.addEventListener('input', antipodes); am.addEventListener('change', antipodes); antipodes(); }
  // ---- 81 states
  var grid = $('st-grid'); if (!grid) return;
  function T(s) { return [s[1], mod(s[0] + s[1])]; }
  function Ti(s) { return [mod(s[1] - s[0]), s[0]]; }
  function key(s) { return s[0] + ',' + s[1]; }
  var orbitOf = {}, orbits = [];
  for (var a = 0; a < 9; a++) for (var b = 0; b < 9; b++) {
    var s = [a, b]; if (orbitOf[key(s)] !== undefined) continue;
    var o = [], x = s; do { orbitOf[key(x)] = orbits.length; o.push(x); x = T(x); } while (key(x) !== key(s));
    orbits.push(o);
  }
  var names = orbits.map(function (o) { return o.length === 1 ? 'the still point' : o.length === 8 ? 'the loop of 8 (the 3-layer)' : 'a loop of 24, through (' + o[0][0] + ', ' + o[0][1] + ')'; });
  var cls = orbits.map(function (o, i) { return o.length === 1 ? 'o-still' : o.length === 8 ? 'o-eight' : 'o-24-' + i; });
  var k24 = 0; cls = cls.map(function (c) { return /^o-24/.test(c) ? 'o-24' + String.fromCharCode(97 + k24++) : c; });
  var cells = {};
  var h = '<div class="st-corner"></div>';
  for (var j = 0; j < 9; j++) h += '<div class="st-head mono">' + j + '</div>';
  for (var i2 = 0; i2 < 9; i2++) {
    h += '<div class="st-head mono">' + i2 + '</div>';
    for (var j2 = 0; j2 < 9; j2++) h += '<button type="button" class="st-cell ' + cls[orbitOf[i2 + ',' + j2]] + '" data-s="' + i2 + ',' + j2 + '" aria-label="state (' + i2 + ', ' + j2 + ')"></button>';
  }
  grid.innerHTML = h;
  grid.querySelectorAll('.st-cell').forEach(function (c) { cells[c.getAttribute('data-s')] = c; c.addEventListener('click', function () { pick(c.getAttribute('data-s').split(',').map(Number)); }); });
  var sel = [0, 1], timer = null;
  function pick(s) {
    sel = s; var k = orbitOf[key(s)], o = orbits[k], start = o.findIndex(function (y) { return key(y) === key(s); });
    Object.keys(cells).forEach(function (kk) { cells[kk].classList.remove('on', 'here', 'anti'); cells[kk].textContent = ''; });
    o.forEach(function (y, n) { var c = cells[key(y)]; c.classList.add('on'); c.textContent = (n - start + o.length) % o.length; });
    cells[key(s)].classList.add('here');
    var anti = [mod(-s[0]), mod(-s[1])]; if (key(anti) !== key(s)) cells[key(anti)].classList.add('anti');
    var digits = []; for (var n = 0; n < o.length; n++) digits.push(o[(start + n) % o.length][0]);
    $('st-info').innerHTML = '<b>(' + s[0] + ', ' + s[1] + ')</b> lies on ' + names[k] + ', period <b>' + o.length + '</b>.<br>' +
      'Next, T(a, b) = (b, a + b): (' + T(s).join(', ') + ') · previous, T⁻¹(a, b) = (b − a, a): (' + Ti(s).join(', ') + ')<br>' +
      'Antipode, −(a, b): (' + anti.join(', ') + ')' + (o.length > 1 ? ', which is ' + (o.length / 2) + ' steps ahead, half the period' : ', the state itself') + '.<br>' +
      'First digits around the loop: <span class="mono">' + digits.join(' ') + '</span>';
  }
  $('st-step').addEventListener('click', function () { pick(T(sel)); });
  $('st-back').addEventListener('click', function () { pick(Ti(sel)); });
  $('st-play').addEventListener('click', function () {
    if (timer) { clearInterval(timer); timer = null; $('st-play').textContent = 'Play'; return; }
    $('st-play').textContent = 'Pause'; timer = setInterval(function () { pick(T(sel)); }, 700);
  });
  $('st-legend').innerHTML = orbits.map(function (o, i) { return '<span class="st-key ' + cls[i] + '"></span>' + names[i] + ' (' + o.length + ')'; }).join(' · ');
  pick([0, 1]);
})();
