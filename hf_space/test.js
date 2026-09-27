const assert = require("assert");
const { verdict, payoff } = require("./model.js");

// 三档 k：低于两条线 / 在中间 / 都超过
const L = 1, dC = 2, dE = 1;
const cases = [
  [0.5, "secrecy"],    // k < L 且 k < ΔC/ΔE
  [1.5, "imitation"],  // k > L，但 k < ΔC/ΔE
  [2.5, "healthy"],    // k > max(L, ΔC/ΔE)
];
for (const [k, want] of cases) {
  const v = verdict(k, L, dC, dE);
  assert.strictEqual(v.state, want, `k=${k} -> ${v.state}, want ${want}`);
  console.log(`k=${k}  lower=${v.lower.toFixed(2)}  state=${v.state}`);
}

// 每个状态下，最优格子应该符合该状态的定义
const want = {
  secrecy:   "imitateClosed",
  imitation: "imitateOpen",
  healthy:   "innovateOpen",
};
for (const [k, state] of cases) {
  const p = payoff(k, L, dC, dE);
  const best = Object.entries(p).sort((a, b) => b[1] - a[1])[0][0];
  assert.strictEqual(best, want[state], `k=${k}: best=${best}, want ${want[state]}`);
  console.log(`k=${k}  best cell = ${best}`);
}

// 边界：k 刚好等于门槛时不算超过
assert.strictEqual(verdict(L, L, dC, dE).willOpen, false);
assert.strictEqual(verdict(dC / dE, L, dC, dE).willInnovate, false);

// 奖励定额（ΔE -> 0）时，创新门槛发散：任何 k 都救不了自己做的公司
const flat = verdict(1000, L, dC, 1e-9);
assert.strictEqual(flat.willInnovate, false);
console.log("ΔE -> 0 : innovate never pays, for any k");

console.log("all checks passed");
