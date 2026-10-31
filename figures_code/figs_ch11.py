# -*- coding: utf-8 -*-
"""제11장 그림: 11-1 임금상승률별 소득대체율(예제 11-1), 11-2 서비스표의 재직자와 탈퇴(예제 11-4),
11-3 나이별 TUC·PUC 정상부담금(예시: 30세 입사, 임금상승 3%, 적립률 1.5%, 65세 정년, SULT 사망률, i=5%)
실행: 책 폴더에서 python3 code/figs_ch11.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import plt, new, save, COLORS, STYLES, MARKERS
import numpy as np


def m(txt):
    return txt.replace("-", "−")


# ---------- 예제 11-1 ----------
alpha, n = 0.015, 35


def ratios(g, j=0.02):
    fas = alpha * n * sum((1 + g) ** -k for k in range(3)) / 3
    cae = alpha * sum((1 + g) ** -k for k in range(n))
    care = alpha * sum(((1 + j) / (1 + g)) ** k for k in range(n))
    return fas, cae, care


print("예제 11-1 (g=3%%): FAS %.4f  CAE %.4f  CARE %.4f" % ratios(0.03))

# ---------- 예제 11-4 ----------
lx = [100000.0]; dx = []; rx = []
for k, qd in enumerate([0.010, 0.011, 0.012, 0.013, 0.014]):
    d = lx[-1] * qd; r = lx[-1] * 0.10
    dx.append(d); rx.append(r); lx.append(lx[-1] - d - r)
rx.append(lx[-1])
print("예제 11-4 l_x", [round(x, 1) for x in lx], " l65/l60=%.5f  sum d/l60=%.5f" % (lx[-1] / lx[0], sum(dx) / lx[0]))

# ---------- 예제 11-6 확인 ----------
F = 1.05 ** -10 * 0.92 * 13.5
S, g = 60000.0, 0.03
tuc_aal = alpha * 25 * S * F; tuc_nc = alpha * 26 * S * (1 + g) * F - tuc_aal
Sh = S * (1 + g) ** 10
puc_aal = alpha * 25 * Sh * F; puc_nc = alpha * Sh * F
print(f"예제 11-6: F={F:.5f} TUC AAL {tuc_aal:,.0f} NC {tuc_nc:,.0f} / PUC AAL {puc_aal:,.0f} NC {puc_nc:,.0f}")

# ---------- 그림 11-1 ----------
gs = np.linspace(0.0, 0.06, 61)
R = np.array([ratios(x) for x in gs])
fig, ax = new(6.3, 3.2)
names = ["최종평균임금(FAS, 3년)", "경력평균임금(CAE)", "재평가 경력평균임금(CARE, 재평가율 2%)"]
for k in range(3):
    ax.plot(gs * 100, R[:, k] * 100, color=COLORS[k], ls=STYLES[k], label=names[k])
    ax.plot([3], [ratios(0.03)[k] * 100], marker=MARKERS[k], color=COLORS[k], ms=5, ls="none")
    ax.annotate(f"{ratios(0.03)[k] * 100:.2f}%", xy=(3, ratios(0.03)[k] * 100),
                xytext=(3.15, ratios(0.03)[k] * 100 + (1.5 if k != 1 else -5.5)), fontsize=8)
ax.axvline(3, color=COLORS[2], lw=0.8, ls=":")
ax.set_xlabel("임금상승률 $g$ (%)"); ax.set_ylabel("소득대체율 (%)")
ax.set_ylim(20, 80)
ax.legend(frameon=False, loc="upper right")
save(fig, "ch11_fig1.png")

# ---------- 그림 11-2 ----------
ages = np.arange(60, 66)
fig, ax = new(6.3, 3.2)
ax.bar(ages, lx, width=0.6, color="white", edgecolor=COLORS[0], hatch="///", label="연초 재직자 $l_x$")
ax.bar(ages[:-1] + 0.5, rx[:-1], width=0.35, color=COLORS[1], label="조기퇴직 $r_x$")
ax.bar(ages[:-1] + 0.5, dx, bottom=rx[:-1], width=0.35, color=COLORS[2], label="재직 중 사망 $d_x$")
ax.annotate(f"65세 정년 일괄 퇴직\n{lx[-1]:,.1f}명", xy=(65, lx[-1]), xytext=(63.6, 88000), fontsize=8,
            arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.8))
ax.set_xticks(ages); ax.set_xticklabels([f"{a}세" for a in ages])
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:,.0f}"))
ax.set_ylabel("인원(명)")
ax.set_ylim(0, 112000)
ax.legend(frameon=False, loc="upper right", ncol=3, fontsize=7.5)
ax.grid(axis="x", visible=False)
save(fig, "ch11_fig2.png")

# ---------- 그림 11-3 (예시) ----------
A, B, c = 0.00022, 2.7e-6, 1.124


def q(x):
    return 1 - math.exp(-(A + B * c ** x * (c - 1) / math.log(c)))


def npx(x, k):
    p = 1.0
    for j in range(k):
        p *= 1 - q(x + j)
    return p


v = 1 / 1.05
a65 = sum(v ** k * npx(65, k) for k in range(0, 120 - 65))
entry, ret = 30, 65
xs = np.arange(entry, ret)
tuc, puc = [], []
for x in xs:
    Fx = v ** (ret - x) * npx(x, ret - x) * a65
    Sx = 1.03 ** (x - entry)                  # 30세 임금 = 1
    Sfin = 1.03 ** (ret - 1 - entry)          # 퇴직 직전 1년 임금
    nsv = x - entry
    tuc.append((alpha * (nsv + 1) * Sx * 1.03 - alpha * nsv * Sx) * Fx / Sx)   # 현재 임금 대비
    puc.append(alpha * Sfin * Fx / Sx)
tuc = np.array(tuc); puc = np.array(puc)
cross = xs[np.argmax(tuc > puc)]
print(f"예시 a65(SULT,5%)={a65:.4f}, TUC NC가 PUC NC를 넘는 첫 나이 {cross}")
fig, ax = new(6.3, 3.2)
ax.plot(xs, puc / 1.0 * 100, color=COLORS[0], ls=STYLES[0], label="PUC 정상부담금")
ax.plot(xs, tuc * 100, color=COLORS[1], ls=STYLES[1], label="TUC 정상부담금")
ax.axvline(cross, color=COLORS[2], lw=0.8, ls=":")
ax.text(cross + 0.4, max(tuc * 100) * 0.85, f"{cross}세 무렵부터\nTUC > PUC", fontsize=8)
ax.set_xlabel("가입자 나이 $x$"); ax.set_ylabel("정상부담금 (현재 임금 대비, %)")
ax.legend(frameon=False, loc="upper left")
save(fig, "ch11_fig3.png")
print("ok")
