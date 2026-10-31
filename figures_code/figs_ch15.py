# -*- coding: utf-8 -*-
"""제15장 그림: 보증의 지급 구조(풋옵션), 예제 15-1 GMDB 보증금액 경로, 예제 15-4 GLWB 펀드 소진."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import new, save, COLORS, STYLES, MARKERS, plt
import numpy as np

# ---------- 그림 15-1: 만기 지급과 회사 부담 ----------
G = 100.0
F = np.linspace(0, 200, 401)
fig, (a1, a2) = new(h=3.0, ncols=2)
a1.plot(F, np.maximum(G, F), color=COLORS[0], ls=STYLES[0], label="계약자 수령 $\\max(G,F_n)$")
a1.plot(F, F, color=COLORS[2], ls=STYLES[2], label="펀드 $F_n$ (계약자 몫)")
a1.fill_between(F, F, np.maximum(G, F), where=F < G, color="#DDDDDD", hatch="//", ec="#888888", lw=0, label="회사 부담")
a1.set_xlabel("만기 펀드 $F_n$"); a1.set_ylabel("금액"); a1.set_title("(a) 만기 지급의 분해")
a1.legend(loc="upper left", frameon=False); a1.set_xlim(0, 200); a1.set_ylim(0, 210)
a2.plot(F, np.maximum(G - F, 0), color=COLORS[1], ls=STYLES[1], label="회사 부담 $\\max(G-F_n,0)$")
a2.axvline(G, color=COLORS[2], ls=":", lw=1.0)
a2.text(G + 3, 80, "행사가격 $G$", fontsize=8)
a2.set_xlabel("만기 펀드 $F_n$"); a2.set_title("(b) 회사 부담 = 풋옵션 지급액")
a2.legend(loc="upper right", frameon=False); a2.set_xlim(0, 200); a2.set_ylim(0, 110)
fig.tight_layout()
save(fig, "ch15_fig1.png")

# ---------- 그림 15-2: 예제 15-1 ----------
P, m, g = 100.0, 0.025, 0.03
R = [0.12, -0.18, 0.06, -0.10, 0.15]
Fs = [P]
for r_ in R:
    Fs.append(Fs[-1] * (1 - m) * (1 + r_))
t = np.arange(0, 6)
roll = [P * (1 + g) ** k for k in t]
ratchet = [P]
for k in range(1, 6):
    ratchet.append(max([P] + Fs[1:k]))   # GD_t = max(P, F_1..F_{t-1})
ratchet[0] = P
comb = [max(a, b) for a, b in zip(roll, ratchet)]
print("F_t", [round(x, 3) for x in Fs[1:]])                      # 본문 109.200, 87.305, 90.230, 79.177, 88.777
print("래칫 부담", [round(max(ratchet[k] - Fs[k], 0), 3) for k in range(1, 6)])   # 0, 21.895, 18.970, 30.023, 20.423
print("롤업 부담", [round(max(roll[k] - Fs[k], 0), 3) for k in range(1, 6)])      # 0, 18.785, 19.043, 33.374, 27.150

fig, ax = new(h=3.2)
ax.plot(t, Fs, color=COLORS[0], ls=STYLES[0], marker=MARKERS[0], ms=4, label="펀드 $F_t$")
ax.plot(t, [P] * 6, color=COLORS[2], ls=STYLES[3], label="원금보장 $P$")
ax.plot(t, roll, color=COLORS[1], ls=STYLES[1], marker=MARKERS[1], ms=4, label="롤업 3%")
ax.step(t, ratchet, where="post", color=COLORS[3], ls=STYLES[2], lw=1.6, label="래칫")
ax.plot(t, ratchet, ls="none", marker=MARKERS[2], ms=4, color=COLORS[3])
for k in (2, 4):
    ax.annotate("", xy=(k, Fs[k]), xytext=(k, comb[k]), arrowprops=dict(arrowstyle="<->", lw=0.9, color="#444444"))
    ax.text(k + 0.06, 94.5 if k == 2 else (Fs[k] + comb[k]) / 2, f"결합형 부담\n{comb[k] - Fs[k]:.3f}", fontsize=7.5, va="center")
ax.set_xlabel("경과연수 $t$"); ax.set_ylabel("금액"); ax.set_ylim(70, 125)
ax.legend(loc="upper left", ncol=2, frameon=False)
save(fig, "ch15_fig2.png")

# ---------- 그림 15-3: 예제 15-4 GLWB ----------
W, m4, v = 6.0, 0.025, 1 / 1.04
Fp = [100.0]
for k in range(40):
    Fp.append(max((Fp[-1] - W) * (1 - m4), 0.0) if Fp[-1] >= W else 0.0)
tau = next(k for k, f in enumerate(Fp) if f < W)
pay_fund = [min(W, Fp[k]) for k in range(30)]
pay_co = [W - p for p in pay_fund]
pv = sum(pay_co[k] * v ** k for k in range(30))
print("F13 %.3f F14 %.3f tau %d PV %.2f" % (Fp[13], Fp[14], tau, pv))  # 본문 6.329, 0.321, 14, 41.80

fig, (a1, a2) = new(h=3.1, ncols=2, gridspec_kw=dict(width_ratios=[1, 1.25]))
a1.plot(range(0, 16), Fp[:16], color=COLORS[0], marker=MARKERS[0], ms=3.5)
a1.axhline(W, color=COLORS[2], ls=":", lw=1.0)
a1.text(0.3, W + 2, "인출액 $W=6$", fontsize=8)
a1.annotate(f"$F_{{14}}={Fp[14]:.3f}$", xy=(14, Fp[14]), xytext=(6.5, 12), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
a1.set_xlabel("시점 $t$ (나이 65+$t$)"); a1.set_ylabel("인출 전 펀드 $F_t$"); a1.set_title("(a) 펀드 소진 경로")
x = np.arange(30)
a2.bar(x, pay_fund, color="white", ec=COLORS[0], hatch="///", lw=0.6, label="펀드에서 인출")
a2.bar(x, pay_co, bottom=pay_fund, color=COLORS[1], ec=COLORS[1], lw=0.6, label="회사 부담")
a2.set_xlabel("인출 시점 $t$"); a2.set_ylabel("연초 인출액"); a2.set_ylim(0, 8.5)
a2.set_title(f"(b) 회사 부담의 현가(4%) = {pv:.2f}")
a2.legend(loc="upper left", ncol=2, frameon=False)
fig.tight_layout()
save(fig, "ch15_fig3.png")
print("done")
