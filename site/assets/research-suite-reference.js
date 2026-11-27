/* Omega42 Research Suite kernel, version 1 (27 November 2026). Claude, Mathematical Research and Statistics.
 *
 * The shared mathematics behind the eight instruments of the Research Suite (site/pages/research-suite.html), each
 * function named by the OmegaSL operation it implements and by the register entry it computes. Integers only; no
 * randomness except a seeded generator for sample memories. Checked against an independent Python recomputation by
 * records/osl/suite_check.py, which must exit 0 before a release. Browser: window.Omega42Suite; Node: module.exports.
 *
 *   World W_k = (Z/3^k)^2, law A = [[0,1],[1,1]], A^t = [[F(t-1), F(t)], [F(t), F(t+1)]], order N_k = 8*3^(k-1).
 *   Native reading at phase t: (F(t-1) a + F(t) b mod 3^k) mod 7.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Omega42Suite = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var VERSION = '1';
  var mod = function (n, q) { return ((n % q) + q) % q; };
  function depth(k, lo, hi) { if (!(k === Math.floor(k) && k >= lo && k <= hi)) throw new RangeError('depth must be ' + lo + '..' + hi); return Math.pow(3, k); }
  function order(k) { return 8 * Math.pow(3, k - 1); }
  function v3(n, k) { var q = Math.pow(3, k); n = mod(n, q); if (n === 0) return k; var e = 0; while (n % 3 === 0) { n /= 3; e++; } return e; }
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }

  /* F(t) mod q for t = 0..n+1, with F(-1) = 1 stored as P[0]: P[t] = F(t-1), R[t] = F(t). */
  function fibRows(k, n) {
    var q = Math.pow(3, k), P = new Int32Array(n), R = new Int32Array(n), p = 1, r = 0;
    for (var t = 0; t < n; t++) { P[t] = p; R[t] = r; var s = (p + r) % q; p = r; r = s; }
    return { P: P, R: R };
  }
  function readingArray(k, t, rows) {
    var q = Math.pow(3, k), n = q * q, out = new Uint8Array(n), p = rows.P[t], r = rows.R[t];
    for (var a = 0, i = 0; a < q; a++) { var pa = (p * a) % q; for (var b = 0; b < q; b++, i++) out[i] = ((pa + r * b) % q) % 7; }
    return out;
  }

  /* ---------- Observation (OBS.PARTITION, OBS.COMPLETE, OBS.DESCEND; MF-201, MF-207/208, MF-214, MF-217, MF-221) ---------- */
  function bound(k) { return Math.ceil(k * Math.log(9) / Math.log(7) - 1e-12); }
  /* Class label of every state after the readings at the phases (labels 0..C-1, in order of first appearance). */
  function labels(phases, k) {
    var q = depth(k, 1, 6), n = q * q, N = order(k), rows = fibRows(k, N), lab = new Int32Array(n), C = 1;
    phases.forEach(function (t) {
      t = mod(t, N); var r = readingArray(k, t, rows), map = new Map(), nl = new Int32Array(n);
      for (var i = 0; i < n; i++) { var key = lab[i] * 7 + r[i], v = map.get(key); if (v === undefined) { v = map.size; map.set(key, v); } nl[i] = v; }
      lab = nl; C = map.size;
    });
    return { labels: lab, classes: C };
  }
  function partition(phases, k) {
    var L = labels(phases, k), cnt = new Int32Array(L.classes); for (var i = 0; i < L.labels.length; i++) cnt[L.labels[i]]++;
    var hist = {}, pairs = 0, max = 0;
    for (var c = 0; c < cnt.length; c++) { hist[cnt[c]] = (hist[cnt[c]] || 0) + 1; pairs += cnt[c] * (cnt[c] - 1) / 2; if (cnt[c] > max) max = cnt[c]; }
    return { states: L.labels.length, classes: L.classes, histogram: hist, pairs: pairs, largest: max, separates: pairs === 0, bound: bound(k) };
  }
  /* Selective aperture completion (MF-221): after the fixed phases, for each ambiguous class the least phase in the pool
     that separates it completely. */
  function complete(phases, k, pool) {
    var L = labels(phases, k), n = L.labels.length, N = order(k), rows = fibRows(k, N), cnt = new Int32Array(L.classes);
    for (var i = 0; i < n; i++) cnt[L.labels[i]]++;
    var done = new Int8Array(L.classes), chosen = new Int32Array(L.classes).fill(-1);
    for (var c = 0; c < L.classes; c++) if (cnt[c] === 1) done[c] = 1;
    pool.forEach(function (t) {
      var r = readingArray(k, mod(t, N), rows), seen = new Map(), distinct = new Int32Array(L.classes);
      for (var i = 0; i < n; i++) { var c = L.labels[i]; if (done[c]) continue; var key = c * 7 + r[i]; if (!seen.has(key)) { seen.set(key, 1); distinct[c]++; } }
      for (var c2 = 0; c2 < L.classes; c2++) if (!done[c2] && distinct[c2] === cnt[c2]) { done[c2] = 1; chosen[c2] = t; }
    });
    var amb = 0, unresolved = 0, extra = 0, used = {};
    for (var c3 = 0; c3 < L.classes; c3++) if (cnt[c3] > 1) { amb++; extra += cnt[c3]; if (chosen[c3] < 0) unresolved++; else used[chosen[c3]] = (used[chosen[c3]] || 0) + 1; }
    return { ambiguous: amb, unresolved: unresolved, completionPhases: used, distinctPhases: Object.keys(used).length,
             mean: (phases.length * n + extra) / n, worst: phases.length + (amb ? 1 : 0) };
  }
  /* The adaptive greedy observer (MF-217): each class takes the phase whose readings leave its largest part smallest. */
  function adaptive(k, maxRounds) {
    var q = depth(k, 1, 5), n = q * q, N = order(k), rows = fibRows(k, N), lab = new Int32Array(n), C = 1, rounds = 0, trace = [];
    var R = []; for (var t = 0; t < N; t++) R.push(readingArray(k, t, rows));
    while (rounds < (maxRounds || 12)) {
      var size = new Int32Array(C); for (var i = 0; i < n; i++) size[lab[i]]++;
      var mx = 0; for (var c = 0; c < C; c++) if (size[c] > mx) mx = size[c];
      trace.push(mx); if (mx <= 1) break;
      var best = new Int32Array(C).fill(n + 1), bp = new Int32Array(C), h = new Int32Array(C * 7);
      for (var t2 = 0; t2 < N; t2++) {
        h.fill(0); var r = R[t2]; for (var i2 = 0; i2 < n; i2++) h[lab[i2] * 7 + r[i2]]++;
        for (var c2 = 0; c2 < C; c2++) { var m = 0; for (var s = 0; s < 7; s++) if (h[c2 * 7 + s] > m) m = h[c2 * 7 + s]; if (m < best[c2]) { best[c2] = m; bp[c2] = t2; } }
      }
      var map = new Map(), nl = new Int32Array(n);
      for (var i3 = 0; i3 < n; i3++) { var key = lab[i3] * 7 + R[bp[lab[i3]]][i3], v = map.get(key); if (v === undefined) { v = map.size; map.set(key, v); } nl[i3] = v; }
      lab = nl; C = map.size; rounds++;
    }
    return { readings: rounds, bound: bound(k), attains: rounds === bound(k), largestClassAfterEachReading: trace };
  }
  /* Separation descent (Lemma 5.9): a team that separates W_k separates W_(k-1) with the same phases mod N_(k-1). */
  function descend(phases, k) {
    var here = partition(phases, k), below = k > 1 ? partition(phases.map(function (t) { return mod(t, order(k - 1)); }), k - 1) : null;
    return { here: here, below: below, consistent: !here.separates || !below || below.separates };
  }

  /* ---------- Memory (MEM.LIFT, MEM.EXTINCTION, MEM.INVARIANT; MF-197, MF-198, MF-220) ---------- */
  function orbits(k) {
    var q = Math.pow(3, k), seen = new Uint8Array(q * q), out = [];
    for (var i = 0; i < q * q; i++) if (!seen[i]) { var a = Math.floor(i / q), b = i % q, o = []; while (!seen[a * q + b]) { seen[a * q + b] = 1; o.push(a * q + b); var t = (a + b) % q; a = b; b = t; } out.push(o); }
    return out;
  }
  function orbitSums(g, k) { var q = Math.pow(3, k); return orbits(k).map(function (o) { return o.reduce(function (s, i) { return (s + g[i]) % q; }, 0); }); }
  /* g' = 3 g o pi: the memory at depth k + 1 that reads the parent state's memory and multiplies by 3 (Theorem 20.1). */
  function lift(g, k) { var q = Math.pow(3, k), Q = 3 * q, out = new Int32Array(Q * Q); for (var a = 0; a < Q; a++) for (var b = 0; b < Q; b++) out[a * Q + b] = (3 * g[(a % q) * q + (b % q)]) % Q; return out; }
  function sampleMemory(k, seed) { var q = Math.pow(3, k), x = seed >>> 0 || 1, g = new Int32Array(q * q); for (var i = 0; i < g.length; i++) { x = (Math.imul(x, 1103515245) + 12345) >>> 0; g[i] = (x >>> 8) % q; } return g; }
  function extinctionDepth(W, k) { W = mod(W, Math.pow(3, k)); return W === 0 ? 0 : k - v3(W, k); }
  function invariant(s, k) { var q = Math.pow(3, k); s = mod(s, q); var d = gcd(s, q) || q; return { num: s / d, den: q / d, text: s === 0 ? '0' : (s / d) + '/' + (q / d) }; }
  /* The trajectory of one moving sum W and the still value s over a number of lifts, by the laws of Proposition 20.11. */
  function trajectory(W, s, k, lifts) {
    if (!(k >= 1 && lifts >= 0 && k + lifts <= 16)) throw new RangeError("depth plus lifts must be at most 16");
    var rows = [];
    for (var j = 0; j <= lifts; j++) { var q = Math.pow(3, k + j), w = mod(Math.pow(9, j) % q * mod(W, Math.pow(3, k)), q), sv = mod(Math.pow(3, j) * mod(s, Math.pow(3, k)), q);
      rows.push({ lift: j, depth: k + j, moving: w, still: sv, invariant: invariant(sv, k + j).text }); }
    return { rows: rows, extinction: extinctionDepth(W, k), invariant: invariant(s, k).text };
  }
  /* Exact check of Proposition 20.11 on a sample memory: after j >= k lifts, the orbit sums equal those of the memory that
     keeps only the still-point value; the still value is 3^j s. */
  function verifyMemory(k, seed, lifts) {
    var g = sampleMemory(k, seed), s = g[0], h = new Int32Array(g.length); h[0] = s; var ok = true, log = [];
    for (var j = 1; j <= lifts; j++) {
      g = lift(g, k + j - 1); h = lift(h, k + j - 1); var A = orbitSums(g, k + j), B = orbitSums(h, k + j), same = A.join() === B.join();
      var stillOk = g[0] === (Math.pow(3, j) * s) % Math.pow(3, k + j); ok = ok && stillOk && (j < k || same);
      log.push({ lift: j, depth: k + j, orbits: A.length, nonzeroSums: A.filter(Boolean).length, dependsOnStillOnly: same, stillValue: g[0] });
    }
    return { pass: ok, s: s, log: log };
  }

  /* ---------- Spectrum (SPEC.PROJECT; MF-218, the golden split of the law) ---------- */
  var PHI = (1 + Math.sqrt(5)) / 2, PSI = -1 / PHI;
  /* A = phi P+ + psi P-, with P+ = (A - psi I)/sqrt5 and P- = (phi I - A)/sqrt5; A^n = F(n) A + F(n-1) I exactly. */
  function project(v) { var r5 = Math.sqrt(5), Av = [v[1], v[0] + v[1]];
    var plus = [(Av[0] - PSI * v[0]) / r5, (Av[1] - PSI * v[1]) / r5], minus = [(PHI * v[0] - Av[0]) / r5, (PHI * v[1] - Av[1]) / r5];
    return { plus: plus, minus: minus }; }
  function channel(v, steps) {
    var pr = project(v), out = [], F0 = 0, F1 = 1, Fm = 1;     /* F(n-1), F(n) */
    for (var n = 0; n <= steps; n++) {
      var exact = [Fm * v[0] + F0 * v[1], F0 * v[0] + (Fm + F0) * v[1]];
      out.push({ n: n, exact: exact, plus: Math.pow(PHI, n) * Math.hypot(pr.plus[0], pr.plus[1]), minus: Math.pow(Math.abs(PSI), n) * Math.hypot(pr.minus[0], pr.minus[1]) });
      var t = Fm + F0; Fm = F0; F0 = t;
    }
    return { phi: PHI, psi: PSI, projection: pr, steps: out };
  }

  /* ---------- Design and geometry (DESIGN.RING; MF-219) ---------- */
  function inverse(x, q) { for (var i = 1; i < q; i++) if ((x * i) % q === 1) return i; throw new RangeError('not a unit'); }
  function normalize(d, q) { return d[0] % 3 ? [1, (d[1] * inverse(d[0], q)) % q] : [(d[0] * inverse(d[1], q)) % q, 1]; }
  /* The 4*3^(k-1) directions in the order the law visits them, starting from (1, 0). */
  function directions(k) { var q = depth(k, 1, 4), out = [], d = [1, 0]; do { out.push(d); d = normalize([d[1], (d[0] + d[1]) % q], q); } while (d.join() !== '1,0' && out.length <= 4 * q); return out; }
  /* Round r: the parallel class of lines x + t d; each group is a line of q states, given as indices a*q + b. */
  function round(k, r) {
    var q = Math.pow(3, k), d = directions(k)[r], seen = new Uint8Array(q * q), groups = [];
    for (var i = 0; i < q * q; i++) if (!seen[i]) { var a = Math.floor(i / q), b = i % q, g = []; for (var t = 0; t < q; t++) { var j = ((a + t * d[0]) % q) * q + (b + t * d[1]) % q; seen[j] = 1; g.push(j); } groups.push(g); }
    return { direction: d, groups: groups };
  }
  function schedule(k) { return directions(k).map(function (_, r) { return round(k, r); }); }
  function valuation(x, y, k) { var q = Math.pow(3, k); return Math.min(v3(x[0] - y[0], k), v3(x[1] - y[1], k)); }
  /* Certificate: every round partitions W_k into q groups of q; two distinct states meet in exactly 3^r rounds. */
  function verifyDesign(k) {
    var q = depth(k, 1, 3), S = schedule(k), ok = S.length === 4 * Math.pow(3, k - 1), meet = new Map();
    S.forEach(function (R) { var cover = new Uint8Array(q * q); ok = ok && R.groups.length === q;
      R.groups.forEach(function (g) { g.forEach(function (i) { cover[i]++; }); for (var u = 0; u < g.length; u++) for (var w = u + 1; w < g.length; w++) { var key = Math.min(g[u], g[w]) * q * q + Math.max(g[u], g[w]); meet.set(key, (meet.get(key) || 0) + 1); } });
      ok = ok && cover.every(function (c) { return c === 1; }); });
    var pairs = 0;
    for (var i = 0; i < q * q; i++) for (var j = i + 1; j < q * q; j++) { pairs++; var r = valuation([Math.floor(i / q), i % q], [Math.floor(j / q), j % q], k); if ((meet.get(i * q * q + j) || 0) !== Math.pow(3, r)) ok = false; }
    return { pass: ok, rounds: S.length, groupsPerRound: q, pairs: pairs };
  }

  /* ---------- Adaptors (ADAPT.DEFECT, ADAPT.COMPOSE; lexicon 127 and 128) ---------- */
  function circ(x, n) { x = mod(x, n); return Math.min(x, n - x); }
  /* Cyclic compatibility: a cycle of length n is a native factor at depth k exactly when n | 8*3^(k-1). */
  function compatibility(n, k) {
    var N = order(k), factor = N % n === 0, least = null;
    for (var j = 1; j <= 12; j++) if (order(j) % n === 0) { least = j; break; }
    return { n: n, N: N, factor: factor, leastDepth: least };
  }
  /* The adaptor E(t) = t mod n from the native cycle Z/N (T: t -> t+1) to Z/n (U: s -> s+1): its defect
     max_t d(E(Tt), U(E t)) in the circular metric, and the number of phases where it is nonzero. */
  function defect(N, n) { var worst = 0, bad = 0; for (var t = 0; t < N; t++) { var d = circ(((t + 1) % N) % n - ((t % n) + 1), n); if (d) { bad++; if (d > worst) worst = d; } } return { defect: worst, phases: bad, exact: worst === 0 }; }
  /* Composition Z/N -> Z/n1 -> Z/n2 by reductions: the composite defect and the bound L*d1 + d2 with L = 1. */
  function compose(N, n1, n2) {
    var d1 = defect(N, n1), d2 = defect(n1, n2), worst = 0;
    for (var t = 0; t < N; t++) { var d = circ((((t + 1) % N) % n1) % n2 - (((t % n1) % n2) + 1), n2); if (d > worst) worst = d; }
    return { first: d1.defect, second: d2.defect, composite: worst, bound: d1.defect + d2.defect, withinBound: worst <= d1.defect + d2.defect };
  }

  /* ---------- Navigation (GEN.DISTANCE, GEN.MINSET; MF-209 to MF-212) ---------- */
  var OPS = { A: function (a, b, q) { return [b, (a + b) % q]; }, V: function (a, b, q) { return [(2 * a) % q, (2 * b) % q]; },
              C: function (a, b, q) { return [(3 * a) % q, (3 * b) % q]; }, S: function (a, b, q) { return [a, (3 * a + b) % q]; } };
  function navigate(ops, k, target) {
    var q = depth(k, 1, 6), n = q * q, dist = new Int32Array(n).fill(-1), via = new Int32Array(n).fill(-1), by = new Int8Array(n), queue = new Int32Array(n), head = 0, tail = 0, seed = (2 % q) * q + 5 % q, ecc = 0;
    dist[seed] = 0; queue[tail++] = seed;
    while (head < tail) { var i = queue[head++], a = Math.floor(i / q), b = i % q;
      for (var o = 0; o < ops.length; o++) { var y = OPS[ops[o]](a, b, q), j = y[0] * q + y[1]; if (dist[j] < 0) { dist[j] = dist[i] + 1; via[j] = i; by[j] = o; if (dist[j] > ecc) ecc = dist[j]; queue[tail++] = j; } } }
    var route = null;
    if (target) { var t = (mod(target[0], q)) * q + mod(target[1], q); if (dist[t] >= 0) { route = []; while (t !== seed) { route.push(ops[by[t]]); t = via[t]; } route.reverse(); } }
    return { reached: tail, states: n, generates: tail === n, eccentricity: ecc, route: route, routeWord: route ? route.join('') : null };
  }
  function compareSets(k) { var sets = []; for (var m = 1; m < 16; m++) { var s = ''; 'AVCS'.split('').forEach(function (c, i) { if (m & (1 << i)) s += c; }); var r = navigate(s, k); sets.push({ ops: s, reached: r.reached, generates: r.generates, eccentricity: r.generates ? r.eccentricity : null }); } return sets; }
  function lowerBound(k) { return Math.ceil(Math.log2(8 * Math.pow(9, k - 1) + 1)) - 1; }

  /* ---------- Discovery (exploration over moduli; results are hypotheses until registered) ---------- */
  function pisano(m) { var a = 0, b = 1 % m, n = 0; do { var t = (a + b) % m; a = b; b = t; n++; } while (!(a === 0 && b === 1 % m)); return n; }
  function orbitCount(m) { var seen = new Uint8Array(m * m), c = 0; for (var i = 0; i < m * m; i++) if (!seen[i]) { c++; var a = Math.floor(i / m), b = i % m; while (!seen[a * m + b]) { seen[a * m + b] = 1; var t = (a + b) % m; a = b; b = t; } } return c; }
  var PROPERTIES = {
    'period divides 24': function (m, p) { return 24 % p === 0; },
    'period equals 6m': function (m, p) { return p === 6 * m; },
    'period equals m - 1 or a divisor of it': function (m, p) { return (m - 1) % p === 0; },
    'period divides 2(m + 1)': function (m, p) { return (2 * (m + 1)) % p === 0; },
    'period is a native factor (divides 8*3^j)': function (m, p) { while (p % 3 === 0) p /= 3; return 8 % p === 0; }
  };
  function explore(lo, hi, property) {
    var f = PROPERTIES[property]; if (!f) throw new RangeError('unknown property');
    var rows = [], hits = [];
    for (var m = Math.max(2, lo); m <= hi; m++) { var p = pisano(m), r = { m: m, period: p, orbits: orbitCount(m), holds: f(m, p) }; rows.push(r); if (r.holds) hits.push(m); }
    return { property: property, rows: rows, hits: hits };
  }

  return { VERSION: VERSION, order: order, bound: bound, v3: v3, partition: partition, complete: complete, adaptive: adaptive, descend: descend,
           orbits: orbits, orbitSums: orbitSums, lift: lift, sampleMemory: sampleMemory, extinctionDepth: extinctionDepth, invariant: invariant,
           trajectory: trajectory, verifyMemory: verifyMemory, project: project, channel: channel, directions: directions, round: round,
           schedule: schedule, valuation: valuation, verifyDesign: verifyDesign, compatibility: compatibility, defect: defect, compose: compose,
           navigate: navigate, compareSets: compareSets, lowerBound: lowerBound, pisano: pisano, orbitCount: orbitCount,
           PROPERTIES: Object.keys(PROPERTIES), explore: explore };
}));
