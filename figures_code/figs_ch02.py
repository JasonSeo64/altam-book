# -*- coding: utf-8 -*-
"""제2장 그림: 대표 다중상태모형 4종(그림 2-1), 장해소득 모형의 Euler 해(그림 2-2), 확정시점 퇴직(그림 2-3)
실행: 책 폴더에서 python3 code/figs_ch02.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig_style as fs
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---- 그림 2-1: 상태전이도 4종 ----
BOX = dict(boxstyle="round,pad=0.02,rounding_size=0.08", lw=0.9, ec="#444444")


def node(ax, x, y, w, h, text, absorb=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, fc="#E3E3E3" if absorb else "white", **BOX))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5)


def arrow(ax, p0, p1, label=None, lpos=None, dashed=False, rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=9, lw=0.9, color="#333333",
                                 ls=(0, (3, 2)) if dashed else "-", connectionstyle=f"arc3,rad={rad}"))
    if label:
        ax.text(*lpos, label, ha="center", va="center", fontsize=8.5)


fig, axs = fs.new(6.3, 4.6, nrows=2, ncols=2)
for a in axs.flat:
    a.set_xlim(0, 10); a.set_ylim(0, 6); a.axis("off")
# (a) 영구장해
a = axs[0, 0]; a.set_title("(a) 영구장해 모형", fontsize=9.5)
node(a, 2.2, 4.4, 3.0, 1.1, "0 건강"); node(a, 7.8, 4.4, 3.0, 1.1, "1 장해"); node(a, 5.0, 1.3, 3.0, 1.1, "2 사망", True)
arrow(a, (3.75, 4.4), (6.25, 4.4), "$\\mu^{01}$", (5.0, 4.85))
arrow(a, (2.6, 3.8), (4.3, 1.9), "$\\mu^{02}$", (2.75, 2.7))
arrow(a, (7.4, 3.8), (5.7, 1.9), "$\\mu^{12}$", (7.3, 2.7))
# (b) 장해소득
a = axs[0, 1]; a.set_title("(b) 장해소득 모형(회복 허용)", fontsize=9.5)
node(a, 2.2, 4.4, 3.0, 1.1, "0 건강"); node(a, 7.8, 4.4, 3.0, 1.1, "1 장해"); node(a, 5.0, 1.3, 3.0, 1.1, "2 사망", True)
arrow(a, (3.75, 4.6), (6.25, 4.6), "$\\mu^{01}$", (5.0, 5.05))
arrow(a, (6.25, 4.2), (3.75, 4.2), "$\\mu^{10}$", (5.0, 3.75))
arrow(a, (2.6, 3.8), (4.3, 1.9), "$\\mu^{02}$", (2.75, 2.7))
arrow(a, (7.4, 3.8), (5.7, 1.9), "$\\mu^{12}$", (7.3, 2.7))
# (c) LTC, (d) CCRC
for a, title, labs, note in [
    (axs[1, 0], "(c) 장기요양(LTC) 모형", ["0 건강", "1 경증 요양", "2 중증 요양"], "점선: 경증에서 건강으로의 회복(선택적 가정)"),
    (axs[1, 1], "(d) CCRC 모형", ["0 IL 독립", "1 AL 보조", "2 SNF 요양"], "점선: AL 일시 입소 후 IL로 복귀")]:
    a.set_title(title, fontsize=9.5)
    xs = [1.6, 5.0, 8.4]
    for xx, lb in zip(xs, labs):
        node(a, xx, 4.2, 2.8, 1.0, lb)
    node(a, 5.0, 1.3, 8.6, 0.9, "3 사망", True)
    arrow(a, (3.0, 4.35), (3.6, 4.35)); arrow(a, (6.4, 4.35), (7.0, 4.35))
    arrow(a, (3.6, 4.0), (3.0, 4.0), dashed=True)
    a.add_patch(FancyArrowPatch((1.6, 4.7), (8.4, 4.7), arrowstyle="-|>", mutation_scale=9, lw=0.9,
                                color="#333333", connectionstyle="bar,fraction=-0.08"))
    for xx in xs:
        arrow(a, (xx, 3.7), (xx, 1.75))
    a.text(0.2, 0.15, note, fontsize=7.5)
fig.tight_layout()
fs.save(fig, "ch02_fig1.png")

# ---- 그림 2-2: 장해소득 모형(예제 2-2)의 Euler 해 ----
a1, b1, c1 = 4e-4, 3.4674e-6, 0.138155
a2, b2, c2 = 5e-4, 7.5858e-5, 0.087498
m01 = lambda x: a1 + b1 * np.exp(c1 * x)
m10 = lambda x: 0.1 * m01(x)
m02 = lambda x: a2 + b2 * np.exp(c2 * x)
m12 = m02


def euler(h, x=60, T=10):
    n = int(round(T / h)); p0, p1 = 1.0, 0.0
    out = [(0.0, p0, p1)]
    for k in range(n):
        y = x + k * h
        d0 = p1 * m10(y) - p0 * (m01(y) + m02(y))
        d1 = p0 * m01(y) - p1 * (m10(y) + m12(y))
        p0, p1 = p0 + h * d0, p1 + h * d1
        out.append(((k + 1) * h, p0, p1))
    return np.array(out)


E = euler(1 / 12)
t = E[:, 0]; p00 = E[:, 1]; p01 = E[:, 2]; p02 = 1 - p00 - p01
s = np.linspace(0, 10, 100001)
cum = np.concatenate([[0], np.cumsum((m01(60 + s[:-1]) + m02(60 + s[:-1]) + m01(60 + s[1:]) + m02(60 + s[1:])) / 2 * np.diff(s))])
pbar = np.exp(-cum)
print("h=1/12: 10p00 =", round(p00[-1], 5), " 10p01 =", round(p01[-1], 5), " 10p02 =", round(p02[-1], 5))
print("10p00bar =", round(pbar[-1], 5))
hs = [1, 1 / 2, 1 / 4, 1 / 12, 1 / 120, 1 / 1200, 1 / 12000]
ends = {h: euler(h)[-1] for h in hs}
for h in (1 / 120, 1 / 12000):
    e = ends[h]
    print(f"h=1/{round(1 / h)}: 10p00 = {e[1]:.5f}  10p01 = {e[2]:.5f}  10p02 = {1 - e[1] - e[2]:.5f}")
ref = ends[1 / 12000][1]
fig, (ax, bx) = fs.new(6.3, 2.9, ncols=2, gridspec_kw=dict(width_ratios=[1.35, 1]))
ax.plot(t, p00, color=fs.COLORS[0], ls=fs.STYLES[0], label="${}_tp_{60}^{00}$ 건강")
ax.plot(t, p01, color=fs.COLORS[1], ls=fs.STYLES[1], label="${}_tp_{60}^{01}$ 장해")
ax.plot(t, p02, color=fs.COLORS[3], ls=fs.STYLES[2], label="${}_tp_{60}^{02}$ 사망")
for val, dy in ((p00[-1], 0.05), (p01[-1], -0.07), (p02[-1], 0.03)):
    ax.plot([10], [val], marker="o", ms=3.5, color="black")
    ax.text(9.9, val + dy, f"{val:.5f}", fontsize=7.5, ha="right")
ax.set_ylim(0, 1.03); ax.set_xlabel("경과연수 $t$"); ax.set_ylabel("확률")
ax.set_title("(a) 상태확률($h=1/12$)")
ax.legend(loc="center left", frameon=False)
hh = np.array(hs[:-1]); err = np.array([abs(ends[h][1] - ref) for h in hh])
bx.loglog(hh, err, color=fs.COLORS[0], marker=fs.MARKERS[0], ms=4)
bx.loglog(hh, err[0] * hh / hh[0], color=fs.COLORS[2], ls=fs.STYLES[1], lw=1.0, label="기울기 1 ($O(h)$)")
bx.set_xlabel("간격 $h$ (로그)"); bx.set_ylabel("${}_{10}p_{60}^{00}$의 오차 (로그)")
bx.set_title("(b) Euler법의 누적 오차")
bx.legend(loc="upper left", frameon=False)
fig.tight_layout()
fs.save(fig, "ch02_fig2.png")

# ---- 그림 2-3: 확정시점 퇴직(예제 2-4) ----
mu01, mu02, mu12 = 0.05, 0.01, 0.015
tt = np.linspace(0, 10, 1001)
P0 = np.where(tt < 5, np.exp(-(mu01 + mu02) * tt), 0.0)
# 65세 전 조기퇴직 후 퇴직 상태에 있을 확률
a = mu01 + mu02 - mu12
early = lambda u: mu01 * np.exp(-mu12 * u) * (1 - np.exp(-a * np.minimum(u, 5))) / a
P1 = np.where(tt < 5, early(tt), early(tt) + np.exp(-(mu01 + mu02) * 5) * np.exp(-mu12 * (tt - 5)))
P2 = 1 - P0 - P1
print("10p01 =", round(P1[-1], 5), " early part =", round(early(10.0), 5),
      " normal part =", round(np.exp(-0.3) * np.exp(-0.075), 5))
fig, ax = fs.new(6.3, 3.0)
m = tt < 5
ax.plot(60 + tt[m], P0[m], color=fs.COLORS[0], ls=fs.STYLES[0], label="${}_tp_{60}^{00}$ (재직)")
ax.plot(60 + tt[~m], P0[~m], color=fs.COLORS[0], ls=fs.STYLES[0])
ax.plot(60 + tt[m], P1[m], color=fs.COLORS[1], ls=fs.STYLES[1], label="${}_tp_{60}^{01}$ (퇴직)")
ax.plot(60 + tt[~m], P1[~m], color=fs.COLORS[1], ls=fs.STYLES[1])
ax.plot(60 + tt, P2, color=fs.COLORS[2], ls=fs.STYLES[2], label="${}_tp_{60}^{02}$ (사망)")
ax.annotate("", xy=(65, P1[tt >= 5][0]), xytext=(65, P1[m][-1]),
            arrowprops=dict(arrowstyle="-|>", lw=1.0, ls=(0, (2, 2))))
ax.text(65.2, 0.45, "65세 정년:\n재직자 전원이\n퇴직 상태로 이동", fontsize=8)
ax.plot([70], [P1[-1]], marker="o", ms=4, color="black")
ax.text(68.2, P1[-1] + 0.05, f"${{}}_{{10}}p_{{60}}^{{01}}={P1[-1]:.5f}$", fontsize=8)
ax.set_xlabel("나이"); ax.set_ylabel("확률"); ax.set_ylim(0, 1.05)
ax.set_title("확정시점 전이가 있는 재직자 모형")
ax.legend(loc="center left", frameon=False)
fs.save(fig, "ch02_fig3.png")
