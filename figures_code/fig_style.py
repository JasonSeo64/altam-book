# -*- coding: utf-8 -*-
"""교재 공통 그림 스타일(교재제작표준 11.1절). 모든 책의 figs_chNN.py가 import한다.
- 글꼴: Noto Sans CJK KR, 흑백 인쇄에서도 구분되도록 선 모양·표식을 함께 쓴다.
- 저장: <책 폴더>/figures/chNN_figK.png (300dpi, 폭 16cm 기준). 책 폴더에서 실행하거나 환경변수 FIG_DIR로 지정
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

for f in font_manager.findSystemFonts():
    if "NotoSansCJK-Regular" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({
    "font.family": "Noto Sans CJK KR",
    "axes.unicode_minus": True,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.6,
    "lines.linewidth": 1.6,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# 인쇄 친화 팔레트 (진한 남색, 주황, 회색, 청록, 자주)
COLORS = ["#1F3B57", "#D9822B", "#7F7F7F", "#2A9D8F", "#8E4585"]
STYLES = ["-", "--", "-.", ":", (0, (5, 1, 1, 1))]
MARKERS = ["o", "s", "^", "D", "v"]

FIG_DIR = os.environ.get("FIG_DIR") or os.path.join(os.getcwd(), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

W, H = 6.3, 3.4   # 인치 (약 16cm × 8.6cm)


def new(w=W, h=H, **kw):
    return plt.subplots(figsize=(w, h), **kw)


def _fix_minus(fig):
    """그림 안 글자의 음수 부호를 「−」(U+2212)로 통일한다(표준 9.1절). 수식($…$) 안은 그대로 둔다."""
    import re
    from matplotlib.text import Text
    pat = re.compile(r"(?<![\w$])-(?=\d)")
    for t in fig.findobj(Text):
        s = t.get_text()
        if s and "-" in s:
            parts = re.split(r"(\$[^$]*\$)", s)
            t.set_text("".join(p if p.startswith("$") else pat.sub("\u2212", p) for p in parts))


def save(fig, name):
    _fix_minus(fig)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path)
    plt.close(fig)
    return path


def won(ax, axis="y", unit=1):
    """천 단위 쉼표 눈금 (unit=1e4 이면 만원)"""
    from matplotlib.ticker import FuncFormatter
    fmt = FuncFormatter(lambda v, p: f"{v/unit:,.0f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)
