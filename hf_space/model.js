/* Two policies.
   flat   : everyone who discloses gets the same prize R = k * E_d
   perE   : the prize is paid per unit of the firm's own training budget, k * E
   Units: E_d = 1, C_d = 0  =>  E_n = 1 + dE, C_n = dC
*/

function verdictFlat(k, L) {
  const willOpen = k > L;
  return { lower: L, willOpen, willInnovate: false, state: willOpen ? "imitation" : "secrecy" };
}

function verdictPerE(k, L, dC, dE) {
  const lower = Math.max(L, dC / dE);
  const willOpen = k > L;
  const willInnovate = k > dC / dE;
  return { lower, willOpen, willInnovate, state: !willOpen ? "secrecy" : willInnovate ? "healthy" : "imitation" };
}

function payoffFlat(k, L, dC) {
  return { imitateClosed: 0, imitateOpen: k * 1 - L, innovateClosed: -dC, innovateOpen: k - dC - L };
}

function payoffPerE(k, L, dC, dE) {
  return { imitateClosed: 0, imitateOpen: k * 1 - L, innovateClosed: -dC, innovateOpen: k * (1 + dE) - dC - L };
}

/* The one number that separates the two policies: originate minus disclose */
function originateGap(k, dC, dE, policy) {
  return policy === "flat" ? -dC : k * dE - dC;
}

if (typeof module !== "undefined")
  module.exports = { verdictFlat, verdictPerE, payoffFlat, payoffPerE, originateGap };
