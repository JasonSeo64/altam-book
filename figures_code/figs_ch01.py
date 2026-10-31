# -*- coding: utf-8 -*-
"""제1장 그림: 사망률 곡선의 모양(그림 1-1), 연금 가입자 사망률과 연금 EPV(그림 1-2), 생존자 평균 허약도(그림 1-3)
실행: 책 폴더에서 python3 code/figs_ch01.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig_style as fs

# ---- 그림 1-1: (a) Heligman–Pollard 예시, (b) Gompertz 개인 사력과 감마 frailty 집단 사력 ----
# (a)의 모수는 곡선의 모양을 보이기 위한 예시값이다(본문 1.2.1).
HP = dict(A=0.0008, B=0.02, C=0.12, D=0.0010, E=12.0, F=22.0, G=0.00004, H=1.105)


def hp_q(x):
    p = HP
    x = np.maximum(x, 1e-6)
    r = p["A"] ** ((x + p["B"]) ** p["C"]) + p["D"] * np.exp(-p["E"] * (np.log(x) - np.log(p["F"])) ** 2) \
        + p["G"] * p["H"] ** x
    return r / (1 + r)


B, c, s2 = 2.7e-6, 1.124, 0.25
lnc = np.log(c)


def mu(x):
    return B * c ** x


def M(x):  # 누적 사력, x0 = 0
    return B * (c ** x - 1) / lnc


def EZ(x):  # 생존자 평균 허약도
    return 1 / (1 + s2 * M(x))


def mubar(x):
    return mu(x) * EZ(x)


fig, (a1, a2) = fs.new(6.3, 2.9, ncols=2)
xa = np.arange(0, 101)
a1.semilogy(xa, hp_q(xa), color=fs.COLORS[0])
a1.annotate("영아 사망", xy=(1, hp_q(np.array([1.0]))[0]), xytext=(12, 1.2e-2), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
xh = 22
a1.annotate("사고 혹(accident hump)", xy=(xh, hp_q(np.array([float(xh)]))[0]), xytext=(28, 2.5e-4), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
a1.annotate("노화 구간: 지수 증가", xy=(70, hp_q(np.array([70.0]))[0]), xytext=(25, 6e-2), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
a1.set_xlabel("나이")
a1.set_ylabel("$q_x$ (로그 눈금)")
a1.set_title("(a) 전 나이 사망률 곡선(예시 모수)")
xb = np.linspace(60, 115, 221)
a2.semilogy(xb, mu(xb), color=fs.COLORS[2], ls=fs.STYLES[1], label="개인 사력(Gompertz)")
a2.semilogy(xb, mubar(xb), color=fs.COLORS[1], ls=fs.STYLES[0], label="집단 사력(감마 frailty, $\\sigma^2=0.25$)")
a2.axhline(lnc / s2, color="black", lw=0.8, ls=":")
a2.text(61, lnc / s2 * 1.15, f"상한 $\\ln c/\\sigma^2={lnc / s2:.4f}$", fontsize=8)
a2.set_xlabel("나이")
a2.set_title("(b) 고연령 사망률 감속과 이질성")
a2.legend(loc="lower right", frameon=False)
fig.tight_layout()
fs.save(fig, "ch01_fig1.png")
for x in (90, 100):
    print(f"x={x}: mu={mu(x):.5f} mubar={mubar(x):.5f} EZ={EZ(x):.4f}")
print("upper bound", round(lnc / s2, 4))

# ---- 그림 1-2: 연금 가입자 사망률(SULT의 80%)과 연금 EPV ----
A_, B_, c_, i = 0.00022, 2.7e-6, 1.124, 0.05
v = 1 / (1 + i)


def q_sult(x):
    return 1 - np.exp(-A_ - B_ * c_ ** x * (c_ - 1) / np.log(c_))


def adue(x, mult=1.0, select=False, omega=131):
    k = np.arange(0, omega - x)
    q = mult * q_sult(x + k)
    if select:
        q = q.copy(); q[0] *= 0.81; q[1] *= 0.9
    q = np.minimum(q, 1.0)
    p = np.concatenate([[1.0], np.cumprod(1 - q)[:-1]])
    return float(np.sum(v ** k * p))


print("a[60] =", round(adue(60, select=True), 4), " a60 =", round(adue(60), 4))
print("a65 SULT =", round(adue(65), 4), " a65 80% =", round(adue(65, 0.8), 4),
      " +", round((adue(65, 0.8) / adue(65) - 1) * 100, 1), "%")
ages = np.arange(50, 91)
a100 = np.array([adue(x) for x in ages])
a80 = np.array([adue(x, 0.8) for x in ages])
fig, (b1, b2) = fs.new(6.3, 2.8, ncols=2)
b1.plot(ages, a100, color=fs.COLORS[0], ls=fs.STYLES[0], label="SULT")
b1.plot(ages, a80, color=fs.COLORS[1], ls=fs.STYLES[1], label="SULT × 0.8 (연금 가입자)")
for val, col in [(adue(65), fs.COLORS[0]), (adue(65, 0.8), fs.COLORS[1])]:
    b1.plot([65], [val], marker="o", ms=4, color=col)
b1.annotate(f"$\\ddot a_{{65}}$: {adue(65):.4f} → {adue(65, 0.8):.4f}", xy=(65, adue(65, 0.8)),
            xytext=(67, 15.6), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
b1.set_xlabel("나이 $x$"); b1.set_ylabel("$\\ddot a_x$")
b1.set_title("(a) 사망률 수준에 따른 $\\ddot a_x$")
b1.legend(loc="lower left", frameon=False)
b2.plot(ages, (a80 / a100 - 1) * 100, color=fs.COLORS[1], ls=fs.STYLES[1], marker=fs.MARKERS[1], ms=2.5,
        markevery=5, label="사망률 80%")
sel = np.array([adue(x, select=True) for x in ages])
b2.plot(ages, (sel / a100 - 1) * 100, color=fs.COLORS[2], ls=fs.STYLES[2], marker=fs.MARKERS[2], ms=2.5,
        markevery=5, label="2년 선택표")
b2.set_xlabel("나이 $x$"); b2.set_ylabel("SULT 대비 증가율(%)")
b2.set_title("(b) 연금 EPV의 증가율")
b2.legend(loc="upper left", frameon=False)
fig.tight_layout()
fs.save(fig, "ch01_fig2.png")

# ---- 그림 1-3: 생존자 평균 허약도 ----
xs = np.linspace(60, 115, 221)
fig, ax = fs.new(6.3, 2.8)
ax.plot(xs, EZ(xs), color=fs.COLORS[0], label="$E[Z\\mid T>x]$ (생존자 평균 허약도)")
ax.plot(xs, mubar(xs) / mu(xs), ls="none")
for x in (90, 100):
    ax.plot([x], [EZ(x)], marker="s", ms=5, mfc="white", color="black")
    ax.annotate(f"{x}세: {EZ(x):.4f}", xy=(x, EZ(x)), xytext=(x + 2.5, EZ(x) + 0.08), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.8))
ax.axhline(1, color="black", lw=0.8, ls=":")
ax.text(61, 1.02, "출생 시 평균 1", fontsize=8)
ax.set_ylim(0, 1.12)
ax.set_xlabel("나이 $x$"); ax.set_ylabel("평균 허약도 = $\\bar\\mu_x/\\mu_x$")
ax.set_title("감마 frailty($\\sigma^2=0.25$)에서 생존자 집단의 평균 허약도")
ax.legend(loc="lower left", frameon=False)
fs.save(fig, "ch01_fig3.png")
