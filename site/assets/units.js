/* Ω42 measurement converter: SI and back, from the unit table in api/units.json (records/units/units.json).
   Every result shows its formula and the definitions used. Runs on the device; nothing is sent anywhere. */
(function () {
  var root = document.getElementById('conv'); if (!root) return;
  var $ = function (id) { return document.getElementById(id); };
  var Q = [], cur = null;
  function num(s) {
    s = String(s).replace(/pi/g, String(Math.PI));
    if (/^[0-9.eE+\-]+\/[0-9.eE+\-]+$/.test(s)) { var p = s.split('/'); return parseFloat(p[0]) / parseFloat(p[1]); }
    if (/^2\*/.test(s)) return 2 * parseFloat(s.slice(2));
    if (/\//.test(s)) { var q = s.split('/'); return parseFloat(q[0]) / parseFloat(q[1]); }
    return parseFloat(s);
  }
  function fmt(x, sig) {
    if (!isFinite(x)) return '—';
    if (x === 0) return '0';
    var a = Math.abs(x);
    var s = (a >= 1e-4 && a < 1e12) ? String(parseFloat(x.toPrecision(sig))) : x.toExponential(sig - 1).replace('e+', ' × 10^').replace('e-', ' × 10^-');
    return s;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  function fill() {
    cur = Q[$('c-q').value];
    var opts = cur.units.map(function (u, i) { return '<option value="' + i + '">' + esc(u[1]) + ' (' + esc(u[0]) + ')</option>'; }).join('');
    $('c-from').innerHTML = opts; $('c-to').innerHTML = opts;
    $('c-from').value = cur.units.length > 1 ? String(Math.min(6, cur.units.length - 1)) : '0'; $('c-to').value = '0';
    run();
  }
  function run() {
    var x = parseFloat(String($('c-x').value).replace(',', '.')), sig = +$('c-sig').value;
    var a = cur.units[+$('c-from').value], b = cur.units[+$('c-to').value], out, steps;
    if (isNaN(x)) { $('c-out').textContent = 'Enter a number'; $('c-math').innerHTML = ''; return; }
    if (cur.affine) {
      var sa = num(a[2]), oa = num(a[3]), sb = num(b[2]), ob = num(b[3]);
      var K = (x + oa) * sa; out = K / sb - ob;
      steps = 'Temperature needs an offset, not only a factor.<br>Into kelvin: K = (' + x + ' + ' + a[3] + ') × ' + a[2] + ' = ' + fmt(K, 15) + ' K<br>Out of kelvin: ' + esc(b[0]) + ' = K ÷ ' + b[2] + ' − ' + b[3] + ' = <b>' + fmt(out, 15) + '</b>';
      steps += '<br>Definitions: ' + esc(a[1]) + ': ' + esc(a[4]) + '; ' + esc(b[1]) + ': ' + esc(b[4]) + '.';
    } else {
      var fa = num(a[2]), fb = num(b[2]); out = x * fa / fb;
      steps = 'Into ' + esc(cur.si) + ': ' + x + ' ' + esc(a[0]) + ' × ' + esc(a[2]) + ' = ' + fmt(x * fa, 15) + ' ' + esc(cur.si) +
        '<br>Out of ' + esc(cur.si) + ': ÷ ' + esc(b[2]) + ' = <b>' + fmt(out, 15) + ' ' + esc(b[0]) + '</b>' +
        '<br>One ' + esc(a[1]) + ' = ' + fmt(fa / fb, 15) + ' ' + esc(b[0]) + '.' +
        '<br>Definitions: ' + esc(a[1]) + ' = ' + esc(a[3]) + '; ' + esc(b[1]) + ' = ' + esc(b[3]) + '.';
    }
    $('c-out').innerHTML = '<b>' + fmt(out, sig) + '</b> ' + esc(b[1]) + ' <span class="mono">(' + esc(b[0]) + ')</span>';
    $('c-math').innerHTML = steps;
  }
  fetch((window.O42 && O42.base || '') + 'api/units.json').then(function (r) { return r.json(); }).then(function (t) {
    Q = t.quantities;
    $('c-q').innerHTML = Q.map(function (q, i) { return '<option value="' + i + '">' + esc(q.q) + ' (SI: ' + esc(q.si) + ')</option>'; }).join('');
    $('c-q').value = '0'; fill();
    $('c-pre').innerHTML = t.prefixes.map(function (p) { return '<tr><td class="mono">' + esc(p[0]) + '</td><td>' + esc(p[1]) + '</td><td class="mono">10^' + p[2] + '</td></tr>'; }).join('');
    ['c-x', 'c-sig', 'c-from', 'c-to'].forEach(function (id) { $(id).addEventListener('input', run); $(id).addEventListener('change', run); });
    $('c-q').addEventListener('change', fill);
    $('c-swap').addEventListener('click', function () { var f = $('c-from').value; $('c-from').value = $('c-to').value; $('c-to').value = f; run(); });
    $('c-copy').addEventListener('click', function () { var t2 = $('c-out').textContent + '\n' + $('c-math').textContent; if (navigator.clipboard) navigator.clipboard.writeText(t2); $('c-copy').textContent = 'Copied'; setTimeout(function () { $('c-copy').textContent = 'Copy result and working'; }, 1500); });
  }).catch(function () { $('c-out').textContent = 'The unit table could not be loaded.'; });
})();
