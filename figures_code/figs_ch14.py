# -*- coding: utf-8 -*-
"""제14장 그림: 계정 구조(개념도), 예제 14-1 펀드 경로와 profit signature, 예제 14-2 영점화 준비금."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import new, save, COLORS, STYLES, MARKERS, plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

# ---------- 예제 14-1 모형 ----------
P, m, i, r = 100_000.0, 0.025, 0.05, 0.10
q = [0.008, 0.009, 0.010, 0.011, 0.012]
w = [0.05, 0.05, 0.05, 0.05, 0.0]
sc = [0.05, 0.04, 0.03, 0.0, 0.0]
n = 5


def project(R):
    F = P
    out = dict(F=[F], Pr=[], Pi=[], p=[], DB=[], MB=0.0)
    surv = 1.0
    for t in range(1, n + 1):
        MC = m * F
        E = 0.01 * P + 150 if t == 1 else 0.002 * F + 50
        Ft = (F - MC) * (1 + R[t - 1])
        db = q[t - 1] * max(P - Ft, 0)
        scin = (1 - q[t - 1]) * w[t - 1] * sc[t - 1] * Ft
        mb = (1 - q[t - 1]) * max(P - Ft, 0) if t == n else 0.0
        Pr = (MC - E) * (1 + i) - db + scin - mb
        out["Pr"].append(Pr); out["Pi"].append(surv * Pr); out["p"].append((1 - q[t - 1]) * (1 - w[t - 1]))
        surv *= (1 - q[t - 1]) * (1 - w[t - 1])
        F = Ft; out["F"].append(F)
    out["NPV"] = sum(pi / (1 + r) ** t for t, pi in enumerate(out["Pi"], 1))
    return out


be = project([0.07] * 5)
st = project([-0.25, 0.04, 0.04, 0.04, 0.04])
print("NPV 최선추정 %.2f, 스트레스 %.2f" % (be["NPV"], st["NPV"]))       # 본문 8,342.57 / −5,726.78
print("F_5 최선추정 %.2f, 스트레스 %.2f" % (be["F"][-1], st["F"][-1]))   # 본문 123,578.23 / 77,306.80
print("Pi 스트레스", [round(x, 2) for x in st["Pi"]])

# 영점화 준비금 (예제 14-2)
V = [0.0] * (n + 1)
for t in range(n, 0, -1):
    V[t - 1] = max((st["p"][t - 1] * V[t] - st["Pr"][t - 1]) / (1 + i), 0.0)
print("영점화 준비금", [round(v, 2) for v in V])                            # 본문 7,873.22, 10,240.59, 13,150.34, 16,384.44, 19,909.06, 0

comma = FuncFormatter(lambda v, p: f"{v:,.0f}")

# ---------- 그림 14-1: 두 계정의 구조 ----------
fig, ax = new(h=3.3)
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")


def box(x, y, w_, h_, text, fc, hatch=None, fs=9):
    ax.add_patch(FancyBboxPatch((x, y), w_, h_, boxstyle="round,pad=0.05,rounding_size=0.15",
                                fc=fc, ec="#333333", lw=1.0, hatch=hatch))
    ax.text(x + w_ / 2, y + h_ / 2, text, ha="center", va="center", fontsize=fs)


def arrow(x1, y1, x2, y2, text="", dy=0.18, ha="center"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=1.1, color="#333333"))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, text, ha=ha, va="bottom", fontsize=8)


box(0.1, 2.3, 1.7, 1.4, "계약자\n(보험료 납입,\n급부 수령)", "white")
box(3.0, 3.3, 3.0, 2.2, "펀드 계정 $F_t$\n(계약자 몫)\n수익률 $R_t$로 운용", "#E8EEF4")
box(3.0, 0.3, 3.0, 2.2, "", "#FBEBDD", hatch="///")
ax.text(4.5, 1.4, "비펀드 계정\n(회사 몫)\n이율 $i$로 운용", ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
box(7.6, 0.6, 2.2, 1.6, "주주\n위험할인율 $r$로\nNPV 평가", "white")
arrow(1.8, 3.5, 3.0, 4.6, "")
ax.text(2.0, 4.35, "보험료", fontsize=8, ha="right")
arrow(3.0, 4.0, 1.8, 3.1, "")
ax.text(2.55, 3.2, "펀드 가치 지급", fontsize=8, ha="left", va="top")
arrow(4.5, 3.3, 4.5, 2.5, "")
ax.text(4.62, 2.9, "운용수수료 $MC_t$\n해약공제 $SC_t$", fontsize=8, va="center")
arrow(3.0, 1.3, 1.8, 2.3, "")
ax.text(2.3, 1.25, "보증 부족분\n$DB_t$, $MB_n$", fontsize=8, ha="right", va="top")
arrow(6.0, 1.4, 7.6, 1.4, "$Pr_t$")
ax.text(6.15, 0.75, "사업비 $E_t$는\n비펀드에서 지출", fontsize=8)
save(fig, "ch14_fig1.png")

# ---------- 그림 14-2: 예제 14-1 펀드 경로와 profit signature ----------
fig, (a1, a2) = new(h=3.2, ncols=2)
ts = range(0, n + 1)
a1.plot(ts, be["F"], color=COLORS[0], ls=STYLES[0], marker=MARKERS[0], ms=4, label="최선추정(매년 7%)")
a1.plot(ts, st["F"], color=COLORS[1], ls=STYLES[1], marker=MARKERS[1], ms=4, label="스트레스(1년차 −25%)")
a1.axhline(P, color=COLORS[2], ls=":", lw=1.2, label="보증금액 $P$=100,000")
a1.fill_between([n - 0.15, n + 0.15], st["F"][-1], P, color="#CCCCCC", hatch="xx", ec="#666666", lw=0)
a1.annotate("GMMB 부족분", xy=(n - 0.15, (st["F"][-1] + P) / 2), xytext=(3.1, 81_500), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
a1.set_xlabel("경과연수 $t$"); a1.set_ylabel("펀드 $F_t$"); a1.yaxis.set_major_formatter(comma)
a1.set_title("(a) 펀드 경로와 보증"); a1.legend(loc="lower left", bbox_to_anchor=(0.2, 0.27), frameon=False)
x = list(range(1, n + 1)); bw = 0.38
a2.bar([t - bw / 2 for t in x], be["Pi"], bw, color="white", ec=COLORS[0], hatch="//", label="최선추정")
a2.bar([t + bw / 2 for t in x], st["Pi"], bw, color=COLORS[1], ec=COLORS[1], label="스트레스")
a2.axhline(0, color="#333333", lw=0.8)
a2.set_xlabel("보험연도 $t$"); a2.set_ylabel("profit signature $\\Pi_t$"); a2.yaxis.set_major_formatter(comma)
a2.set_title("(b) $\\Pi_t$: NPV %s 대 %s" % (f"{be['NPV']:,.2f}", f"{st['NPV']:,.2f}".replace("-", "−")))
a2.legend(loc="lower left", frameon=False)
fig.tight_layout()
save(fig, "ch14_fig2.png")

# ---------- 그림 14-3: 영점화 준비금 ----------
fig, ax = new(h=3.0)
ax.plot(range(0, n + 1), V, color=COLORS[0], marker=MARKERS[0], ms=4, label="영점화 준비금 ${}_tV$")
for t, v in enumerate(V[:-1]):
    ax.annotate(f"{v:,.2f}", (t, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7.5)
ax.set_xlabel("시점 $t$"); ax.set_ylabel("계약당 준비금"); ax.yaxis.set_major_formatter(comma)
ax.set_ylim(0, max(V) * 1.2)
ax.set_title("스트레스 경로(예제 14-2): 5년차 손실을 미리 메우는 준비금", fontsize=9)
ax.legend(loc="upper left", frameon=False)
save(fig, "ch14_fig3.png")
print("done")
