# -*- coding: utf-8 -*-
"""제3장 그림: 다중탈퇴모형의 상태전이도(그림 3-1), 이중탈퇴표의 집단 구성(그림 3-2), 해약 시점과 종속탈퇴율(그림 3-3)
실행: 책 폴더에서 python3 code/figs_ch03.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig_style as fs
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---- 그림 3-1: 다중탈퇴모형 = 활동상태 하나와 흡수상태 m개 ----
fig, ax = fs.new(6.3, 2.6)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off")
BOX = dict(boxstyle="round,pad=0.02,rounding_size=0.08", lw=0.9, ec="#444444")
ax.add_patch(FancyBboxPatch((0.4, 1.9), 2.6, 1.2, fc="white", **BOX))
ax.text(1.7, 2.5, "0 활동\n(유효계약·재직)", ha="center", va="center", fontsize=8.5)
targets = [(3.75, "1 사망", "$\\mu_x^{01}$"), (2.55, "2 해약(퇴사)", "$\\mu_x^{02}$"), (1.2, "$m$ 기타 원인", "$\\mu_x^{0m}$")]
for y, lab, mu in targets:
    ax.add_patch(FancyBboxPatch((6.6, y - 0.4), 2.8, 0.8, fc="#E3E3E3", **BOX))
    ax.text(8.0, y, lab, ha="center", va="center", fontsize=8.5)
    ax.add_patch(FancyArrowPatch((3.05, 2.5), (6.55, y), arrowstyle="-|>", mutation_scale=10, lw=0.9, color="#333333"))
    ax.text(4.8, (2.5 + y) / 2 + 0.22, mu, ha="center", fontsize=8.5)
ax.text(8.0, 1.9, "$\\vdots$", ha="center", va="center", fontsize=10)
ax.text(0.4, 0.1, "흡수상태(음영)로 한 번 전이하면 끝나므로 ${}_tp_x^{00}={}_tp_x^{\\overline{00}}$이고 모든 확률이 폐쇄형이다",
        fontsize=8)
fs.save(fig, "ch03_fig1.png")

# ---- 그림 3-2: 예제 3-1의 이중탈퇴표 — 100,000명의 구성 변화 ----
pd_ = {60: 0.010, 61: 0.012, 62: 0.015}
pw_ = {60: 0.08, 61: 0.06, 62: 0.04}
l = {60: 100_000.0}; dd = {}; dw = {}
for x in (60, 61, 62):
    dd[x] = l[x] * pd_[x]; dw[x] = l[x] * pw_[x]; l[x + 1] = l[x] - dd[x] - dw[x]
ages = [60, 61, 62, 63]
cumd = [0.0] + list(np.cumsum([dd[x] for x in (60, 61, 62)]))
cumw = [0.0] + list(np.cumsum([dw[x] for x in (60, 61, 62)]))
inf = [l[x] for x in ages]
print("l63 =", round(l[63], 1), " 3p00 =", round(l[63] / 1e5, 5), " 3p0d =", round(cumd[-1] / 1e5, 5),
      " d62 =", round(dd[62], 1), round(dw[62], 1))
fig, ax = fs.new(6.3, 2.9)
xs = np.arange(len(ages))
b1 = ax.bar(xs, inf, color="white", edgecolor="#333333", hatch="", label="유효계약 $l_x$")
b2 = ax.bar(xs, cumw, bottom=inf, color="#BBBBBB", edgecolor="#333333", hatch="//", label="누적 해약")
b3 = ax.bar(xs, cumd, bottom=np.array(inf) + np.array(cumw), color="#555555", edgecolor="#333333",
            label="누적 사망")
for k in xs:
    ax.text(k, inf[k] / 2, f"{inf[k]:,.1f}", ha="center", va="center", fontsize=8)
k = 3
ax.annotate(f"누적 해약 {cumw[k]:,.1f}", xy=(k + 0.4, inf[k] + cumw[k] / 2), xytext=(k + 0.62, 84_000),
            fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.6))
ax.annotate(f"누적 사망 {cumd[k]:,.1f}", xy=(k + 0.4, inf[k] + cumw[k] + cumd[k] / 2), xytext=(k + 0.62, 95_000),
            fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.6))
ax.set_xticks(xs, [f"{x}세" for x in ages]); ax.set_xlim(-0.6, 4.6)
ax.set_ylim(0, 108_000); fs.won(ax)
ax.set_ylabel("인원(기수 100,000)")
ax.set_title("이중탈퇴표(예제 3-1)의 집단 구성: 매년 $l_x-l_{x+1}=d_x^{(d)}+d_x^{(w)}$")
ax.legend(loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.12))
fs.save(fig, "ch03_fig2.png")

# ---- 그림 3-3: 해약 시점 tau에 따른 종속탈퇴율(예제 3-5) ----
qd, qw = 0.02, 0.10
tau = np.linspace(0, 1, 201)
p0d = tau * qd + (1 - qw) * (1 - tau) * qd
p0w = (1 - tau * qd) * qw
for tt in (0.0, 0.5, 1.0):
    print(f"tau={tt}: p0d={tau[0] * 0 + tt * qd + (1 - qw) * (1 - tt) * qd:.5f} p0w={(1 - tt * qd) * qw:.5f}")
asdm_d, asdm_w = qd * (1 - qw / 2), qw * (1 - qd / 2)
fig, (a1, a2) = fs.new(6.3, 2.7, ncols=2)
for a, y, ref, lab, col in [(a1, p0d, asdm_d, "$p^{0d}$ (사망)", fs.COLORS[0]), (a2, p0w, asdm_w, "$p^{0w}$ (해약)", fs.COLORS[1])]:
    a.plot(tau, y, color=col, label=f"{lab}: 해약이 시점 $\\tau$에만 발생")
    a.axhline(ref, color="black", lw=0.8, ls=":", label=f"UDD in ASDM ({ref:.3f})")
    for tt in (0.5, 1.0):
        k = int(round(tt * 200))
        a.plot([tt], [y[k]], marker="o", ms=4, color="black")
        a.annotate(f"{y[k]:.3f}", xy=(tt, y[k]), xytext=(tt - 0.04, y[k] + (0.00015 if a is a1 else -0.00035)), fontsize=7.5, ha="right")
    a.set_xlabel("해약 시점 $\\tau$ (나이 내 위치)")
    a.legend(loc="lower left" if a is a2 else "upper left", frameon=False, fontsize=7)
a1.set_title("(a) 사망 종속탈퇴율"); a2.set_title("(b) 해약 종속탈퇴율")
a1.set_ylim(0.0175, 0.0212); a2.set_ylim(0.0975, 0.1007)
fig.tight_layout()
fs.save(fig, "ch03_fig3.png")
