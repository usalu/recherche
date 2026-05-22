"""Scalability figures from scalability_results.json."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})

HERE = Path(__file__).resolve().parent
OUT = HERE / "report_snapshots"
OUT.mkdir(exist_ok=True)
data = json.loads((HERE / "scalability_results.json").read_text(encoding="utf-8"))


def fig_trajectory() -> None:
    order = ["≤2014", "2015–2019", "2020–2024", "2025+"]
    t = data["temporal"]
    xs = [k for k in order if k in t]
    area = [t[k]["median_area"] for k in xs]
    share = [t[k]["median_reuse_share"] for k in xs]
    n = [t[k]["projekte"] for k in xs]
    fig, ax1 = plt.subplots(figsize=(9, 5))
    bars = ax1.bar(xs, area, color="#4C78A8", width=0.6)
    ax1.set_ylabel("Median Projektfläche (m² BGF)", color="#4C78A8")
    ax1.tick_params(axis="y", labelcolor="#4C78A8")
    for b, a, cnt in zip(bars, area, n):
        if a:
            ax1.text(b.get_x() + b.get_width() / 2, a, f"{int(a)} m²\n(n={cnt})",
                     ha="center", va="bottom", fontsize=8)
    ax2 = ax1.twinx()
    sx = [x for x, s in zip(xs, share) if s is not None]
    sy = [s for s in share if s is not None]
    ax2.plot(sx, sy, "o-", color="#E45756", lw=2, ms=8)
    for x, s in zip(sx, sy):
        ax2.text(x, s + 1.5, f"{s:.0f}%", ha="center", color="#E45756", fontsize=9)
    ax2.set_ylabel("Median Reuse-Anteil (%)", color="#E45756")
    ax2.tick_params(axis="y", labelcolor="#E45756")
    ax2.set_ylim(0, 105)
    ax1.set_title("Projekte skalieren in der Größe — die Reuse-Tiefe bleibt hoch\n"
                  "Median-Fläche wächst 255 → 8.725 m², Reuse-Anteil hält 80–92 %", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "DEEP_scal_trajectory.png", dpi=150)
    plt.close(fig)


def fig_sourcing() -> None:
    s = data["sourcing"]
    cats = ["1 Spender\n(Ganzhaus-Transfer)", "2–3 Spender\n(kleine Aggregation)",
            "≥4 Spender\n(echte Aggregation)"]
    vals = [s["single_donor"], s["few_2_3"], s["many_4plus"]]
    colors = ["#E45756", "#F58518", "#54A24B"]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    bars = ax.bar(cats, vals, color=colors)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v, str(v), ha="center", va="bottom", fontsize=11)
    ax.set_ylabel("Anzahl Projekte (mit Spenderbezug)")
    ax.set_title("Der Skalierungs-Engpass: Wiederverwendung ist heute Einzelquellen-Sache\n"
                 f"{s['single_donor']} von {s['projekte_mit_spender']} Projekten beziehen aus nur "
                 "einem Spenderbauwerk", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "DEEP_scal_sourcing.png", dpi=150)
    plt.close(fig)


def main() -> None:
    fig_trajectory()
    fig_sourcing()
    for f in ["DEEP_scal_trajectory.png", "DEEP_scal_sourcing.png"]:
        p = OUT / f
        print(f"{f}: {p.exists()} {p.stat().st_size if p.exists() else 0} bytes")


if __name__ == "__main__":
    main()
