/* The doorway: the Omega42 emblem, driven by the law itself.
   The point of light follows the canonical cycle generated here from the seeds (2, 5) by (a, b) -> (b, a + b mod 9);
   residue 0 is drawn at 9. One 30-second performance: Genesis (0-3 s), Formation (3-6 s), Generation (phases 0-11, 6-18 s),
   Reflection (phases 12-23, 18-30 s: A^12 = -I, every state meets its negative), then Renewal. Runs in the browser only. */
(function () {
  var root = document.querySelector('.doorway'); if (!root) return;
  var svg = root.querySelector('.doorway-svg'), walker = svg.querySelector('.dw-walker'), trail = svg.querySelector('.dw-trail');
  var phaseEl = root.querySelector('.dw-phase'), stateEl = root.querySelector('.dw-state'), actEl = root.querySelector('.dw-act');
  var pauseB = root.querySelector('.dw-pause'), soundB = root.querySelector('.dw-sound');
  var NS = 'http://www.w3.org/2000/svg', C = 200, R = 150;
  function pt(d) { var a = (40 * (d % 9) - 90) * Math.PI / 180; return [C + R * Math.cos(a), C + R * Math.sin(a)]; }
  var seq = [], s = [2, 5];
  for (var i = 0; i < 24; i++) { seq.push(s.slice()); s = [s[1], (s[0] + s[1]) % 9]; }
  var digit = function (st) { return st[0] === 0 ? 9 : st[0]; };
  var nodes = {}; svg.querySelectorAll('.dw-nodes g').forEach(function (g) { nodes[g.getAttribute('data-d')] = g; });
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var paused = false, t0 = performance.now(), held = 0, lastPhase = -1, ctx = null, sound = false;
  function stage(name) { if (root.getAttribute('data-stage') !== name) { root.setAttribute('data-stage', name); actEl.textContent = name; } }
  function tone(st) {
    if (!sound) return;
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      var o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime;
      o.frequency.value = 220 * Math.pow(2, st[0] / 9); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.025, t + .04); g.gain.linearRampToValueAtTime(0, t + .6);
      o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + .65);
    } catch (e) { sound = false; }
  }
  function clearTrail() { while (trail.firstChild) trail.removeChild(trail.firstChild); }
  function seg(p, q, half) { var l = document.createElementNS(NS, 'line'); l.setAttribute('x1', p[0]); l.setAttribute('y1', p[1]); l.setAttribute('x2', q[0]); l.setAttribute('y2', q[1]); l.setAttribute('class', half ? 'dw-seg b' : 'dw-seg a'); trail.appendChild(l); }
  function arrive(k) {
    var st = seq[k], d = digit(st);
    Object.keys(nodes).forEach(function (n) { nodes[n].classList.remove('lit'); });
    nodes[d].classList.add('lit');
    phaseEl.textContent = 'phase ' + k; stateEl.textContent = 'state (' + st[0] + ', ' + st[1] + ')';
    if (k > 0) seg(pt(digit(seq[k - 1])), pt(d), k > 12);
    if (k === 12) root.classList.add('antipode');
    tone(st);
  }
  function frame(now) {
    if (!paused) {
      var t = ((now - t0 - held) / 1000) % 30;
      if (t < 3) { stage('Genesis'); root.classList.remove('antipode'); if (lastPhase !== -1) { clearTrail(); lastPhase = -1; } walker.style.opacity = 0; }
      else if (t < 6) { stage('Formation'); walker.style.opacity = 0; }
      else {
        stage(t < 18 ? 'Generation' : 'Reflection');
        var x = t - 6, k = Math.min(23, Math.floor(x)), f = Math.min(1, (x - k) / .45);
        f = f < .5 ? 2 * f * f : 1 - Math.pow(-2 * f + 2, 2) / 2;
        var a = pt(digit(seq[k])), b = pt(digit(seq[(k + 1) % 24]));
        walker.style.opacity = 1;
        walker.setAttribute('cx', a[0] + (b[0] - a[0]) * f); walker.setAttribute('cy', a[1] + (b[1] - a[1]) * f);
        if (k !== lastPhase) { if (k < lastPhase) clearTrail(); for (var j = lastPhase + 1; j <= k; j++) arrive(j); lastPhase = k; }
      }
    }
    requestAnimationFrame(frame);
  }
  var pausedAt = 0;
  pauseB.addEventListener('click', function () {
    paused = !paused;
    if (paused) pausedAt = performance.now(); else held += performance.now() - pausedAt;
    root.classList.toggle('paused', paused); pauseB.setAttribute('aria-pressed', paused); pauseB.textContent = paused ? '▶ play' : '❚❚ pause';
  });
  soundB.addEventListener('click', function () {
    sound = !sound; soundB.setAttribute('aria-pressed', sound); soundB.textContent = sound ? '♪ tones on' : '♪ tones off';
    if (!sound && ctx) { ctx.close(); ctx = null; }
  });
  document.addEventListener('visibilitychange', function () { if (document.hidden && ctx) { ctx.close(); ctx = null; } });
  if (reduce) {   // a still, complete figure: the whole cycle drawn, no moving light
    root.setAttribute('data-stage', 'Still'); actEl.textContent = 'the whole canonical cycle';
    for (var k = 1; k < 24; k++) seg(pt(digit(seq[k - 1])), pt(digit(seq[k])), k > 12);
    walker.style.opacity = 0; pauseB.hidden = true; return;
  }
  requestAnimationFrame(frame);
})();
