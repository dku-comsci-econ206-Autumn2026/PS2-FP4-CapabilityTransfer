/* Four decisions, two reward rules.
   Levels are the paper's Appendix A parameters plus the six constants fitted to
   Table 2 (residual 7.4e-5). See code/distill_sim.py. */

const C_D0 = 1.4446;   // distillation cost level
const C_N0 = 5.6704;   // training cost level
const PI_0 = 8.2391;   // monopoly profit level
const L    = 2.5193;   // lost exclusivity
const E_D  = 0.9854;   // training compute reported on a distilled release
const E_N  = 4.6311;   // ... and on an original release

const R_LUMP = 20.0;   // Tool 1
const CAP    = 12.0;   // capped run

/* reward on [distilled, original] releases */
function reward(rule, k) {
  if (rule === "none")     return [0, 0];
  if (rule === "openness") return [R_LUMP, R_LUMP];          // Tool 1, lump sum
  if (rule === "indexed")  return [k * E_D, k * E_N];        // Tool 2, per unit of E
  if (rule === "capped")   return [Math.min(k * E_D, CAP), Math.min(k * E_N, CAP)];
  return [0, 0];
}

/* (1) closed+distill  (2) open+distill  (3) closed+train  (4) open+train */
function payoffs(rule, k) {
  const [rSmall, rLarge] = reward(rule, k);
  return {
    1: -C_D0 + PI_0,
    2: -C_D0 + rSmall - L,
    3: -C_N0 + PI_0,
    4: -C_N0 + rLarge - L,
  };
}

/* Analytic thresholds: disclosure needs k > L/E_d once the reward covers pi;
   innovation needs k > dC/dE. */
function thresholds() {
  return { disclosure: (PI_0 + L) / E_D, innovation: (C_N0 - C_D0) / (E_N - E_D) };
}

/* Private and social rankings, from the paper's Table 1. */
const PRIVATE_ORDER = [1, 3, 2, 4];
const SOCIAL_ORDER  = [4, 2, 3, 1];

const READING = { 1: "free rider", 2: "passer-on", 3: "monopolist", 4: "source" };
const STATE   = { 1: "state 1 closed", 2: "state 2 distill", 3: "state 3 healthy" };

/* Share of firms per decision, Table 2 of the paper (seed 206, N = 20000). */
const TABLE2 = [
  { rule: "none, k = 0",             shares: [0.96, 0.00, 0.04, 0.00], state: 1 },
  { rule: "openness, R = 20",        shares: [0.11, 0.85, 0.00, 0.04], state: 2 },
  { rule: "indexed, k = 4",          shares: [0.35, 0.00, 0.01, 0.64], state: 3 },
  { rule: "indexed, capped, k = 12", shares: [0.42, 0.54, 0.02, 0.03], state: 2 },
];

if (typeof module !== "undefined")
  module.exports = { reward, payoffs, thresholds, READING, STATE, TABLE2, PRIVATE_ORDER, SOCIAL_ORDER };
