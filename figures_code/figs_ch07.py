# -*- coding: utf-8 -*-
"""제7장 그림: 실행은 책 폴더에서  python3 code/figs_ch07.py
그림 7-1 다중상태 준비금의 이산 점화식(개념도)
그림 7-2 예제 7-2 Thiele 방정식의 역방향 Euler 해와 정확해
그림 7-3 예제 7-3 장해소득보험의 상태별 준비금
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fig_style import new, save, COLORS, STYLES, MARKERS, won, plt
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------- 그림 7-1
fig, ax = new(6.3, 2.9)
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
def box(x, y, w, h, txt, fc="white", ec=COLORS[0]):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=8.5)
box(0.2, 1.7, 3.0, 1.6, "시점 $t$, 상태 $i$\n" r"${}_tV^{(i)}+P_t^{(i)}$" "\n(준비금 + 보험료)", fc="#EEF2F6")
ax.annotate("", xy=(4.6, 2.5), xytext=(3.3, 2.5), arrowprops=dict(arrowstyle="->", lw=1.4, color=COLORS[0]))
ax.text(3.95, 2.75, "×(1+i)", ha="center", fontsize=8)
box(4.6, 2.0, 1.4, 1.0, "1년 뒤\n자산", fc="#EEF2F6")
ys = [4.0, 2.5, 0.7]
labs = [r"상태 $j_1$: $b^{(ij_1)}+{}_{t+1}V^{(j_1)}$", r"상태 $j_2$: $b^{(ij_2)}+{}_{t+1}V^{(j_2)}$", "흡수상태(사망): $b^{(i,\\mathrm{d})}$ + 0"]
for y, lab in zip(ys, labs):
    ax.annotate("", xy=(7.0, y + 0.3), xytext=(6.05, 2.5), arrowprops=dict(arrowstyle="->", lw=1.0, color=COLORS[2]))
    box(7.0, y, 2.9, 0.6, lab)
for (xx, yy), pl in zip([(6.2, 3.6), (6.6, 2.9), (6.2, 1.35)], [r"$p^{ij_1}_{x+t}$", r"$p^{ij_2}_{x+t}$", r"$p^{i\mathrm{d}}_{x+t}$"]):
    ax.text(xx, yy, pl, fontsize=8, ha="center")
ax.text(5.0, 0.05, "좌변(1년 굴린 자산) = 우변(각 상태로 옮겨 간 계약의 급부와 새 준비금의 기댓값)", ha="center", fontsize=8)
save(fig, "ch07_fig1.png")

# ---------------------------------------------------------------- 그림 7-2
mu, d, S, n = 0.02, 0.05, 1000.0, 2.0
abar = lambda m: (1 - np.exp(-(mu + d) * m)) / (mu + d)
Abar = lambda m: mu * abar(m) + np.exp(-(mu + d) * m)
P = S * Abar(n) / abar(n)   # 485.8164 (본문 표기 485.82)
print("그림7-2 P = %.2f (본문 485.82)" % P)
Vex = lambda t: S * Abar(n - t) - P * abar(n - t)
def euler(h):
    ts = [n]; v = [S]
    while ts[-1] > 1e-9:
        V = v[-1]; v.append(V - h * (d * V + P - mu * (S - V))); ts.append(ts[-1] - h)
    return np.array(ts), np.array(v)
fig, ax = new()
tt = np.linspace(0, 2, 201)
ax.plot(tt, Vex(tt), color=COLORS[0], ls=STYLES[0], label="정확해")
for k, (h, lab) in enumerate([(0.5, "$h=0.5$"), (0.25, "$h=0.25$"), (1 / 12, "$h=1/12$")]):
    ts, v = euler(h)
    i1 = np.argmin(abs(ts - 1))
    print("  Euler h=%.4f  1V=%.2f" % (h, v[i1]))
    ax.plot(ts, v, color=COLORS[k + 1], ls=STYLES[k + 1], marker=MARKERS[k + 1] if h >= 0.25 else None, ms=4, label="역방향 Euler " + lab)
print("  정확해 1V=%.2f (본문 482.51; Euler 473.56, 478.09, 481.04)" % Vex(1))
ax.set_xlabel("시점 $t$ (년)"); ax.set_ylabel(r"${}_tV$"); ax.set_xlim(0, 2)
ax.legend(frameon=False, loc="upper left")
ax2 = ax.inset_axes([0.6, 0.12, 0.35, 0.38])
ax2.plot(tt, Vex(tt), color=COLORS[0], ls=STYLES[0])
for k, h in enumerate([0.5, 0.25, 1 / 12]):
    ts, v = euler(h); ax2.plot(ts, v, color=COLORS[k + 1], ls=STYLES[k + 1], marker=MARKERS[k + 1] if h >= 0.25 else None, ms=3)
ax2.set_xlim(0.9, 1.1); ax2.set_ylim(460, 500); ax2.set_title("$t=1$ 부근 확대", fontsize=7); ax2.tick_params(labelsize=6)
save(fig, "ch07_fig2.png")

from matplotlib.ticker import FuncFormatter
def wonm(ax):
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: ("−" if v < 0 else "") + f"{abs(v):,.0f}"))

# ---------------------------------------------------------------- 그림 7-3
a1, b1, c1, a2, b2, c2 = 4e-4, 3.4674e-6, 0.138155, 5e-4, 7.5858e-5, 0.087498
x0, dl, B, P = 60, 0.05, 20000.0, 2019.10
m01 = lambda y: a1 + b1 * np.exp(c1 * y)
m10 = lambda y: 0.1 * m01(y)
m02 = lambda y: a2 + b2 * np.exp(c2 * y)
def f(t, V):
    y = x0 + t; V0, V1 = V
    return np.array([dl * V0 + P - m01(y) * (V1 - V0) + m02(y) * V0,
                     dl * V1 - B - m10(y) * (V0 - V1) + m02(y) * V1])
H = 1 / 1200; N = 12000
V = np.zeros((N + 1, 2)); ts = 10 - np.arange(N + 1) * H
for k in range(N):  # RK4, 시간 역방향
    t = ts[k]; v = V[k]; h = -H
    k1 = f(t, v); k2 = f(t + h / 2, v + h / 2 * k1); k3 = f(t + h / 2, v + h / 2 * k2); k4 = f(t + h, v + h * k3)
    V[k + 1] = v + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
i5 = 6000
print("그림7-3 5V0=%.2f 5V1=%.2f 0V0=%.2f  (본문 -1,328.29, 82,407.80, 0)" % (V[i5, 0], V[i5, 1], V[-1, 0]))
fig, (axa, axb) = new(6.3, 3.0, ncols=2)
axa.plot(ts, V[:, 1], color=COLORS[1], ls=STYLES[1], label=r"장해 상태 ${}_tV^{(1)}$")
axa.plot(ts, V[:, 0], color=COLORS[0], ls=STYLES[0], label=r"건강 상태 ${}_tV^{(0)}$")
axa.text(5.25, 12000, f"$R^{{(01)}}$ = {V[i5,1]-V[i5,0]:,.0f}\n($t=5$)", fontsize=7.5)
axa.annotate("", xy=(5, V[i5, 1]), xytext=(5, V[i5, 0]), arrowprops=dict(arrowstyle="<->", color=COLORS[2], lw=1))
axa.set_xlabel("시점 $t$ (년, 나이 $60+t$)"); axa.set_title("상태별 준비금", fontsize=9); wonm(axa)
axa.set_xlim(0, 10); axa.legend(frameon=False, fontsize=7.5, loc="upper right")
axb.plot(ts, V[:, 0], color=COLORS[0], ls=STYLES[0])
axb.axhline(0, color="black", lw=0.6)
axb.plot(5, V[i5, 0], marker=MARKERS[0], color=COLORS[1], ms=4)
axb.annotate(f"${{}}_5V^{{(0)}}$ = −{abs(V[i5,0]):,.2f}", xy=(5, V[i5, 0]), xytext=(5.6, V[i5, 0] - 150), fontsize=7.5)
axb.set_xlabel("시점 $t$ (년)"); axb.set_title("건강 상태 준비금 확대 (음수)", fontsize=9); wonm(axb)
axb.set_xlim(0, 10)
fig.tight_layout()
save(fig, "ch07_fig3.png")
