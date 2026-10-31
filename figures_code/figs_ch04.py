# -*- coding: utf-8 -*-
"""제4장 그림: 예제 4-1의 관측 구조(그림 4-1), 전이 수에 따른 상대우도와 신뢰구간(그림 4-2)
실행: 책 폴더에서 python3 code/figs_ch04.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig_style as fs

# ---- 그림 4-1: [60, 61) 구간의 관측 구조(예제 4-1) ----
obs = [(1, 60.0, 61.0, "생존"), (2, 60.0, 60.4, "사망"), (3, 60.2, 61.0, "생존"), (4, 60.0, 60.7, "해약"),
       (5, 60.5, 61.0, "생존"), (6, 60.0, 60.9, "사망"), (7, 60.3, 60.8, "해약"), (8, 60.0, 61.0, "생존")]
v = sum(e - s for _, s, e, _ in obs); d = sum(r == "사망" for *_, r in obs)
E0 = v + sum(61.0 - e for _, s, e, r in obs if r == "사망")
print(f"v={v:.1f} d={d} mu_hat={d / v:.5f} q_hat={1 - np.exp(-d / v):.5f} E0={E0:.1f} q_act={d / E0:.5f}")
fig, ax = fs.new(6.3, 3.0)
mk = {"생존": ("|", 9, "구간 끝까지 생존"), "사망": ("X", 7, "사망"), "해약": ("o", 6, "해약(중도절단)")}
seen = set()
for k, s, e, r in obs:
    y = 9 - k
    ax.plot([s, e], [y, y], color=fs.COLORS[0], lw=2.2, solid_capstyle="butt")
    if r == "사망":
        ax.plot([e, 61.0], [y, y], color=fs.COLORS[2], lw=1.0, ls=(0, (2, 2)))
    m, ms, lab = mk[r]
    ax.plot([e], [y], marker=m, ms=ms, color="black", mfc="white" if m == "o" else "black", ls="none",
            label=None if r in seen else lab)
    seen.add(r)
    if s > 60.0:
        ax.plot([60.0, s], [y, y], color="#BBBBBB", lw=1.0, ls=":")
    ax.text(e + (0.012 if e < 61 else 0.018), y + 0.18, f"{e - s:.1f}", fontsize=7.5)
ax.plot([], [], color="#BBBBBB", lw=1.0, ls=":", label="관측 전(좌측 절단)")
ax.plot([], [], color=fs.COLORS[2], lw=1.0, ls=(0, (2, 2)), label="계리 추정에만 더하는 기간")
ax.set_yticks(range(1, 9), [f"{k}번" for k in range(8, 0, -1)])
ax.set_xlim(59.95, 61.18); ax.set_ylim(0.3, 8.8)
ax.set_xlabel("나이"); ax.grid(axis="y", visible=False)
ax.set_title(f"관측기간(굵은 선)의 합 $v={v:.1f}$, 사망 $d={d}$")
ax.legend(loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.42), fontsize=7.5)
fs.save(fig, "ch04_fig1.png")

# ---- 그림 4-2: 전이 수 n에 따른 상대우도와 95% 근사 신뢰구간 ----
cases = [("예제 4-1", 2, 5.8), ("예제 4-3", 32, 4850.0)]
r = np.linspace(0.001, 3.6, 1200)
fig, ax = fs.new(6.3, 3.0)
for (name, n, vv), col, ls, yb in zip(cases, (fs.COLORS[1], fs.COLORS[0]), (fs.STYLES[1], fs.STYLES[0]), (-0.08, -0.16)):
    mu = n / vv; sd = np.sqrt(n) / vv
    lo, hi = mu - 1.96 * sd, mu + 1.96 * sd
    print(f"{name}: mu_hat={mu:.6f} sd={sd:.6f} CI=({lo:.6f}, {hi:.6f})  log-CI=({mu * np.exp(-1.96 / np.sqrt(n)):.6f}, {mu * np.exp(1.96 / np.sqrt(n)):.6f})")
    R = r ** n * np.exp(-n * (r - 1))
    ax.plot(r, R, color=col, ls=ls, label=f"{name}: $n={n}$, $\\hat\\mu={mu:.4g}$")
    ax.plot([lo / mu, hi / mu], [yb, yb], color=col, lw=2.2, solid_capstyle="butt")
    ax.plot([1], [yb], marker="|", ms=8, color=col)
    ax.text(hi / mu + 0.04, yb - 0.025, f"95% 구간 ({lo:.3g}, {hi:.3g})", fontsize=7.5, color="black")
ax.axvline(0, color="black", lw=0.8)
ax.set_xlim(-0.5, 3.6); ax.set_ylim(-0.22, 1.08)
ax.set_xlabel("$\\mu/\\hat\\mu$ (추정값 대비 비율)"); ax.set_ylabel("상대우도 $L(\\mu)/L(\\hat\\mu)$")
ax.set_title("관측 전이 수가 정밀도를 정한다: 구간 폭 $\\propto 1/\\sqrt{n}$")
ax.legend(loc="upper right", frameon=False)
fs.save(fig, "ch04_fig2.png")
