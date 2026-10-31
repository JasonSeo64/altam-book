# -*- coding: utf-8 -*-
"""제17장 그림: 문항 유형별 답안 구조(개념도), Excel 문항의 표준 레이아웃(개념도), 출제 비중과 12주 계획."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_style import new, save, COLORS, STYLES, MARKERS, plt
from matplotlib.patches import FancyBboxPatch, Rectangle


def box(ax, x, y, w, h, text, fc="white", fs=8.5, hatch=None, ec="#333333"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.0, hatch=hatch))
    kw = dict(bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none")) if hatch else {}
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, **kw)


def arr(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#333333"))


# ---------- 그림 17-1: 답안 구조 ----------
fig, ax = new(h=3.2)
ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
rows = [
    ("'Show that'", ["식을 기호로", "정밀값 대입\n(5자리 이상)", "요구 자릿수로\n결과·일치 확인", "뒤 문항은\n주어진 반올림 값"], 4.6, "#E8EEF4"),
    ("Calculate", ["식", "중간값", "최종값·단위", "앞 답 사용 시\n'(a) 결과 사용'"], 2.6, "white"),
    ("Critique", ["가정 진술", "현실과의 차이와\n영향 방향", "대안 제시"], 0.6, "#FBEBDD"),
]
for name, steps, y, fc in rows:
    box(ax, 0.05, y, 1.6, 1.2, name, fc="#DDDDDD", fs=9)
    n = len(steps); w = (10 - 2.1 - 0.15 - 0.35 * (n - 1)) / n
    x = 2.1
    arr(ax, 1.65, y + 0.6, x, y + 0.6)
    for k, s in enumerate(steps):
        box(ax, x, y, w, 1.2, s, fc=fc)
        if k < n - 1:
            arr(ax, x + w, y + 0.6, x + w + 0.35, y + 0.6)
        x += w + 0.35
save(fig, "ch17_fig1.png")

# ---------- 그림 17-2: Excel 레이아웃 ----------
fig, ax = new(h=3.4)
ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
# 격자 느낌의 시트 바탕
for c in range(13):
    ax.plot([c, c], [0.3, 7.7], color="#EEEEEE", lw=0.6, zorder=0)
for r_ in range(9):
    ax.plot([0, 12], [0.3 + r_ * 0.925, 0.3 + r_ * 0.925], color="#EEEEEE", lw=0.6, zorder=0)
box(ax, 0.2, 2.2, 2.8, 5.3, "입력\n(A1:B15)\n\n이자율, 전이력 모수,\n사업비, 보험금\n\n이름 정의", fc="#E8EEF4", fs=8)
box(ax, 3.6, 0.5, 5.6, 5.0, "계산표 (D열부터)\n\n한 행 = 한 시점(나이)\n열 = 확률·현금흐름·준비금\n\n수식은 입력 셀을 참조", fc="white", fs=8)
box(ax, 3.6, 5.9, 5.6, 1.6, "결과: 요구된 값 + 라벨 + 단위", fc="#FBEBDD", fs=8, hatch="///")
box(ax, 9.6, 2.2, 2.2, 5.3, "검산\n\n확률 합 = 1\n경계조건\n주어진 값과\n차이", fc="#E6F3F1", fs=8)
arr(ax, 3.0, 4.8, 3.6, 4.0)
arr(ax, 6.4, 5.5, 6.4, 5.9)
arr(ax, 9.2, 6.7, 9.6, 6.0)
save(fig, "ch17_fig2.png")

# ---------- 그림 17-3: 출제 비중과 12주 계획 ----------
topics = ["Topic 1 생존모형", "Topic 2 보험료·준비금", "Topic 3 연생", "Topic 4 수익성 분석",
          "Topic 5 퇴직연금", "Topic 6 유니버설보험", "Topic 7 내재옵션"]
lo = [10, 12, 8, 10, 10, 10, 10]; hi = [20, 20, 16, 20, 18, 18, 18]   # 본문 17.6 표·실라버스 비중
weeks = {0: [1, 2, 3], 1: [4, 5], 2: [6], 3: [7], 4: [8], 5: [9], 6: [10]}  # 본문 17.6 표
fig, (a1, a2) = new(h=3.4, ncols=2, gridspec_kw=dict(width_ratios=[1, 1.15]))
y = list(range(len(topics)))[::-1]
for yi, l, h in zip(y, lo, hi):
    a1.plot([l, h], [yi, yi], color=COLORS[0], lw=5, solid_capstyle="butt")
    a1.plot([(l + h) / 2], [yi], "D", color="white", mec=COLORS[0], ms=5)
    a1.text(h + 0.5, yi, f"{l}–{h}%", va="center", fontsize=7.5)
a1.set_yticks(y); a1.set_yticklabels(topics, fontsize=7.5)
a1.set_xlim(5, 25); a1.set_xlabel("출제 비중(%)"); a1.set_title("(a) 토픽별 비중 범위(◇ 중간값)")
for k, yi in enumerate(y):
    for w_ in weeks[k]:
        a2.add_patch(Rectangle((w_ - 0.45, yi - 0.3), 0.9, 0.6, fc=COLORS[0], ec="white"))
for w_ in (11, 12):
    a2.add_patch(Rectangle((w_ - 0.45, -0.4), 0.9, len(topics) - 0.2, fc="white", ec=COLORS[1], hatch="///"))
for w_, lab in ((11, "기출 서술형(17.5)"), (12, "모의고사 2회")):
    a2.text(w_, (len(topics) - 1.6) / 2, lab, ha="center", va="center", rotation=90, fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
a2.set_xlim(0.4, 12.6); a2.set_ylim(-0.6, len(topics) - 0.4)
a2.set_xticks(range(1, 13)); a2.set_yticks(y); a2.set_yticklabels([t.split()[0] + " " + t.split()[1] for t in topics], fontsize=7.5)
a2.set_xlabel("주"); a2.set_title("(b) 12주 학습 계획"); a2.grid(False)
fig.tight_layout()
save(fig, "ch17_fig3.png")
print("done")
