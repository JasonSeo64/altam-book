# -*- coding: utf-8 -*-
"""제6장 그림: 실행은 책 폴더에서  python3 code/figs_ch06.py
그림 6-1 대기기간이 있는 장해연금의 시간선(개념도)
그림 6-2 예제 6-2 대기기간과 순보험료
그림 6-3 예제 6-4 4상태 LTC의 상태확률
그림 6-4 예제 6-6 CCRC 계약 유형별 수입·비용 EPV
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.linalg import expm
from fig_style import new, save, COLORS, STYLES, MARKERS, won, plt

# ---------------------------------------------------------------- 그림 6-1
fig, ax = new(6.3, 2.4)
ax.set_xlim(0, 10); ax.set_ylim(-1.0, 2.2); ax.grid(False)
for sp in ["left", "bottom"]:
    ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.set_yticks([])
ax.annotate("", xy=(9.9, 0), xytext=(0.1, 0), arrowprops=dict(arrowstyle="->", color="black", lw=1))
pts = [(0.3, "0\n(가입)"), (2.5, "$s$\n장해 시작"), (4.5, "$s+w$\n대기기간 종료"), (8.0, "$s+u$\n회복·사망")]
for xx, lab in pts:
    ax.plot([xx, xx], [-0.1, 0.1], color="black", lw=1)
    ax.text(xx, -0.25, lab, ha="center", va="top", fontsize=8)
ax.fill_between([2.5, 4.5], 0.25, 0.75, facecolor="none", hatch="..", edgecolor=COLORS[2], lw=0.8)
ax.text(3.5, 0.95, "대기기간 $w$\n(급부 없음)", ha="center", fontsize=8)
ax.fill_between([4.5, 8.0], 0.25, 0.75, color=COLORS[1], alpha=0.3, hatch="///", edgecolor=COLORS[1], lw=0)
ax.text(6.25, 0.95, "장해연금 지급\n(장해가 계속되는 동안)", ha="center", fontsize=8)
ax.text(1.4, 0.45, "건강", ha="center", fontsize=8)
ax.text(5.0, 1.75, r"바깥 적분: 장해 시작 시점 $s$의 밀도 ${}_sp_x^{00}\mu_{x+s}^{01}$   안쪽 적분: $u\geq w$인 동안의 체류 ${}_up_{x+s}^{\overline{11}}$",
        ha="center", fontsize=8)
save(fig, "ch06_fig1.png")

# ---------------------------------------------------------------- 그림 6-2
m01, m02, m12, d = 0.02, 0.01, 0.05, 0.04
al = m01 + m02
a00 = 1 / (al + d)
a01 = m01 / (m12 - al) * (1 / (al + d) - 1 / (m12 + d))
P = lambda w: 10000 * a01 * np.exp(-(m12 + d) * w) / a00
print("그림6-2 P(0)=%.2f P(0.25)=%.2f  (본문 2,222.22, 2,172.78)" % (P(0), P(0.25)))
w = np.linspace(0, 2, 201)
fig, ax = new()
ax.plot(w * 12, P(w), color=COLORS[0], ls=STYLES[0])
for ww, lab in [(0, "대기기간 없음\n2,222.22"), (0.25, "3개월\n2,172.78"), (0.5, None), (1.0, None)]:
    ax.plot(ww * 12, P(ww), marker=MARKERS[0], color=COLORS[1], ms=5)
    txt = lab or f"{int(ww*12)}개월\n{P(ww):,.2f}"
    ax.annotate(txt, xy=(ww * 12, P(ww)), xytext=(ww * 12 + 0.6, P(ww) + 40), fontsize=8)
ax.set_xlabel("대기기간 $w$ (개월)"); ax.set_ylabel("연속 순보험료 (연액)")
ax.set_xlim(0, 24); ax.set_ylim(1800, 2350); won(ax)
save(fig, "ch06_fig2.png")

# ---------------------------------------------------------------- 그림 6-3
mu = {(0, 1): 0.03, (0, 2): 0.01, (0, 3): 0.02, (1, 0): 0.05, (1, 2): 0.10, (1, 3): 0.08, (2, 3): 0.25}
Q = np.zeros((4, 4))
for (i, j), v in mu.items():
    Q[i, j] = v; Q[i, i] -= v
dl = 0.04
A = np.linalg.inv(dl * np.eye(3) - Q[:3, :3])
print("그림6-3 첫 행 abar =", np.round(A[0], 5), " (본문 10.58824 1.17647 0.77079)")
print("        P =", round((12000 * A[0, 1] + 30000 * A[0, 2]) / A[0, 0], 2), " (본문 3,517.24)")
ts = np.linspace(0, 60, 601)
Pt = np.array([expm(Q * t)[0] for t in ts])
fig, (ax, ax2) = new(6.3, 3.0, ncols=2, gridspec_kw={"width_ratios": [1.25, 1]})
labs = ["건강 (0)", "경증 요양 (1)", "중증 요양 (2)", "사망 (3)"]
for j in range(4):
    ax.plot(ts, Pt[:, j], color=COLORS[j], ls=STYLES[j], label=labs[j])
ax.set_xlabel("경과시간 $t$ (년)"); ax.set_ylabel(r"${}_tp^{0j}$  (건강 상태로 가입)")
ax.set_xlim(0, 60); ax.set_ylim(0, 1)
ax.legend(frameon=False, loc="center right", fontsize=7.5)
ax.set_title("네 상태 전체", fontsize=9)
for j in (1, 2):
    ax2.plot(ts, Pt[:, j], color=COLORS[j], ls=STYLES[j], label=labs[j])
ax2.set_xlim(0, 60); ax2.set_ylim(0, 0.09); ax2.set_xlabel("경과시간 $t$ (년)")
ax2.set_title("요양 상태 확대", fontsize=9); ax2.legend(frameon=False, fontsize=7.5)
fig.tight_layout()
save(fig, "ch06_fig3.png")

# ---------------------------------------------------------------- 그림 6-4
mu = {(0, 1): 0.05, (0, 2): 0.02, (0, 3): 0.03, (1, 0): 0.20, (1, 2): 0.10, (1, 3): 0.10, (2, 3): 0.30}
Q = np.zeros((4, 4))
for (i, j), v in mu.items():
    Q[i, j] = v; Q[i, i] -= v
a = np.linalg.inv(0.04 * np.eye(3) - Q[:3, :3])[0]
cost = np.array([30000, 60000, 120000]) * a
fees = {"Type A": np.array([30000, 30000, 30000]) * a, "Type B": np.array([30000, 30000, 80000]) * a,
        "Type C": np.array([30000, 60000, 120000]) * a}
E = {k: cost.sum() - v.sum() for k, v in fees.items()}
print("그림6-4 abar =", np.round(a, 5), " 비용 EPV = %.2f" % cost.sum(), " E =", {k: round(v, 2) for k, v in E.items()},
      " (본문 99,863.20 / 60,533.52 / 0)")
fig, ax = new()
xs = np.arange(4); wd = 0.6
names = ["비용 EPV"] + list(fees)
hatches = ["", "//", "xx"]
stlab = ["IL", "AL", "SNF"]
bottom = 0
for k in range(3):
    ax.bar(0, cost[k], wd, bottom=bottom, color=COLORS[k], alpha=0.85 if k == 0 else 0.6, hatch=hatches[k],
           edgecolor="white", label=f"{stlab[k]} 상태")
    bottom += cost[k]
for n, (t_, f) in enumerate(fees.items(), 1):
    b = 0
    for k in range(3):
        ax.bar(n, f[k], wd, bottom=b, color=COLORS[k], alpha=0.85 if k == 0 else 0.6, hatch=hatches[k], edgecolor="white")
        b += f[k]
    if E[t_] > 1:
        ax.bar(n, E[t_], wd, bottom=b, color="white", edgecolor=COLORS[4], hatch="..", lw=1.2,
               label="입주금 $E$" if n == 1 else None)
        ax.text(n, b + E[t_] / 2, f"E = {E[t_]:,.0f}", ha="center", va="center", fontsize=7.5,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    else:
        ax.text(n, b + 8000, "E = 0", ha="center", fontsize=7.5)
ax.set_xticks(xs); ax.set_xticklabels(["비용", "Type A\n수입", "Type B\n수입", "Type C\n수입"])
ax.set_ylabel("EPV (IL 입주자 1인)"); won(ax)
ax.set_ylim(0, 470000)
ax.legend(frameon=False, ncol=4, loc="upper center", fontsize=7.5)
ax.grid(axis="x")
save(fig, "ch06_fig4.png")
