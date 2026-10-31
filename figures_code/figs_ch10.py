# -*- coding: utf-8 -*-
"""제10장 그림: 10-1 profit vector와 profit signature, 10-2 위험할인율별 NPV와 IRR, 10-3 zeroization 전후 이익
모두 예제 10-1·10-3의 계약(50세, 10년 정기, 100,000, SULT, 해약 5%, i=6%, G=260)에서 계산한다.
실행: 책 폴더에서 python3 code/figs_ch10.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import plt, new, save, COLORS, STYLES, MARKERS
import numpy as np


def m(txt):
    return txt.replace("-", "−")


FMT = plt.FuncFormatter(lambda v, p: m(f"{v:,.0f}"))

# ---------- SULT ----------
A, B, c = 0.00022, 2.7e-6, 1.124


def q(x):
    return 1 - math.exp(-(A + B * c ** x * (c - 1) / math.log(c)))


v4 = 1 / 1.04


def term_A(x, n):
    s, p = 0.0, 1.0
    for k in range(n):
        s += p * q(x + k) * v4 ** (k + 1); p *= 1 - q(x + k)
    return s


def ann(x, n):
    s, p = 0.0, 1.0
    for k in range(n):
        s += p * v4 ** k; p *= 1 - q(x + k)
    return s


S, G, E0, i, r, n = 100000, 260.0, 400.0, 0.06, 0.10, 10
e = 0.03 * G
P = S * term_A(50, n) / ann(50, n)
V = [S * term_A(50 + t, n - t) - P * ann(50 + t, n - t) for t in range(n + 1)]


def lapse(t):
    return 0.05 if t < n else 0.0


def profit_vector(res):
    return [-E0] + [(res[t - 1] + G - e) * (1 + i) - q(49 + t) * S - (1 - q(49 + t)) * (1 - lapse(t)) * res[t]
                    for t in range(1, n + 1)]


def signature(pr):
    out, s = [pr[0]], 1.0
    for t in range(1, n + 1):
        out.append(s * pr[t]); s *= (1 - q(49 + t)) * (1 - lapse(t))
    return out


def npv(sig, rr):
    return sum(x / (1 + rr) ** t for t, x in enumerate(sig))


pr = profit_vector(V)
sig = signature(pr)
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if npv(sig, mid) > 0 else (lo, mid)
irr = lo
print(f"P={P:.2f}  NPV(10%)={npv(sig, r):.2f}  IRR={irr:.4%}")
print("Pr", [round(x, 2) for x in pr]); print("Pi", [round(x, 2) for x in sig])

# zeroization
Vz = [0.0] * (n + 1)
for t in range(n, 0, -1):
    Vz[t - 1] = max(0.0, (q(49 + t) * S + (1 - q(49 + t)) * (1 - lapse(t)) * Vz[t]) / (1 + i) - (G - e))
pr0 = profit_vector([0.0] * (n + 1)); prz = profit_vector(Vz)
print("무준비금 Pr", [round(x, 2) for x in pr0[1:]])
print("zeroization V", [round(x, 2) for x in Vz[:-1]])
print("zeroization Pr", [round(x, 2) for x in prz[1:]])
print(f"NPV 무준비금 {npv(signature(pr0), r):.2f}, zeroization {npv(signature(prz), r):.2f}")

# ---------- 그림 10-1 ----------
t = np.arange(0, n + 1)
fig, ax = new(6.3, 3.2)
w = 0.38
ax.bar(t - w / 2, pr, width=w, color="white", edgecolor=COLORS[0], hatch="///", label="profit vector $\\mathrm{Pr}_t$ (연초 유효계약 1건당)")
ax.bar(t + w / 2, sig, width=w, color=COLORS[1], edgecolor=COLORS[1], label="profit signature $\\Pi_t$ (판매 계약 1건당)")
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(t); ax.set_xlabel("보험연도 $t$"); ax.set_ylabel("이익")
ax.yaxis.set_major_formatter(FMT)
ax.annotate(m(f"계약 전 사업비 {pr[0]:,.0f}"), xy=(0, pr[0]), xytext=(1.2, -330), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.8))
ax.set_ylim(-450, 140)
ax.legend(loc="lower right", frameon=False)
ax.grid(axis="x", visible=False)
save(fig, "ch10_fig1.png")

# ---------- 그림 10-2 ----------
rr = np.linspace(0.0, 0.20, 201)
vals = [npv(sig, x) for x in rr]
fig, ax = new(6.3, 3.2)
ax.plot(rr * 100, vals, color=COLORS[0], ls=STYLES[0])
ax.axhline(0, color="black", lw=0.8)
ax.plot([r * 100], [npv(sig, r)], marker=MARKERS[0], color=COLORS[1], ms=6, ls="none")
ax.annotate(f"$r=10\\%$: NPV = {npv(sig, r):,.2f}", xy=(r * 100, npv(sig, r)), xytext=(11.5, 95), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.8))
ax.plot([irr * 100], [0], marker=MARKERS[1], color=COLORS[0], ms=6, ls="none")
ax.annotate(f"IRR = {irr * 100:.2f}%", xy=(irr * 100, 0), xytext=(14.5, 40), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.8))
ax.set_xlabel("위험할인율 $r$ (%)"); ax.set_ylabel("NPV (판매 계약 1건당)")
ax.yaxis.set_major_formatter(FMT)
save(fig, "ch10_fig2.png")

# ---------- 그림 10-3 ----------
tt = np.arange(1, n + 1)
fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0), gridspec_kw=dict(width_ratios=[1.6, 1]))
ax = axs[0]
ax.plot(tt, pr0[1:], color=COLORS[2], ls=STYLES[1], marker=MARKERS[1], ms=4, label="준비금 없음")
ax.plot(tt, prz[1:], color=COLORS[0], ls=STYLES[0], marker=MARKERS[0], ms=4, label="zeroization 후")
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(tt); ax.set_xlabel("보험연도 $t$"); ax.set_ylabel("$\\mathrm{Pr}_t$")
ax.yaxis.set_major_formatter(FMT)
ax.set_title("(a) profit vector", fontsize=9)
ax.legend(frameon=False, loc="upper right")
ax = axs[1]
ax.bar(np.arange(0, n), Vz[:-1], color="white", edgecolor=COLORS[0], hatch="///")
for k in range(n):
    if Vz[k] > 0:
        ax.text(k, Vz[k] + 1, f"{Vz[k]:.2f}", ha="center", va="bottom", fontsize=7, rotation=90)
ax.set_xticks(range(0, n)); ax.set_xlabel("시점 $t-1$"); ax.set_ylabel("준비금")
ax.set_ylim(0, 52)
ax.set_title("(b) zeroization 준비금", fontsize=9)
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, "ch10_fig3.png")
print("ok")
