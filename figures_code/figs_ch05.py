# -*- coding: utf-8 -*-
"""제5장 그림: 실행은 책 폴더에서  python3 code/figs_ch05.py
그림 5-1 연금형·일시금형 급부(개념도)
그림 5-2 예제 5-1 영구장해 모형의 할인 체류확률과 EPV(넓이)
그림 5-3 예제 5-4 수치적분 오차와 격자 간격 h
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fig_style import new, save, COLORS, STYLES, MARKERS, plt
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------- 그림 5-1
fig, ax = new(6.3, 2.6)
ax.set_xlim(0, 10); ax.set_ylim(-0.6, 2.9); ax.grid(False)
ax.set_yticks([0, 1, 2]); ax.set_yticklabels(["상태 0\n(건강)", "상태 1\n(장해)", "상태 2\n(사망)"])
path = [(0, 3.0, 0), (3.0, 6.5, 1), (6.5, 10, 2)]
for a, b, s in path:
    ax.plot([a, b], [s, s], color=COLORS[0], lw=2.2)
ax.plot([3.0, 3.0], [0, 1], color=COLORS[0], lw=1, ls=":")
ax.plot([6.5, 6.5], [1, 2], color=COLORS[0], lw=1, ls=":")
ax.fill_between([3.0, 6.5], 0.82, 1.18, color=COLORS[1], alpha=0.25, hatch="///", edgecolor=COLORS[1], lw=0)
ax.text(5.45, 0.42, "연금형 급부: 상태 1에 있는 동안 연속 지급\n" r"$\overline{Y}_x^{\,01}=\int v^t\,I\{Y(x+t)=1\}\,dt$",
        ha="center", va="center", fontsize=8)
ax.plot(3.0, 0.5, marker="v", color=COLORS[3], ms=7)
ax.annotate(r"$0\to1$ 전이 시 일시금", xy=(3.0, 0.5), xytext=(0.3, 0.75), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=COLORS[2]))
ax.plot(6.5, 1.5, marker="v", color=COLORS[3], ms=7)
ax.annotate(r"$1\to2$ 전이 시 일시금", xy=(6.5, 1.5), xytext=(7.1, 1.4), fontsize=8,
            arrowprops=dict(arrowstyle="->", color=COLORS[2]))
ax.set_xlabel("경과시간 $t$ (한 계약의 상태 경로 예시)")
ax.set_xticks([0, 3.0, 6.5, 10]); ax.set_xticklabels(["0", "전이 시점 1", "전이 시점 2", ""])
save(fig, "ch05_fig1.png")

# ---------------------------------------------------------------- 그림 5-2
m01, m02, m12, d = 0.02, 0.01, 0.05, 0.04
al = m01 + m02
t = np.linspace(0, 80, 4001)
g00 = np.exp(-d * t) * np.exp(-al * t)
g01 = np.exp(-d * t) * m01 / (m12 - al) * (np.exp(-al * t) - np.exp(-m12 * t))
a00 = np.trapezoid(g00, t) + np.exp(-(al + d) * 80) / (al + d)
a01_exact = m01 / (m12 - al) * (1 / (al + d) - 1 / (m12 + d))
print("그림5-2 abar00 =", round(1 / (al + d), 4), " abar01 =", round(a01_exact, 4), " (본문 14.2857, 3.1746)")
fig, ax = new()
ax.plot(t, g00, color=COLORS[0], ls=STYLES[0], label=r"$v^t\,{}_tp_x^{00}$  (넓이 $\bar a_x^{00}=14.2857$)")
ax.fill_between(t, 0, g00, color=COLORS[0], alpha=0.12)
ax.plot(t, g01, color=COLORS[1], ls=STYLES[1], label=r"$v^t\,{}_tp_x^{01}$  (넓이 $\bar a_x^{01}=3.1746$)")
ax.fill_between(t, 0, g01, facecolor="none", hatch="///", edgecolor=COLORS[1], lw=0)
ax.set_xlim(0, 80); ax.set_ylim(0, 1.02)
ax.set_xlabel("경과시간 $t$ (년)"); ax.set_ylabel("할인된 체류확률")
ax.legend(loc="upper right", frameon=False)
save(fig, "ch05_fig2.png")

# ---------------------------------------------------------------- 그림 5-3
a1, b1, c1, a2, b2, c2 = 4e-4, 3.4674e-6, 0.138155, 5e-4, 7.5858e-5, 0.087498
x0, delta = 60, 0.05
mu01 = lambda y: a1 + b1 * np.exp(c1 * y)
mu10 = lambda y: 0.1 * mu01(y)
mu02 = lambda y: a2 + b2 * np.exp(c2 * y)

def rhs(s, p):
    y = x0 + s
    p0, p1 = p
    return np.array([p1 * mu10(y) - p0 * (mu01(y) + mu02(y)),
                     p0 * mu01(y) - p1 * (mu10(y) + mu02(y))])

# 정밀 해: RK4, h=1/1200 → 격자값 저장
H = 1 / 1200; N = 12000
P = np.zeros((N + 1, 2)); P[0] = [1, 0]
for k in range(N):
    s = k * H; p = P[k]
    k1 = rhs(s, p); k2 = rhs(s + H / 2, p + H / 2 * k1); k3 = rhs(s + H / 2, p + H / 2 * k2); k4 = rhs(s + H, p + H * k3)
    P[k + 1] = p + H / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
ts = np.arange(N + 1) * H
G = P * np.exp(-delta * ts)[:, None]
# 정확값: 미세 격자 Simpson
exact = H / 3 * (G[0] + G[-1] + 4 * G[1:-1:2].sum(0) + 2 * G[2:-1:2].sum(0))
print("그림5-3 정확값 abar00, abar01 =", np.round(exact, 5), " (본문 6.53509, 0.65975)")
print("       10p00, 10p01 =", np.round(P[-1], 6), " 5p =", np.round(P[6000], 6))

def rule(hh, kind):
    step = int(round(hh / H)); g = G[::step]; n = len(g) - 1
    if kind == "trap":
        return hh * (g[0] / 2 + g[1:-1].sum(0) + g[-1] / 2)
    return hh / 3 * (g[0] + g[-1] + 4 * g[1:-1:2].sum(0) + 2 * g[2:-1:2].sum(0))

hs = [5, 2.5, 1, 0.5, 0.25, 1 / 12]
tr = np.array([rule(h, "trap") for h in hs]); si = np.array([rule(h, "simp") for h in hs])
print("h=5 사다리꼴", np.round(tr[0], 4), " Simpson", np.round(si[0], 4), " (본문 6.5970/0.6481, 6.5360/0.6591)")
fig, axs = new(6.3, 3.0, ncols=2)
for j, (ax, nm) in enumerate(zip(axs, [r"$\bar a^{00}_{60:\overline{10}\rceil}$", r"$\bar a^{01}_{60:\overline{10}\rceil}$"])):
    ax.loglog(hs, np.abs(tr[:, j] - exact[j]), color=COLORS[0], ls=STYLES[0], marker=MARKERS[0], label="사다리꼴")
    ax.loglog(hs, np.abs(si[:, j] - exact[j]), color=COLORS[1], ls=STYLES[1], marker=MARKERS[1], label="Simpson")
    ax.set_title(nm + " 의 절대오차")
    ax.set_xlabel("격자 간격 $h$ (년)")
    ax.set_xticks([1 / 12, 0.25, 1, 5]); ax.set_xticklabels(["1/12", "1/4", "1", "5"])
    ax.minorticks_off()
axs[0].set_ylabel("|근사값 − 정확값|")
axs[0].legend(frameon=False, loc="lower right")
fig.tight_layout()
save(fig, "ch05_fig3.png")
