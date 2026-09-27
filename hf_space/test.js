const assert = require("assert");
const { verdictFlat, verdictPerE, payoffFlat, payoffPerE, originateGap } = require("./model.js");

const L = 1, dC = 2, dE = 1;

// --- flat policy: never reaches healthy ---------------------------------
assert.strictEqual(verdictFlat(0.5, L).state, "secrecy");
assert.strictEqual(verdictFlat(1.5, L).state, "imitation");
for (const k of [1.5, 5, 50, 5000]) {
  assert.notStrictEqual(verdictFlat(k, L).state, "healthy", `flat at k=${k} must not be healthy`);
}
console.log("flat  : secrecy -> imitation, never healthy");

// --- flat policy: originate can never win, at any k ----------------------
for (const k of [0.5, 1.5, 5, 50, 5000]) {
  assert.ok(originateGap(k, dC, dE, "flat") < 0, `flat gap at k=${k}`);
}
console.log(`flat  : originate - disclose = ${originateGap(9, dC, dE, "flat")} (fixed, negative)`);

// --- per-unit policy: second threshold exists ----------------------------
const k2 = dC / dE;
assert.strictEqual(verdictPerE(k2 - 1e-9, L, dC, dE).state, "imitation");
assert.strictEqual(verdictPerE(k2 + 1e-9, L, dC, dE).state, "healthy");
assert.ok(originateGap(k2 + 1e-9, dC, dE, "perE") > 0);
console.log(`perE  : flip exactly at k = dC/dE = ${k2}`);

// --- per-unit policy: ΔE -> 0 collapses onto flat ------------------------
assert.ok(originateGap(9, dC, 1e-9, "perE") < 0);
assert.strictEqual(verdictPerE(9, L, dC, 1e-9).state, "imitation");
console.log("perE  : as ΔE -> 0 it collapses onto the flat column");

// --- the two columns share the same disclose payoff ----------------------
for (const k of [0.2, 1, 4]) {
  assert.strictEqual(payoffFlat(k, L, dC).imitateOpen, payoffPerE(k, L, dC, dE).imitateOpen);
}
console.log("both  : disclose payoff is identical; only originate differs");

// --- bigger ΔE makes originate easier, not harder ------------------------
let prev = -Infinity;
for (const e of [0.2, 0.5, 1, 2, 4]) {
  const g = originateGap(3, dC, e, "perE");
  assert.ok(g > prev, `gap should rise with ΔE, at ${e}`);
  prev = g;
}
console.log("perE  : originate gap rises with ΔE");

console.log("all checks passed");
