# -*- coding: utf-8 -*-
"""제9장 그림: 9-1 한 보험연도 이익의 흐름(개념도), 9-2 예제 9-2 원천별 이익 폭포도, 9-3 순서효과 비교
실행: 책 폴더에서 python3 code/figs_ch09.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import plt, new, save, COLORS
from matplotlib.patches import FancyBboxPatch


def m(txt):
    """표준 9.1: 음수 부호는 U+2212"""
    return txt.replace("-", "\u2212")


# ---------- 예제 9-2 수치 ----------
N, V0, G, S = 1000, 1500.0, 150.0, 10000.0
i, e, q = 0.05, 27.5, 0.005
V1 = ((V0 + G - e) * (1 + i) - q * S) / (1 - q)          # 경험 가정 기준 준비금
ia, ea, Da, Wa, CV = 0.06, 34.0, 4, 20, 1550.0


def profit(ii, ee, D, W):
    return N * (V0 + G - ee) * (1 + ii) - D * S - W * CV - (N - D - W) * V1


base = profit(i, e, N * q, 0)
g_int = profit(ia, e, N * q, 0) - base
g_exp = profit(ia, ea, N * q, 0) - profit(ia, e, N * q, 0)
g_mort = profit(ia, ea, Da, 0) - profit(ia, ea, N * q, 0)
g_lapse = profit(ia, ea, Da, Wa) - profit(ia, ea, Da, 0)
actual = profit(ia, ea, Da, Wa)
print(f"V11={V1:.4f}  기대이익={base:.2f}")
print(f"이차익 {g_int:,.2f}  비차익 {g_exp:,.2f}  사차익 {g_mort:,.2f}  해약차익 {g_lapse:,.2f}  실제이익 {actual:,.2f}")
# 순서효과(사업비 먼저)
g_exp2 = profit(i, ea, N * q, 0) - base
g_int2 = profit(ia, ea, N * q, 0) - profit(i, ea, N * q, 0)
print(f"사업비 먼저: 이차익 {g_int2:,.2f} 비차익 {g_exp2:,.2f}")


# ---------- 그림 9-1 개념도 ----------
def box(ax, x, y, w, h, text, fc="#FFFFFF", ec=COLORS[0], fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, text=None, dy=0.12):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.2))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, text, ha="center", va="bottom", fontsize=8)


fig, ax = new(6.3, 3.0)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off"); ax.grid(False)
box(ax, 0.1, 2.9, 1.7, 0.9, "연초 준비금\n${}_tV$")
box(ax, 0.1, 1.6, 1.7, 0.9, "보험료 $G$")
box(ax, 0.1, 0.3, 1.7, 0.9, "사업비 $-e_t$", fc="#F2F2F2")
box(ax, 2.7, 1.4, 2.0, 1.4, "연초 순자산\n${}_tV+G-e_t$", fc="#EAF0F6", bold=True)
for y in (3.35, 2.05, 0.75):
    arrow(ax, 1.8, y, 2.7, 2.1)
box(ax, 5.6, 1.4, 1.9, 1.4, "연말 자산\n$\\times(1+i_t)$", fc="#EAF0F6", bold=True)
arrow(ax, 4.7, 2.1, 5.6, 2.1, "1년 부리")
box(ax, 8.2, 3.2, 1.7, 0.9, "사망: $q\\,(S+E)$", fc="#F2F2F2")
box(ax, 8.2, 1.85, 1.7, 0.9, "유지: $p\\,{}_{t+1}V$", fc="#F2F2F2")
box(ax, 8.2, 0.3, 1.7, 1.1, "남는 금액\n= 이익 $\\mathrm{Pr}_{t+1}$", fc="#FBE9D7", ec=COLORS[1], bold=True)
arrow(ax, 7.5, 2.4, 8.2, 3.6)
arrow(ax, 7.5, 2.1, 8.2, 2.3)
arrow(ax, 7.5, 1.8, 8.2, 0.85)
save(fig, "ch09_fig1.png")

# ---------- 그림 9-2 폭포도 ----------
labels = ["이차익", "비차익", "사차익", "해약차익", "실제이익"]
vals = [g_int, g_exp, g_mort, g_lapse]
fig, ax = new(6.3, 3.3)
cum = 0
for k, v in enumerate(vals):
    bottom = cum if v >= 0 else cum + v
    ax.bar(k, abs(v), bottom=bottom, width=0.6, color="white", edgecolor=COLORS[0],
           hatch="///" if v >= 0 else "...", lw=1.2)
    ax.text(k, cum + v + (500 if v >= 0 else -500), m(f"{v:+,.2f}"), ha="center",
            va="bottom" if v >= 0 else "top", fontsize=8)
    if k < len(vals) - 1:
        ax.plot([k + 0.3, k + 0.7], [cum + v, cum + v], color=COLORS[2], lw=0.8, ls="--")
    cum += v
ax.bar(4, actual, width=0.6, color=COLORS[0], edgecolor=COLORS[0])
ax.plot([3.3, 3.7], [cum, cum], color=COLORS[2], lw=0.8, ls="--")
ax.text(4, actual + 500, f"{actual:,.2f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
ax.set_xticks(range(5)); ax.set_xticklabels(labels)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("이익(1,000건 합계)")
ax.set_ylim(0, 27000)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: m(f"{v:,.0f}")))
ax.grid(axis="x", visible=False)
save(fig, "ch09_fig2.png")

# ---------- 그림 9-3 순서효과 ----------
fig, ax = new(6.3, 3.0)
orders = ["이자 → 사업비", "사업비 → 이자"]
ints = [g_int, g_int2]; exps = [g_exp, g_exp2]
y = [1, 0]
ax.barh([v + 0.18 for v in y], ints, height=0.34, color="white", edgecolor=COLORS[0], hatch="///", label="이차익")
ax.barh([v - 0.18 for v in y], exps, height=0.34, color="white", edgecolor=COLORS[1], hatch="...", label="비차익")
for yy, a, b in zip(y, ints, exps):
    ax.text(a + 250, yy + 0.18, f"{a:,.2f}", va="center", fontsize=8)
    ax.text(b - 250, yy - 0.18, m(f"{b:,.2f}"), va="center", ha="right", fontsize=8)
    ax.text(21500, yy, f"합계 {a + b:,.2f}", va="center", fontsize=8, fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels(orders)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlim(-13500, 25500)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: m(f"{v:,.0f}")))
ax.set_xlabel("이익(1,000건 합계)")
ax.legend(loc="lower right", frameon=False, ncol=2)
ax.grid(axis="y", visible=False)
save(fig, "ch09_fig3.png")
print("ok")
