# -*- coding: utf-8 -*-
"""제12장 그림: 12-1 적립금 점화식의 흐름(개념도), 12-2 Type A·Type B의 COI와 사망급부 구성(예제 12-1·12-2),
12-3 코리더와 사망급부(예제 12-3)
실행: 책 폴더에서 python3 code/figs_ch12.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import plt, new, save, COLORS, STYLES, MARKERS
from matplotlib.patches import FancyBboxPatch
import numpy as np

FMT = plt.FuncFormatter(lambda v, p: f"{v:,.0f}")

# ---------- 예제 12-1, 12-2 ----------
FA, P, iq, ic = 100000.0, 3000.0, 0.04, 0.045
qs = [0.0020, 0.0022, 0.0024]; SC = [2000, 1500, 1000]
E = 0.03 * P + 150
vq = 1 / (1 + iq)
AVa, COIa, AVb, COIb = [], [], [], []
av = 0.0
for t in range(3):
    X = av + P - E
    coi = qs[t] * vq * (FA - X * (1 + ic)) / (1 - qs[t] * vq * (1 + ic))
    av = (X - coi) * (1 + ic); COIa.append(coi); AVa.append(av)
av = 0.0
for t in range(3):
    X = av + P - E
    coi = qs[t] * vq * FA
    av = (X - coi) * (1 + ic); COIb.append(coi); AVb.append(av)
print("Type A COI", [round(x, 2) for x in COIa], "AV", [round(x, 2) for x in AVa])
print("Type B COI", [round(x, 2) for x in COIb], "AV", [round(x, 2) for x in AVb], f"3년차 AV 차이 {AVa[2] - AVb[2]:.2f}")

# ---------- 예제 12-3 ----------
AV0, E3, q3, gam = 60000.0, 150.0, 0.02, 1.9
X3 = AV0 - E3
coi_nc = q3 * vq * (FA - X3 * (1 + ic)) / (1 - q3 * vq * (1 + ic))
av_nc = (X3 - coi_nc) * (1 + ic)
coi_c = q3 * vq * (gam - 1) * X3 * (1 + ic) / (1 + q3 * vq * (gam - 1) * (1 + ic))
av_c = (X3 - coi_c) * (1 + ic)
print(f"예제 12-3: 코리더 무시 AV {av_nc:,.2f} COI {coi_nc:,.2f} / 코리더 COI {coi_c:,.2f} AV {av_c:,.2f} DB {gam * av_c:,.2f}")


# ---------- 그림 12-1 ----------
def box(ax, x, y, w, h, text, fc="#FFFFFF", ec=COLORS[0], bold=False, fs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, text=None, off=(0, 0.1), color=COLORS[0]):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2))
    if text:
        ax.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], text, ha="center", va="bottom", fontsize=8)


fig, ax = new(6.3, 2.9)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off"); ax.grid(False)
box(ax, 0.1, 2.6, 1.7, 0.9, "전년도 적립금\n$AV_{t-1}$")
box(ax, 0.1, 1.2, 1.7, 0.9, "보험료 $P_t$")
box(ax, 2.6, 1.7, 1.9, 1.3, "$X_t=$\n$AV_{t-1}+P_t-E_t$", fc="#EAF0F6")
arrow(ax, 1.8, 3.05, 2.6, 2.6); arrow(ax, 1.8, 1.65, 2.6, 2.1)
box(ax, 2.7, 0.1, 1.7, 0.8, "사업비 공제 $E_t$", fc="#F2F2F2")
arrow(ax, 3.55, 1.7, 3.55, 0.9)
box(ax, 5.3, 1.7, 1.9, 1.3, "$X_t-COI_t$", fc="#EAF0F6")
arrow(ax, 4.5, 2.35, 5.3, 2.35)
box(ax, 5.35, 0.1, 1.8, 0.8, "위험보험료 $COI_t$", fc="#F2F2F2")
arrow(ax, 6.25, 1.7, 6.25, 0.9)
box(ax, 8.0, 1.7, 1.9, 1.3, "적립금 $AV_t$", fc="#FBE9D7", ec=COLORS[1], bold=True)
arrow(ax, 7.2, 2.35, 8.0, 2.35)
ax.text(7.6, 2.45, "$\\times(1+i^c_t)$", ha="center", va="bottom", fontsize=7.5)
ax.annotate("", xy=(6.25, 0.6), xytext=(8.95, 1.7),
            arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=1.0, ls="--", connectionstyle="arc3,rad=-0.25"))
ax.text(8.95, 3.35, "Type A: NAR $=FA-AV_t$\nCOI가 $AV_t$에 의존(순환)", fontsize=7.5, ha="center", va="bottom", color=COLORS[2])
save(fig, "ch12_fig1.png")

# ---------- 그림 12-2 ----------
yrs = np.arange(1, 4)
fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.1), gridspec_kw=dict(width_ratios=[1, 1.25]))
ax = axs[0]
ax.plot(yrs, COIa, color=COLORS[0], ls=STYLES[0], marker=MARKERS[0], label="Type A")
ax.plot(yrs, COIb, color=COLORS[1], ls=STYLES[1], marker=MARKERS[1], label="Type B")
for y, a, b in zip(yrs, COIa, COIb):
    ax.text(y, a - 3, f"{a:.2f}", ha="center", va="top", fontsize=7)
    ax.text(y, b + 3, f"{b:.2f}", ha="center", va="bottom", fontsize=7)
ax.set_xticks(yrs); ax.set_xlabel("보험연도 $t$"); ax.set_ylabel("COI")
ax.set_ylim(170, 245); ax.set_xlim(0.6, 3.4)
ax.set_title("(a) 위험보험료(COI)", fontsize=9)
ax.legend(frameon=False, loc="upper left")
ax = axs[1]
w = 0.36
NARa = [FA - a for a in AVa]
ax.bar(yrs - w / 2, AVa, width=w, color=COLORS[0], label="적립금 $AV_t$")
ax.bar(yrs - w / 2, NARa, bottom=AVa, width=w, color="white", edgecolor=COLORS[0], hatch="///", label="위험보험금(NAR)")
ax.bar(yrs + w / 2, AVb, width=w, color=COLORS[0])
ax.bar(yrs + w / 2, [FA] * 3, bottom=AVb, width=w, color="white", edgecolor=COLORS[0], hatch="///")
for y in yrs:
    ax.text(y - w / 2, FA + 1500, "A", ha="center", fontsize=8)
    ax.text(y + w / 2, FA + AVb[y - 1] + 1500, "B", ha="center", fontsize=8)
ax.set_xticks(yrs); ax.set_xlabel("보험연도 $t$"); ax.set_ylabel("사망급부")
ax.yaxis.set_major_formatter(FMT)
ax.set_ylim(0, 140000)
ax.set_title("(b) 사망급부 = 적립금 + NAR", fontsize=9)
ax.legend(frameon=False, loc="upper center", ncol=2, fontsize=7.5)
ax.grid(axis="x", visible=False)
fig.tight_layout()
save(fig, "ch12_fig2.png")

# ---------- 그림 12-3 ----------
avs = np.linspace(0, 80000, 401)
fig, ax = new(6.3, 3.2)
ax.plot(avs, np.maximum(FA, gam * avs), color=COLORS[0], ls=STYLES[0], label="사망급부 $\\max(FA,\\ \\gamma AV)$")
ax.plot(avs, np.maximum(FA, gam * avs) - avs, color=COLORS[1], ls=STYLES[1], label="위험보험금(NAR)")
ax.plot(avs, avs, color=COLORS[2], ls=STYLES[3], lw=1.0, label="적립금 $AV$")
th = FA / gam
ax.axvline(th, color=COLORS[2], lw=0.8, ls=":")
ax.text(th - 800, 8000, f"$FA/\\gamma$ = {th:,.0f}", ha="right", fontsize=8)
ax.plot([av_c], [gam * av_c], marker=MARKERS[0], color=COLORS[1], ms=6, ls="none")
ax.annotate(f"예제 12-3: $AV$ = {av_c:,.2f}\n사망급부 = {gam * av_c:,.2f}", xy=(av_c, gam * av_c),
            xytext=(61500, 88000), fontsize=7.5, arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.8))
ax.text(th + 1000, 145000, "코리더 적용 구간", fontsize=8)
ax.text(4000, 145000, "코리더 미적용 구간", fontsize=8)
ax.set_xlabel("연말 적립금 $AV$"); ax.set_ylabel("금액")
ax.xaxis.set_major_formatter(FMT); ax.yaxis.set_major_formatter(FMT)
ax.set_ylim(0, 160000)
ax.legend(frameon=False, loc="lower right", fontsize=7.5)
save(fig, "ch12_fig3.png")
print("ok")
