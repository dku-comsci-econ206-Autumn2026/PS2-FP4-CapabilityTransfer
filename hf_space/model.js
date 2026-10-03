/* Four decisions, two reward rules, and the future market-share motive.
   Levels are the paper's Appendix A parameters plus the six constants fitted to Table 2
   (residual 7.4e-5). The future-share term follows the economics of open source:
   beta (discount factor), phi (efficiency of the open source ecosystem), K (external
   contributions an open release attracts), m (share of compatible applications), m0
   (internal-capacity scale). See code/distill_sim.py and the paper's Appendix A. */

const C_D0 = 1.4446;   // distillation cost level
const C_N0 = 5.6704;   // training cost level
const PI_0 = 8.2391;   // monopoly profit level
const L    = 2.5193;   // lost exclusivity
const E_D  = 0.9854;   // training compute reported on a distilled release
const E_N  = 4.6311;   // ... and on an original release

const R_LUMP = 20.0;   // Tool 1
const CAP    = 12.0;   // capped run

/* future market-share motive: beta * phi * K * m / (m + m0) */
const BETA = 0.90;     // time discount factor
const PHI  = 0.50;     // efficiency of the open source ecosystem
const K_EXT = 44.4;    // external contributions an open release attracts
const M0   = 0.50;     // internal-capacity scale
const ECOSYSTEM = BETA * PHI * K_EXT;     // = 19.98
const M_REP = 1.0;     // representative firm, as in the paper's Table 1

/* reward on [distilled, original] releases */
function reward(rule, k) {
  if (rule === "none")     return [0, 0];
  if (rule === "openness") return [R_LUMP, R_LUMP];          // Tool 1, lump sum
  if (rule === "indexed")  return [k * E_D, k * E_N];        // Tool 2, per unit of E
  if (rule === "capped")   return [Math.min(k * E_D, CAP), Math.min(k * E_N, CAP)];
  return [0, 0];
}

/* value of the future market share an open release buys */
function future(m = M_REP, ecosystem = ECOSYSTEM, m0 = M0) {
  return ecosystem * m / (m + m0);
}

/* (1) closed+distill  (2) open+distill  (3) closed+train  (4) open+train */
function payoffs(rule, k, ecosystem = ECOSYSTEM, m = M_REP) {
  const [rSmall, rLarge] = reward(rule, k);
  const f = future(m, ecosystem);
  return {
    1: -C_D0 + PI_0 * m,
    2: -C_D0 + rSmall - L + f,
    3: -C_N0 + PI_0 * m,
    4: -C_N0 + rLarge - L + f,
  };
}

/* Thresholds. Disclosure needs k*E_d > L + pi*m - future(m); innovation needs k > dC/dE,
   which the future term does not affect because it is common to both open cells. */
function thresholds(ecosystem = ECOSYSTEM, m = M_REP) {
  return {
    disclosure: (L + PI_0 * m - future(m, ecosystem)) / E_D,
    innovation: (C_N0 - C_D0) / (E_N - E_D),
  };
}

/* Range of m where a firm opens at k = 0: future(m) > L + pi*m.
   Solves pi*m^2 + (pi*m0 + L - ecosystem) m + L*m0 = 0. */
function opennessWindow(ecosystem = ECOSYSTEM, m0 = M0) {
  const a = PI_0, b = PI_0 * m0 + L - ecosystem, c = L * m0;
  const disc = b * b - 4 * a * c;
  if (disc <= 0) return [NaN, NaN];
  const r = Math.sqrt(disc);
  return [(-b - r) / (2 * a), (-b + r) / (2 * a)];
}

/* Private and social rankings, from the paper's Table 1. */
const PRIVATE_ORDER = [1, 3, 2, 4];
const SOCIAL_ORDER  = [4, 2, 3, 1];

const READING = { 1: "free rider", 2: "passer-on", 3: "monopolist", 4: "source" };
const STATE   = { 1: "state 1 closed", 2: "state 2 distill", 3: "state 3 healthy" };

/* Table 2 of the paper (seed 206, N = 20000), share of firms per decision.
   (a) no future-share motive, (b) with it. */
const TABLE2 = [
  { rule: "none, k = 0",             shares: [0.96, 0.00, 0.04, 0.00], state: 1 },
  { rule: "openness, R = 20",        shares: [0.11, 0.85, 0.00, 0.04], state: 2 },
  { rule: "indexed, k = 4",          shares: [0.35, 0.00, 0.01, 0.64], state: 3 },
  { rule: "indexed, capped, k = 12", shares: [0.42, 0.54, 0.02, 0.03], state: 2 },
];

const TABLE2_MOTIVE = [
  { rule: "none, k = 0",             shares: [0.28, 0.68, 0.01, 0.03], state: 2 },
  { rule: "openness, R = 20",        shares: [0.01, 0.95, 0.00, 0.04], state: 2 },
  { rule: "indexed, k = 4",          shares: [0.03, 0.02, 0.00, 0.95], state: 3 },
  { rule: "indexed, capped, k = 12", shares: [0.03, 0.93, 0.00, 0.05], state: 2 },
];

if (typeof module !== "undefined")
  module.exports = { reward, payoffs, thresholds, future, opennessWindow,
                     READING, STATE, TABLE2, TABLE2_MOTIVE, PRIVATE_ORDER, SOCIAL_ORDER,
                     BETA, PHI, K_EXT, M0, ECOSYSTEM };
