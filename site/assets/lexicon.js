/* Ω42 Lexicon and Glossary: general meanings, protocol terms and the Lexicon of readings, searchable, side by side. */
(function () {
  var box = document.getElementById('lx'); if (!box) return;
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  var base = (window.O42 && O42.base) || '', G = null, L = null, tab = 'general';
  function norm(t) { return String(t).toLowerCase().replace(/^the /, '').replace(/ \(.*\)$/, ''); }
  function render() {
    if (!G || !L) return;
    var q = $('lx-q').value.trim().toLowerCase(), lexBy = {};
    L.entries.forEach(function (e) { lexBy[norm(e.term)] = e; });
    function hit(s) { return !q || s.toLowerCase().indexOf(q) >= 0; }
    var html = '', n = 0;
    if (tab === 'general') {
      G.general.forEach(function (e) {
        var lx = lexBy[norm(e.term)];
        if (!hit(e.term + ' ' + e.meaning + ' ' + e.domain)) return; n++;
        html += '<article class="lx-e" id="' + e.id + '"><h3>' + esc(e.term) + ' <span class="chip">' + esc(e.domain) + '</span> <span class="chip">established</span></h3><p>' + esc(e.meaning) + '</p>' +
          (lx ? '<div class="lx-cmp"><span class="k">In the Omega42 Lexicon (LX-' + ('00' + lx.n).slice(-3) + ', ' + esc(lx.status) + ')</span><p>' + esc(lx.definition) + '</p></div>' : '') +
          '<p class="note">' + e.id + ' · ' + esc(e.source) + '</p></article>';
      });
    } else if (tab === 'protocol') {
      G.protocol.forEach(function (e) {
        if (!hit(e.term + ' ' + e.definition)) return; n++;
        html += '<article class="lx-e" id="' + e.id + '"><h3>' + esc(e.term) + ' <span class="chip">' + esc(e.type) + '</span> <span class="chip">' + esc(e.status) + '</span></h3><p>' + esc(e.definition) + '</p><p class="note">' + e.id + ' · authority: ' + esc(e.authority) + ' · ' + esc(e.version) + '</p></article>';
      });
    } else {
      var f = $('lx-field').value;
      L.entries.forEach(function (e) {
        if (f && e.field !== f) return;
        if (!hit(e.term + ' ' + e.definition + ' ' + e.basis)) return; n++;
        html += '<article class="lx-e" id="LX-' + ('00' + e.n).slice(-3) + '"><h3>' + esc(e.term) + ' <span class="chip">' + esc(e.field) + '</span> <span class="chip">adapted · ' + esc(e.status) + '</span></h3><p>' + esc(e.definition) + '</p><p class="note">LX-' + ('00' + e.n).slice(-3) + ' · basis: ' + esc(e.basis) + ' · coordinate: ' + esc(e.coordinate) + '</p></article>';
      });
    }
    $('lx-list').innerHTML = html || '<p class="note">No term matches.</p>';
    $('lx-count').textContent = n + ' shown';
    $('lx-field').hidden = tab !== 'lexicon';
  }
  document.querySelectorAll('[data-tab]').forEach(function (b) { b.addEventListener('click', function () {
    tab = b.getAttribute('data-tab'); document.querySelectorAll('[data-tab]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); render(); }); });
  $('lx-q').addEventListener('input', render); $('lx-field').addEventListener('change', render);
  Promise.all([fetch(base + 'api/glossary.json').then(function (r) { return r.json(); }), fetch(base + 'api/lexicon.json').then(function (r) { return r.json(); })]).then(function (r) {
    G = r[0]; L = r[1];
    var fields = {}; L.entries.forEach(function (e) { fields[e.field] = 1; });
    $('lx-field').innerHTML = '<option value="">All fields</option>' + Object.keys(fields).sort().map(function (f) { return '<option>' + esc(f) + '</option>'; }).join('');
    $('lx-n-g').textContent = G.general.length; $('lx-n-p').textContent = G.protocol.length; $('lx-n-l').textContent = L.entries.length;
    var h = location.hash.slice(1); if (/^OT-/.test(h)) tab = 'protocol'; else if (/^LX-/.test(h)) tab = 'lexicon';
    document.querySelectorAll('[data-tab]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-tab') === tab)); });
    render(); if (h && document.getElementById(h)) document.getElementById(h).scrollIntoView();
  }).catch(function () { $('lx-list').innerHTML = '<p class="note">The definitions could not be loaded.</p>'; });
})();
