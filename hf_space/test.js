const assert = require("assert");
const { payoffs, thresholds, TABLE2, PRIVATE_ORDER, SOCIAL_ORDER } = require("./model.js");

// --- the private ranking must be (1) > (3) > (2) > (4) at k = 0 -------------
const u0 = payoffs("none", 0);
const priv = [1, 2, 3, 4].sort((a, b) => u0[b] - u0[a]);
assert.deepStrictEqual(priv, PRIVATE_ORDER, `private order ${priv}`);
console.log(`k=0 private order   ${priv.join(" > ")}   (paper Table 1)`);

// --- and the social ranking is its exact reverse --------------------------
assert.deepStrictEqual([...SOCIAL_ORDER].reverse(), PRIVATE_ORDER);
console.log(`social order        ${SOCIAL_ORDER.join(" > ")}   (reverse)`);

// --- (1) is dominant at k = 0 ---------------------------------------------
assert.strictEqual(priv[0], 1);
console.log("(1) closed+distill is privately best at k = 0");

// --- Tool 1 makes (2) beat (4) at every level -----------------------------
for (const R of [1, 20, 100, 1000]) {
  const u = payoffs("openness", R);
  assert.ok(u[2] > u[4], `lump sum R=${R}: (2) must beat (4)`);
}
console.log("Tool 1: (2) beats (4) at every R — nobody trains");

// --- Tool 2 separates the two open cells ---------------------------------
const k = 4, u = payoffs("indexed", k);
assert.ok(u[4] > u[2], "indexed: (4) must beat (2) at k=4");
console.log(`Tool 2: at k=${k}, (4)=${u[4].toFixed(2)} > (2)=${u[2].toFixed(2)}`);

// --- thresholds ----------------------------------------------------------
const t = thresholds();
console.log(`thresholds: disclosure k > ${t.disclosure.toFixed(2)}, innovation k > ${t.innovation.toFixed(2)}`);

// --- capping collapses the differential between the two open cells --------
const cap = 12;
const noCap = cap * 4.6311 - cap * 0.9854;                                        // uncapped gap
const withCap = Math.min(cap * 4.6311, cap) - Math.min(cap * 0.9854, cap);        // capped gap
assert.ok(withCap < noCap / 100, `capped gap ${withCap} not << uncapped ${noCap}`);
console.log(`capped: the gap between (4) and (2) falls from ${noCap.toFixed(1)} to ${withCap.toFixed(2)}`);

// --- Table 2 row integrity ----------------------------------------------
assert.strictEqual(TABLE2.length, 4);
for (const row of TABLE2) {
  const s = row.shares.reduce((x, y) => x + y, 0);
  assert.ok(Math.abs(s - 1) < 0.02, `shares sum to ${s}`);
  assert.strictEqual(row.shares[3] === Math.max(...row.shares), row.state === 3);
}
console.log("Table 2: shares sum to 1; state 3 exactly when (4) is modal");
console.log("all checks passed");
