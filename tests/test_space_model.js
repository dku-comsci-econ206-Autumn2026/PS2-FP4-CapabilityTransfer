/* Logic checks for the Prize Rate Game page. Run: node test.js */
const M = require("./model.js");

let fails = 0;
function ok(name, cond, extra) {
  console.log((cond ? "  PASS  " : "  FAIL  ") + name + (extra ? "   " + extra : ""));
  if (!cond) fails++;
}
const close = (a, b, tol = 1e-6) => Math.abs(a - b) < tol;

/* --- old behaviour must be unchanged when the motive is switched off --- */
const u0 = M.payoffs("none", 0, 0);
ok("k = 0, no motive: (1) is privately best",
   Object.keys(u0).every(i => i === "1" || u0["1"] >= u0[i]));
const t0 = M.thresholds(0);
ok("no motive: disclosure threshold = (pi + L)/E_d", close(t0.disclosure, (8.2391 + 2.5193) / 0.9854, 1e-3),
   "= " + t0.disclosure.toFixed(4));
ok("innovation threshold = dC/dE", close(t0.innovation, (5.6704 - 1.4446) / (4.6311 - 0.9854), 1e-6),
   "= " + t0.innovation.toFixed(4));

/* --- the future market-share motive --- */
ok("future(1) = beta*phi*K/(1+m0)", close(M.future(1), 19.98 / 1.5, 1e-6),
   "= " + M.future(1).toFixed(4));
const u1 = M.payoffs("none", 0);
ok("k = 0, motive on: openness (2) beats closing (1)", u1[2] > u1[1],
   "(2)=" + u1[2].toFixed(2) + " vs (1)=" + u1[1].toFixed(2));
const t1 = M.thresholds();
ok("motive on: disclosure pays even at k = 0", t1.disclosure < 0, "= " + t1.disclosure.toFixed(2));
const [lo, hi] = M.opennessWindow();
ok("openness window is an interval", lo > 0 && hi > lo, "m in (" + lo.toFixed(3) + ", " + hi.toFixed(3) + ")");
ok("window brackets the representative firm m = 1", lo < 1 && hi > 1);

/* --- the paper's policy result survives the motive --- */
const uIdx = M.payoffs("indexed", 4);
const bestIdx = Object.keys(uIdx).reduce((a, b) => (uIdx[a] >= uIdx[b] ? a : b));
ok("indexed k = 4 still makes (4) privately best", bestIdx === "4",
   "(4)=" + uIdx[4].toFixed(2) + " vs (2)=" + uIdx[2].toFixed(2));
const uCap = M.payoffs("capped", 12);
const bestCap = Object.keys(uCap).reduce((a, b) => (uCap[a] >= uCap[b] ? a : b));
ok("capping still returns the market to imitation", bestCap === "2");

/* --- Table 2 panels are internally consistent with the state labels --- */
ok("panel (a): k = 0 is state 1", M.TABLE2[0].state === 1);
ok("panel (b): k = 0 is state 2", M.TABLE2_MOTIVE[0].state === 2);
ok("panel (b): indexed k = 4 is state 3", M.TABLE2_MOTIVE[2].state === 3);
ok("every share row sums to 1",
   [...M.TABLE2, ...M.TABLE2_MOTIVE].every(r => close(r.shares.reduce((a, b) => a + b, 0), 1, 0.02)));

console.log(fails ? "\n" + fails + " test(s) failed" : "\nall tests passed");
process.exit(fails ? 1 : 0);
