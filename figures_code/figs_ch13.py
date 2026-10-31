# -*- coding: utf-8 -*-
"""제13장 그림: 13-1 최소 보험료 G와 NLG 준비금(예제 13-1), 13-2 연도별 이익의 원천별 분해(예제 13-2),
13-3 스트레스 시나리오별 NPV(13.5.1절 표)
실행: 책 폴더에서 python3 code/figs_ch13.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import plt, new, save, COLORS, STYLES, MARKERS
import numpy as np


def m(txt):
    return txt.replace("-", "−")


FMT = plt.FuncFormatter(lambda v, p: m(f"{v:,.0f}"))

# ---------- 예제 13-1 ----------
DB, A55, a55, AV = 100000.0, 0.235, 16.06, 2000.0


def W(G):
    return DB * A55 - G * a55


G0 = DB * A55 / a55
print(f"예제 13-1: W(1200)={W(1200):,.0f} NLG={max(W(1200) - AV, 0):,.0f}  W(1500)={W(1500):,.0f}  평준순보험료={G0:,.0f}")

# ---------- 예제 13-2 모형 ----------
ADB, P0, iq, ic, r = 100000.0, 3000.0, 0.04, 0.045, 0.10
SC = [2000, 1500, 1000, 500, 0]
QA = [0.0015, 0.0017, 0.0019, 0.0021, 0.0023]
WL = [0.10, 0.08, 0.06, 0.05, 1.0]          # 5년차 말 잔존 계약 전부 해약


def project(P=P0, qmult=1.0, ie=0.06, wmult=1.0):
    E = 0.03 * P + 150
    av = 0.0; pr = []; comp = []; surv = 1.0; sig = []
    for t in range(5):
        qs = 0.0020 + 0.0002 * t
        X = av + P - E
        coi = qs * ADB / (1 + iq)
        av_new = (X - coi) * (1 + ic)
        cv = max(av_new - SC[t], 0.0)
        Ea = 1200.0 if t == 0 else 80.0
        qa = QA[t] * qmult
        w = WL[t] * (wmult if t < 4 else 1.0)
        p = 1 - qa
        prt = (av + P - Ea) * (1 + ie) - qa * (av_new + ADB) - p * w * cv - p * (1 - w) * av_new
        comp.append((X * (ie - ic), (E - Ea) * (1 + ie), coi * (1 + ic) - qa * ADB, p * w * (av_new - cv)))
        pr.append(prt); sig.append(surv * prt)
        surv *= p * (1 - w)
        av = av_new
    npv = sum(s / (1 + r) ** (t + 1) for t, s in enumerate(sig))
    return pr, sig, comp, npv


pr, sig, comp, npv = project()
print("Pr", [round(x, 2) for x in pr], "NPV", round(npv, 2))
print("2년차 분해", [round(x, 2) for x in comp[1]], "합", round(sum(comp[1]), 2))
for t in range(5):
    assert abs(sum(comp[t]) - pr[t]) < 0.02, (t, sum(comp[t]), pr[t])

scen = [("최선추정", {}), ("사망률 ×1.2", dict(qmult=1.2)), ("운용수익률 5%", dict(ie=0.05)),
        ("해약률 ×1.5\n(1–4년차)", dict(wmult=1.5)), ("해약률 ×0.5\n(1–4년차)", dict(wmult=0.5)),
        ("결합 스트레스", dict(qmult=1.2, wmult=1.5, ie=0.05))]
snpv = [project(**kw)[3] for _, kw in scen]
print("시나리오 NPV", [round(x, 2) for x in snpv])

# ---------- 그림 13-1 ----------
Gs = np.linspace(800, 1800, 201)
fig, ax = new(6.3, 3.2)
ax.plot(Gs, [W(g) for g in Gs], color=COLORS[2], ls=STYLES[1], label="보증 의무의 가치 ${}_tW^{\\mathrm{G}}$")
ax.plot(Gs, [max(W(g), AV) for g in Gs], color=COLORS[0], ls=STYLES[0], lw=2.0, label="총준비금 $\\max({}_tW^{\\mathrm{G}},\\ AV_t)$")
ax.axhline(AV, color=COLORS[1], ls=STYLES[3], lw=1.0, label="적립금 $AV_t$ = 2,000")
ax.axhline(0, color="black", lw=0.8)
ax.fill_between(Gs, AV, [max(W(g), AV) for g in Gs], color=COLORS[0], alpha=0.12, hatch="///", label="NLG 준비금")
ax.plot([1200], [W(1200)], marker=MARKERS[0], color=COLORS[0], ms=6, ls="none")
ax.annotate(f"$G$ = 1,200: 총준비금 {W(1200):,.0f}\n(NLG 준비금 {W(1200) - AV:,.0f})", xy=(1200, W(1200)),
            xytext=(830, -3300), fontsize=8, arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.8))
ax.axvline(G0, color=COLORS[2], lw=0.8, ls=":")
ax.text(G0 - 15, -2600, f"평준순보험료\n{G0:,.0f}", fontsize=8, ha="right")
ax.set_xlabel("최소 보험료 $G$"); ax.set_ylabel("금액")
ax.xaxis.set_major_formatter(FMT); ax.yaxis.set_major_formatter(FMT)
ax.set_ylim(-4500, 11000)
ax.legend(frameon=False, loc="upper right", fontsize=7.5)
save(fig, "ch13_fig1.png")

# ---------- 그림 13-2 ----------
yrs = np.arange(1, 6)
names = ["이차(스프레드)", "비차", "사차", "해약 이익"]
hatches = ["", "///", "...", "xx"]
fcs = [COLORS[0], "white", "white", "white"]
ecs = [COLORS[0], COLORS[1], COLORS[0], COLORS[2]]
fig, ax = new(6.3, 3.3)
pos = np.zeros(5); neg = np.zeros(5)
for k in range(4):
    vals = np.array([comp[t][k] for t in range(5)])
    bottoms = np.where(vals >= 0, pos, neg)
    ax.bar(yrs, vals, bottom=bottoms, width=0.55, color=fcs[k], edgecolor=ecs[k], hatch=hatches[k], label=names[k])
    pos += np.where(vals >= 0, vals, 0); neg += np.where(vals < 0, vals, 0)
ax.plot(yrs, pr, color=COLORS[1], ls="none", marker=MARKERS[3], ms=6, label="이익 $Pr_t$(합계)")
for t in range(5):
    ax.text(yrs[t] + 0.32, pr[t], m(f"{pr[t]:,.2f}"), va="center", fontsize=7.5)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(yrs); ax.set_xlabel("보험연도 $t$"); ax.set_ylabel("연초 유효계약 1건당 이익")
ax.yaxis.set_major_formatter(FMT)
ax.set_xlim(0.5, 5.9)
ax.legend(frameon=False, loc="lower right", ncol=3, fontsize=7.5)
ax.set_ylim(-1350, 700)
ax.grid(axis="x", visible=False)
save(fig, "ch13_fig2.png")

# ---------- 그림 13-3 ----------
labels = [s for s, _ in scen]
fig, ax = new(6.3, 3.2)
y = np.arange(len(labels))[::-1]
for k, (yy, v) in enumerate(zip(y, snpv)):
    style = dict(color=COLORS[0]) if k == 0 else dict(color="white", edgecolor=COLORS[0], hatch="///")
    ax.barh(yy, v, height=0.6, **style)
    ax.text(v + 6, yy, f"{v:,.2f}", va="center", fontsize=8)
ax.axvline(snpv[0], color=COLORS[2], lw=0.8, ls=":")
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("NPV(위험할인율 10%, 판매 계약 1건당)")
ax.set_xlim(0, 440)
ax.grid(axis="y", visible=False)
save(fig, "ch13_fig3.png")
print("ok")
