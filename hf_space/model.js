/* 判定：k 落在哪一段。单位：E_d = 1, C_d = 0。 */
function verdict(k, L, dC, dE) {
  const lines = { open: L, innovate: dC / dE };   // 两条门槛
  const lower = Math.max(lines.open, lines.innovate);
  const willOpen    = k > lines.open;             // 蒸馏者愿意公开
  const willInnovate = k > lines.innovate;        // 有人愿意自己做
  let state;
  if (!willOpen) state = "secrecy";               // 没人公开：全闭源
  else if (!willInnovate) state = "imitation";    // 公开了但没人自己做：全蒸馏
  else state = "healthy";
  return { lines, lower, willOpen, willInnovate, state };
}

/* 四格净收益。E_d = 1, C_d = 0 => E_n = 1 + dE, C_n = dC */
function payoff(k, L, dC, dE) {
  const En = 1 + dE;
  return {
    imitateClosed:  0,
    imitateOpen:    k * 1 - L,
    innovateClosed: -dC,
    innovateOpen:   -dC + k * En - L,
  };
}

if (typeof module !== "undefined") module.exports = { verdict, payoff };
