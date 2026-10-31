# -*- coding: utf-8 -*-
"""제0장 그림: SULT 사망률·생존곡선, 준비금 점화식 시간선, 종신보험 준비금 경로
실행: 책 폴더에서 python3 code/figs_ch00.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig_style as fs
from matplotlib.patches import FancyArrowPatch

A, B, c, i = 0.00022, 2.7e-6, 1.124, 0.05
v = 1 / (1 + i)
OMEGA = 131


def tpx(x, t):
    return np.exp(-A * t - B * c ** x * (c ** t - 1) / np.log(c))


def qx(x):
    return 1 - tpx(x, 1)


def Ax(x):
    k = np.arange(0, OMEGA - x)
    return float(np.sum(v ** (k + 1) * tpx(x, k) * qx(x + k)))


def adue(x):
    k = np.arange(0, OMEGA - x)
    return float(np.sum(v ** k * tpx(x, k)))


# ---- 그림 0-1: SULT 사망률(선택·종국)과 생존곡선 ----
ages = np.arange(20, 101)
q = qx(ages)
print("10p60 =", round(tpx(60, 10), 5), " q60 =", round(qx(60), 6),
      " q[60] =", round(0.81 * qx(60), 6), " q[60]+1 =", round(0.9 * qx(61), 6))
fig, (a1, a2) = fs.new(6.3, 3.0, ncols=2)
a1.semilogy(ages, q, color=fs.COLORS[0], ls=fs.STYLES[0], label="종국률 $q_x$")
a1.semilogy(ages, 0.9 * q, color=fs.COLORS[1], ls=fs.STYLES[1], label="$q_{[x-1]+1}=0.9\\,q_x$")
a1.semilogy(ages, 0.81 * q, color=fs.COLORS[2], ls=fs.STYLES[2], label="$q_{[x]}=0.81\\,q_x$")
a1.set_xlabel("나이 $x$")
a1.set_ylabel("1년 사망률 (로그 눈금)")
a1.set_title("(a) SULT 선택률과 종국률")
a1.legend(loc="upper left", frameon=False)
t = np.arange(0, 61)
a2.plot(60 + t, tpx(60, t), color=fs.COLORS[0])
a2.plot([70], [tpx(60, 10)], marker="o", color=fs.COLORS[1], ms=5)
a2.annotate(f"$_{{10}}p_{{60}}={tpx(60, 10):.5f}$", xy=(70, tpx(60, 10)), xytext=(73, 0.98),
            fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
a2.set_xlabel("도달 나이 $60+t$")
a2.set_ylabel("$_tp_{60}$")
a2.set_ylim(0, 1.05)
a2.set_title("(b) 60세의 생존확률")
fig.tight_layout()
fs.save(fig, "ch00_fig1.png")

# ---- 그림 0-2: 준비금 점화식의 시간선(개념도) ----
fig, ax = fs.new(6.3, 2.6)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")
ax.plot([1, 9], [1.2, 1.2], color="black", lw=1.2)
for xx, lab in [(1, "$t$"), (9, "$t+1$")]:
    ax.plot([xx, xx], [1.05, 1.35], color="black", lw=1.2)
    ax.text(xx, 0.7, lab, ha="center", fontsize=10)
box = dict(boxstyle="round,pad=0.35", fc="white", ec="#555555", lw=0.9)
ax.text(1, 2.6, "연초 자산\n${}_tV+P_t-E_t$", ha="center", va="center", fontsize=9, bbox=box)
ax.text(5, 2.6, "1년 부리\n$\\times(1+i_t)$", ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.35", fc="#EEEEEE", ec="#555555", lw=0.9))
ax.text(9, 3.45, "사망자 몫  $q_{x+t}\\,(S_{t+1}+E^S_{t+1})$", ha="center", va="center", fontsize=9, bbox=box)
ax.text(9, 2.05, "생존자 몫  $p_{x+t}\\times$ ${}_{t+1}V$", ha="center", va="center", fontsize=9, bbox=box)
for (x0, y0, x1, y1) in [(2.15, 2.6, 4.05, 2.6), (5.95, 2.75, 7.0, 3.3), (5.95, 2.45, 7.55, 2.1)]:
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=12, lw=1.0, color="black"))
ax.text(5, 0.35, "좌변(연초 자산을 굴린 값) = 우변(연말에 필요한 금액)", ha="center", fontsize=9)
fs.save(fig, "ch00_fig2.png")

# ---- 그림 0-3: (60) 종신보험 준비금 경로 ----
S = 100_000
A60, a60 = Ax(60), adue(60)
P = S * A60 / a60
ts = np.arange(0, 51)
V = np.array([S * Ax(60 + k) - P * adue(60 + k) for k in ts])
print("A60 =", round(A60, 5), " a60 =", round(a60, 4), " P =", round(P, 2), " 10V =", round(V[10], 2))
fig, ax = fs.new(6.3, 3.0)
ax.plot(ts, V, color=fs.COLORS[0], label="${}_tV$ (장래법)")
ax.plot(ts, S * (1 - np.array([adue(60 + k) for k in ts]) / a60), ls="none",
        marker="o", ms=2.5, color=fs.COLORS[1], label="검산 $S(1-\\ddot a_{60+t}/\\ddot a_{60})$")
ax.plot([10], [V[10]], marker="s", ms=6, mfc="white", color="black")
ax.annotate("${}_{10}V=" + f"{V[10]:,.2f}".replace(",", "{,}") + "$", xy=(10, V[10]), xytext=(14, V[10] - 9000), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlabel("경과연수 $t$")
ax.set_ylabel("준비금")
fs.won(ax)
ax.set_title("(60) 완전이산 종신보험(보험금 100,000)의 준비금")
ax.legend(loc="upper left", frameon=False)
fs.save(fig, "ch00_fig3.png")
