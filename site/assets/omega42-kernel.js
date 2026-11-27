/* Omega42 mathematical kernel, version 1 (27 November 2026). Claude, Mathematical Research Architect.
 *
 * One dependency-free module for every website instrument that computes. Each function implements a definition of
 * the paper (docs/OMEGA42_MATHEMATICAL_PAPER.md) and is checked against an independent Python recomputation by
 * records/osl/kernel_check.py, which must exit 0 before a release. Works in a browser (window.Omega42Kernel) and in
 * Node (module.exports). Pure functions; integers only; no randomness.
 *
 *   Notation (paper, Part I): the law A = [[0,1],[1,1]] acts on x = (a, b); the world at depth k is W_k = (Z/3^k)^2,
 *   with 9^k states; the canonical world is W_2 (81 states); Q(a, b) = a^2 + ab - b^2; the native aperture reads a mod 7.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Omega42Kernel = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var VERSION = '1';
  var mod = function (n, q) { return ((n % q) + q) % q; };
  var modulus = function (k) { if (!(k >= 1 && k <= 6 && k === Math.floor(k))) throw new RangeError('depth must be 1..6'); return Math.pow(3, k); };

  /* The world W_k, its states in the order (a, b) = (0,0), (0,1), ..., (q-1, q-1); index = a*q + b. */
  function states(k) { var q = modulus(k), out = []; for (var a = 0; a < q; a++) for (var b = 0; b < q; b++) out.push([a, b]); return out; }
  function index(x, k) { var q = modulus(k); return mod(x[0], q) * q + mod(x[1], q); }

  /* The law and its powers. step: (a, b) -> (b, a + b). power(x, n): A^n x, n any integer (A is invertible: det A = -1). */
  function step(x, q) { return [x[1], mod(x[0] + x[1], q)]; }
  function back(x, q) { return [mod(x[1] - x[0], q), x[0]]; }
  function matmul(M, N, q) { return [[mod(M[0][0] * N[0][0] + M[0][1] * N[1][0], q), mod(M[0][0] * N[0][1] + M[0][1] * N[1][1], q)],
                                     [mod(M[1][0] * N[0][0] + M[1][1] * N[1][0], q), mod(M[1][0] * N[0][1] + M[1][1] * N[1][1], q)]]; }
  function matpow(n, q) {               /* A^n mod q for n >= 0, by squaring */
    var R = [[1 % q, 0], [0, 1 % q]], B = [[0, 1], [1, 1 % q]];
    while (n > 0) { if (n & 1) R = matmul(R, B, q); B = matmul(B, B, q); n = Math.floor(n / 2); }
    return R;
  }
  function power(x, n, k) {
    var q = modulus(k), N = order(k), M = matpow(mod(n, N), q);
    return [mod(M[0][0] * x[0] + M[0][1] * x[1], q), mod(M[1][0] * x[0] + M[1][1] * x[1], q)];
  }
  /* The order of A on W_k: 8 * 3^(k-1) (paper, Theorem 3.1). */
  function order(k) { modulus(k); return 8 * Math.pow(3, k - 1); }
  /* The order of A modulo any m >= 2 (the Pisano period of m); 24 for m = 9, 16 for m = 7, 10 for m = 11. */
  function orderMod(m) {
    if (!(m >= 2 && m === Math.floor(m))) throw new RangeError('modulus must be an integer >= 2');
    var a = 0, b = 1 % m, n = 0;
    do { var t = (a + b) % m; a = b; b = t; n++; } while (!(a === 0 && b === 1 % m) && n <= 6 * m);
    return n;
  }

  /* Orbits. orbit(x, k): the states x, Ax, A^2 x, ... until return. census(k): orbit lengths with their counts. */
  function orbit(x, k) { var q = modulus(k), s = [mod(x[0], q), mod(x[1], q)], o = [s], y = step(s, q);
    while (y[0] !== s[0] || y[1] !== s[1]) { o.push(y); y = step(y, q); } return o; }
  function period(x, k) { return orbit(x, k).length; }
  function orbits(k) {
    var q = modulus(k), seen = new Uint8Array(q * q), out = [];
    for (var i = 0; i < q * q; i++) if (!seen[i]) { var o = orbit([Math.floor(i / q), i % q], k); o.forEach(function (y) { seen[y[0] * q + y[1]] = 1; }); out.push(o); }
    return out;
  }
  function census(k) { var c = {}; orbits(k).forEach(function (o) { c[o.length] = (c[o.length] || 0) + 1; }); return c; }

  /* The alternating form Q(a, b) = a^2 + ab - b^2 mod 3^k; Q(Ax) = -Q(x) (Theorem 2.3). */
  function Q(x, k) { var q = modulus(k); return mod(x[0] * x[0] + x[0] * x[1] - x[1] * x[1], q); }

  /* The canonical loop: first coordinates of the orbit of the seeds (2, 5) on W_2, residue 0 written as the digit 9. */
  function canonicalLoop() { return orbit([2, 5], 2).map(function (y) { return y[0] === 0 ? 9 : y[0]; }); }

  /* The native aperture: the reading at phase t of state x is (A^t x).a mod 7 (Theorem 5.2). */
  function read(x, t, k) { return power(x, t, k)[0] % 7; }
  function history(x, phases, k) { return phases.map(function (t) { return read(x, t, k); }); }
  /* separation(phases, k): the number of classes into which the readings at the given phases split W_k
     (k = 2: 7, 49, 73, 77, 80, 81 after phases 0..5 read in turn). */
  function separation(phases, k) { var seen = {}, n = 0; states(k).forEach(function (x) { var h = history(x, phases, k).join(','); if (!seen[h]) { seen[h] = 1; n++; } }); return n; }
  /* reconstruct(phases, values, k): every state whose readings at the phases equal the values. */
  function reconstruct(phases, values, k) {
    if (phases.length !== values.length) throw new RangeError('one value per phase');
    return states(k).filter(function (x) { return history(x, phases, k).every(function (v, i) { return v === values[i]; }); });
  }

  /* Generation: breadth-first reach from a seed under the operations
     A (the law), V (doubling), C (tripling), S (shear (a, b) -> (a, 3a + b)). Returns {reached, depth, distances}. */
  var OPS = { A: function (x, q) { return [x[1], mod(x[0] + x[1], q)]; }, V: function (x, q) { return [mod(2 * x[0], q), mod(2 * x[1], q)]; },
              C: function (x, q) { return [mod(3 * x[0], q), mod(3 * x[1], q)]; }, S: function (x, q) { return [x[0], mod(3 * x[0] + x[1], q)]; } };
  function reach(ops, k, seed) {
    var q = modulus(k); seed = seed || [2 % q, 5 % q];
    ops.split('').forEach(function (o) { if (!OPS[o]) throw new RangeError('unknown operation ' + o); });
    var dist = new Int32Array(q * q).fill(-1), queue = [seed], head = 0, deepest = 0;
    dist[seed[0] * q + seed[1]] = 0;
    while (head < queue.length) {
      var x = queue[head++], d = dist[x[0] * q + x[1]];
      for (var j = 0; j < ops.length; j++) { var y = OPS[ops[j]](x, q), i = y[0] * q + y[1];
        if (dist[i] < 0) { dist[i] = d + 1; if (d + 1 > deepest) deepest = d + 1; queue.push(y); } }
    }
    return { reached: queue.length, depth: deepest, distances: dist };
  }

  /* Harmonic multiplicities (Theorem 4.1): the multiplicity of the eigenvalue omega^j, omega = exp(2 pi i / N),
     N = order(k), of the shift on functions on W_k: the number of orbits of length L for which N/L divides j. */
  function multiplicities(k) {
    var N = order(k), m = new Array(N).fill(0);
    orbits(k).forEach(function (o) { var s = N / o.length; for (var j = 0; j < N; j += s) m[j]++; });
    return m;
  }

  /* The cat map (Theorem 8.1): A^2 = [[1, 1], [1, 2]]. */
  function catMap(x, k) { return power(x, 2, k); }

  return { VERSION: VERSION, modulus: modulus, states: states, index: index, step: step, back: back, power: power, order: order, orderMod: orderMod,
           orbit: orbit, period: period, orbits: orbits, census: census, Q: Q, canonicalLoop: canonicalLoop, read: read, history: history,
           separation: separation, reconstruct: reconstruct, reach: reach, multiplicities: multiplicities, catMap: catMap };
}));
