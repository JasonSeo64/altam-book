# -*- coding: utf-8 -*-
"""제16장 그림: 만기별 풋옵션 가격(예제 16-2), 예제 16-4 헷지오차, 이산 헷지와 볼록성."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import new, save, COLORS, STYLES, MARKERS, plt
import numpy as np
from math import erf, sqrt, exp, log

Phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
r, sig, m = 0.05, 0.20, 0.025


def bsp(F, G, tau, m_=m):
    d1 = (log(F / G) + (r - m_ + 0.5 * sig ** 2) * tau) / (sig * sqrt(tau))
    d2 = d1 - sig * sqrt(tau)
    return G * exp(-r * tau) * Phi(-d2) - F * exp(-m_ * tau) * Phi(-d1), d1


def delta(F, G, tau):
    return -exp(-m * tau) * Phi(-bsp(F, G, tau)[1])


# ---------- 그림 16-1: 예제 16-2 만기별 BSP ----------
ks = np.arange(1, 11)
p_m = [bsp(100, 100, k)[0] for k in ks]
p_0 = [bsp(100, 100, k, 0.0)[0] for k in ks]
print("BSP(m=2.5%)", [round(x, 4) for x in p_m])   # 본문 6.5286 … 10.2221(k=7) … 9.8503
kmax = int(ks[int(np.argmax(p_m))])
print("최대 만기", kmax)
fig, ax = new(h=3.0)
ax.plot(ks, p_m, color=COLORS[0], ls=STYLES[0], marker=MARKERS[0], ms=4, label="수수료 $m=2.5\\%$ (예제 16-2)")
ax.plot(ks, p_0, color=COLORS[2], ls=STYLES[1], marker=MARKERS[1], ms=4, label="수수료 없음 $m=0$ (비교)")
ax.annotate(f"최대: $k={kmax}$, {max(p_m):.4f}", xy=(kmax, max(p_m)), xytext=(7.4, 7.6), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlabel("만기 $k$ (년)"); ax.set_ylabel("$BSP(0,100;100,k)$"); ax.set_xticks(ks)
ax.legend(loc="upper left", frameon=False)
save(fig, "ch16_fig1.png")

# ---------- 그림 16-2: 예제 16-4 헷지오차 ----------
n, G, pn = 3, 100.0, 0.99 ** 3
Fp = [100.0, 78.0, 95.0, 84.0]
H, a, b = [], [], []
for t in range(3):
    p, _ = bsp(Fp[t], G, n - t)
    H.append(pn * p); a.append(pn * delta(Fp[t], G, n - t) * Fp[t]); b.append(H[-1] - a[-1])
H.append(pn * max(G - Fp[3], 0))
old = [None] + [a[t - 1] * Fp[t] / Fp[t - 1] * exp(m) + b[t - 1] * exp(r) for t in (1, 2, 3)]
HE = [old[t] - H[t] for t in (1, 2, 3)]
pv = sum(HE[t - 1] * exp(-r * t) for t in (1, 2, 3))
print("H", [round(x, 4) for x in H], "HE", [round(x, 4) for x in HE], "PV %.3f" % pv)  # 본문 HE −1.6882, 1.3179, 0.0952, PV −0.331

fig, (a1, a2) = new(h=3.1, ncols=2)
x = np.array([1, 2, 3]); bw = 0.36
a1.bar(x - bw / 2, [old[t] for t in (1, 2, 3)], bw, color="white", ec=COLORS[0], hatch="//", label="기존 포트폴리오 가치")
a1.bar(x + bw / 2, H[1:], bw, color=COLORS[0], label="새 헷지 비용 $H_t$")
a1.set_xticks(x); a1.set_xlabel("시점 $t$"); a1.set_ylabel("최초 계약 1건당 금액")
a1.set_title("(a) 리밸런싱 직전의 비교"); a1.legend(loc="upper right", frameon=False)
a1.set_ylim(0, 27)
cols = [COLORS[1] if h < 0 else COLORS[3] for h in HE]
bars = a2.bar(x, HE, 0.5, color=cols, ec="#333333", lw=0.6)
for xi, h in zip(x, HE):
    a2.text(xi, h + (0.08 if h >= 0 else -0.08), f"{h:+.4f}".replace("-", "−"), ha="center",
            va="bottom" if h >= 0 else "top", fontsize=8)
a2.axhline(0, color="#333333", lw=0.8)
a2.set_xticks(x); a2.set_xlabel("시점 $t$"); a2.set_ylabel("헷지오차 $HE_t$")
a2.set_ylim(-2.3, 2.0)
a2.set_title(f"(b) 헷지오차(현가 {pv:.3f})".replace("-", "−"))
a2.set_xticklabels([f"{t_}\n($F_{t_}={F_:.0f}$)" for t_, F_ in zip(x, Fp[1:])])
fig.tight_layout()
save(fig, "ch16_fig2.png")

# ---------- 그림 16-3: 1년 뒤 펀드 F_1에 따른 헷지오차(예제 16-4 1년차, 최초 계약 1건당) ----------
F1 = np.linspace(55, 150, 300)
port = np.array([a[0] * f / 100.0 * exp(m) + b[0] * exp(r) for f in F1])     # 굴린 기존 포트폴리오(선형)
cost = np.array([pn * bsp(f, G, 2)[0] for f in F1])                          # 새 헷지 비용(볼록)
he78 = a[0] * 78 / 100 * exp(m) + b[0] * exp(r) - pn * bsp(78, G, 2)[0]
print("HE(F1=78) %.4f" % he78)   # 본문 −1.6882
fig, ax = new(h=3.1)
ax.plot(F1, cost, color=COLORS[0], ls=STYLES[0], label="새 헷지 비용 $H_1$ (볼록)")
ax.plot(F1, port, color=COLORS[1], ls=STYLES[1], label="굴린 기존 포트폴리오 (선형)")
ax.fill_between(F1, port, cost, where=cost > port, color="#D0D0D0", lw=0, label="손실 구간($HE<0$, 큰 움직임)")
ax.fill_between(F1, port, cost, where=cost <= port, color="#BFE3DE", hatch="//", ec=COLORS[3], lw=0, label="이익 구간($HE>0$, 작은 움직임)")
ax.axvline(78, color=COLORS[2], ls=":", lw=1.0)
ax.text(79, 33, f"$F_1=78$: $HE_1={he78:.4f}$".replace("-", "−"), fontsize=8)
ax.set_xlabel("1년 뒤 펀드 $F_1$"); ax.set_ylabel("최초 계약 1건당 금액"); ax.set_ylim(-6, 40)
ax.legend(loc="upper right", frameon=False)
save(fig, "ch16_fig3.png")
print("done")
