/* AD-008 Information transmission adaptor: native observation + Reed-Solomon over F7 (R-14 §4, R-15).
   The message is the state's native observation: the readings a mod 7 at phases (0, 2, 5) of depth 2 (Theorem 5.4).
   It is the value of a polynomial p, deg p < 3, at x = 0, 1, 2; the codeword is p(0..6). Minimum distance 5:
   two symbol errors are corrected. Uses Omega42Kernel.power when present, else its own step. */
(function (root) {
  'use strict';
  const PHASES = [0, 2, 5], Q = 9;
  function step(s) { return [s[1], (s[0] + s[1]) % Q]; }
  function at(s, n) {
    if (root.Omega42Kernel && root.Omega42Kernel.power) return root.Omega42Kernel.power(s, n, 2);
    let x = s.slice(); for (let i = 0; i < n; i++) x = step(x); return x;
  }
  function observe(a, b) { return PHASES.map(t => at([a, b], t)[0] % 7); }
  const inv7 = x => [0, 1, 4, 5, 2, 3, 6][x];
  function evalAt(m, x) {                    // Lagrange interpolation through (0, m0), (1, m1), (2, m2), at x
    let s = 0;
    for (let i = 0; i < 3; i++) {
      let num = 1, den = 1;
      for (let j = 0; j < 3; j++) if (j !== i) { num = (num * ((x - j + 7) % 7)) % 7; den = (den * ((i - j + 7) % 7)) % 7; }
      s = (s + m[i] * num * inv7(den)) % 7;
    }
    return s;
  }
  function encode(a, b) { const m = observe(a, b); return [0, 1, 2, 3, 4, 5, 6].map(x => evalAt(m, x)); }
  const BOOK = []; for (let a = 0; a < Q; a++) for (let b = 0; b < Q; b++) BOOK.push({ state: [a, b], word: encode(a, b) });
  function decode(r) {                       // nearest codeword among the 81; unique within distance 2
    let best = null, bd = 8;
    for (const e of BOOK) { const d = e.word.reduce((s, x, i) => s + (x !== r[i]), 0); if (d < bd) { bd = d; best = e; } }
    return bd <= 2 ? { state: best.state, readings: best.word.slice(0, 3), errors: bd } : null;
  }
  function certify() {                       // every state, every single and double error
    let ok = new Set(BOOK.map(e => e.word.join(''))).size === 81, n = 0;
    for (const e of BOOK) {
      for (let i = 0; i < 7; i++) for (let j = i; j < 7; j++) for (let u = 1; u < 7; u++) for (let v = (i === j ? 0 : 1); v < (i === j ? 1 : 7); v++) {
        const r = e.word.slice(); r[i] = (r[i] + u) % 7; if (i !== j) r[j] = (r[j] + v) % 7;
        const d = decode(r); n++;
        ok = ok && d !== null && d.state[0] === e.state[0] && d.state[1] === e.state[1] && d.readings.join() === observe(...e.state).join();
      }
    }
    return { pass: ok, decodes: n };
  }
  root.Omega42AD008 = { observe, encode, decode, certify, PHASES };
})(typeof window !== 'undefined' ? window : globalThis);
if (typeof module !== 'undefined' && require.main === module) {
  const c = globalThis.Omega42AD008.certify();
  console.log('AD-008 certificate:', c.pass ? 'PASS' : 'FAIL', '-', c.decodes, 'corrupted words decoded (81 states x 42 single + 756 double errors)');
  process.exit(c.pass ? 0 : 1);
}
