# -*- coding: utf-8 -*-
"""제8장 그림: 실행은 책 폴더에서  python3 code/figs_ch08.py
그림 8-1 다중상태 연생모형의 상태전이도(개념도)
그림 8-2 예제 8-4 SULT (60)·(65)의 단일·동시생존·최종생존 생존확률
그림 8-3 예제 8-5 최종생존 보험의 상태별 준비금
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fig_style import new, save, COLORS, STYLES, MARKERS, won, plt
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------- 그림 8-1
fig, ax = new(6.3, 3.4)
ax.set_xlim(-0.1, 10.1); ax.set_ylim(0, 6); ax.axis("off")
pos = {0: (1.3, 2.5), 1: (5.0, 4.4), 2: (5.0, 0.6), 3: (8.7, 2.5)}
txt = {0: "상태 0\n두 사람 모두 생존", 1: "상태 1\n$(x)$만 생존", 2: "상태 2\n$(y)$만 생존", 3: "상태 3\n두 사람 모두 사망"}
W_, H_ = 2.3, 1.0
for k, (x, y) in pos.items():
    ax.add_patch(FancyBboxPatch((x - W_ / 2, y - H_ / 2), W_, H_, boxstyle="round,pad=0.05",
                                fc="#EEF2F6" if k < 3 else "#DDDDDD", ec=COLORS[0], lw=1.2))
    ax.text(x, y, txt[k], ha="center", va="center", fontsize=8.5)
def arr(a, b, lab, off=(0, 0), rad=0.0):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.annotate("", xy=(x2 - np.sign(x2 - x1) * W_ / 2 * (abs(x2 - x1) > 1) , y2 - np.sign(y2 - y1) * H_ / 2 * (abs(y2 - y1) > 1) * 0.0),
                xytext=(x1 + np.sign(x2 - x1) * W_ / 2, y1 + (y2 - y1) * 0.12),
                arrowprops=dict(arrowstyle="->", lw=1.3, color=COLORS[0], connectionstyle=f"arc3,rad={rad}"))
    mx, my = (x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1]
    ax.text(mx, my, lab, fontsize=8.5, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.5))
arr(0, 1, r"$\mu^{01}_t$" "\n($(y)$ 사망)", off=(-0.3, 0.35))
arr(0, 2, r"$\mu^{02}_t$" "\n($(x)$ 사망)", off=(-0.3, -0.35))
arr(0, 3, r"$\mu^{03}_t$ (동시사망)", off=(0.0, 0.0))
arr(1, 3, r"$\mu^{13}_t$", off=(0.25, 0.2))
arr(2, 3, r"$\mu^{23}_t$", off=(0.25, -0.2))
ax.text(5.0, 5.75, "독립: $\\mu^{03}=0,\\ \\mu^{13}=\\mu^{02},\\ \\mu^{23}=\\mu^{01}$     공통충격: $\\mu^{03}=\\lambda$     상실 효과: $\\mu^{13}>\\mu^{02},\\ \\mu^{23}>\\mu^{01}$",
        ha="center", fontsize=7.5)
save(fig, "ch08_fig1.png")

# ---------------------------------------------------------------- SULT
A, B, c, i = 0.00022, 2.7e-6, 1.124, 0.05
v = 1 / (1 + i)
def tp(x, t):
    return np.exp(-A * t - B / np.log(c) * c ** x * (c ** t - 1))
K = np.arange(0, 121)
def ann(x, y=None):  # 연초급 종신연금, y가 있으면 독립 동시생존
    p = tp(x, K) * (tp(y, K) if y is not None else 1)
    return np.sum(v ** K * p)
def Ax(x):
    return 1 - (i / (1 + i)) * ann(x)
a60, a65, a6065 = ann(60), ann(65), ann(60, 65)
A6065 = 1 - (i / (1 + i)) * a6065
Alast = Ax(60) + Ax(65) - A6065
P2 = 100000 * Alast / a6065
print("그림8-2 a60=%.4f a65=%.4f a60:65=%.4f  (본문 14.9041 13.5498 12.3738)" % (a60, a65, a6065))
print("        A60:65=%.5f A_last=%.5f P(2)=%.2f  (본문 0.41077 0.23428 1,893.38)" % (A6065, Alast, P2))

t = np.linspace(0, 50, 501)
p60, p65 = tp(60, t), tp(65, t)
pj = p60 * p65; pl = p60 + p65 - pj
fig, ax = new()
ax.plot(t, pl, color=COLORS[0], ls=STYLES[0], label=r"최종생존 ${}_tp_{\overline{60:65}}$")
ax.plot(t, p60, color=COLORS[3], ls=STYLES[3], label=r"$(60)$ 단일생명 ${}_tp_{60}$")
ax.plot(t, p65, color=COLORS[2], ls=STYLES[2], label=r"$(65)$ 단일생명 ${}_tp_{65}$")
ax.plot(t, pj, color=COLORS[1], ls=STYLES[1], label=r"동시생존 ${}_tp_{60:65}$")
ax.fill_between(t, pj, pl, color=COLORS[4], alpha=0.10)
ax.annotate("음영: 한 사람만 생존\n(상태 1 또는 2)", xy=(36, 0.14), xytext=(40, 0.42), fontsize=8, ha="center",
            arrowprops=dict(arrowstyle="->", color=COLORS[2]))
ax.set_xlabel("경과시간 $t$ (년)"); ax.set_ylabel("생존확률"); ax.set_xlim(0, 50); ax.set_ylim(0, 1.02)
ax.legend(frameon=False, loc="upper right")
save(fig, "ch08_fig2.png")

# ---------------------------------------------------------------- 그림 8-3
ts = np.arange(0, 46)
V0 = [100000 * (Ax(60 + s) + Ax(65 + s) - (1 - (i / (1 + i)) * ann(60 + s, 65 + s))) - P2 * ann(60 + s, 65 + s) for s in ts]
V1 = [100000 * Ax(60 + s) for s in ts]
V2 = [100000 * Ax(65 + s) for s in ts]
print("그림8-3 10V0=%.2f 10V1=%.2f 10V2=%.2f  (본문 19,407.78 42,817.60 50,867.69)" % (V0[10], V1[10], V2[10]))
fig, ax = new()
ax.plot(ts, V2, color=COLORS[1], ls=STYLES[1], marker=MARKERS[1], ms=3, markevery=5, label=r"$(y)$만 생존 ${}_tV^{(2)}=100{,}000\,A_{65+t}$")
ax.plot(ts, V1, color=COLORS[3], ls=STYLES[3], marker=MARKERS[3], ms=3, markevery=5, label=r"$(x)$만 생존 ${}_tV^{(1)}=100{,}000\,A_{60+t}$")
ax.plot(ts, V0, color=COLORS[0], ls=STYLES[0], marker=MARKERS[0], ms=3, markevery=5, label=r"둘 다 생존 ${}_tV^{(0)}$")
for vv in (V1[10], V2[10]):
    ax.annotate("", xy=(10, vv), xytext=(10, V0[10]), arrowprops=dict(arrowstyle="->", color=COLORS[2], lw=1))
ax.text(10.8, 8000, "$t=10$에서 첫 사망 시\n준비금 급증", fontsize=8)
ax.set_xlabel("경과시간 $t$ (년, 나이 $60+t$·$65+t$)"); ax.set_ylabel("상태별 준비금"); won(ax)
ax.set_xlim(0, 45); ax.set_ylim(0, 100000)
ax.legend(frameon=False, loc="upper left", fontsize=7.5)
save(fig, "ch08_fig3.png")
