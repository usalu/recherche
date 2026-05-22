"""Render deep-analysis figures from deep_analysis_results.json."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})

HERE = Path(__file__).resolve().parent
OUT = HERE / "report_snapshots"
OUT.mkdir(exist_ok=True)
data = json.loads((HERE / "deep_analysis_results.json").read_text(encoding="utf-8"))


def fig_brokers() -> None:
    bro = data["topology"]["top_betweenness"][:10][::-1]
    arts = {a["name"] for a in data["topology"]["articulation_points"]}
    names = [b["name"] for b in bro]
    vals = [b["betweenness"] for b in bro]
    colors = ["#E45756" if n in arts else "#4C78A8" for n in names]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.barh(names, vals, color=colors)
    for i, b in enumerate(bro):
        ax.text(vals[i] + max(vals) * 0.01, i, f"  Grad {b['degree']} · {b['land'] or '?'}",
                va="center", fontsize=8, color="#333")
    ax.set_xlabel("Betweenness-Zentralität (Brückenfunktion)")
    ax.set_title("Die wahren Brücken des Reuse-Netzwerks\n"
                 "rot = Articulation Point (Wegfall fragmentiert das Netz)", fontsize=11)
    ax.margins(x=0.18)
    fig.tight_layout()
    fig.savefig(OUT / "DEEP_brokers.png", dpi=150)
    plt.close(fig)


def fig_fingerprint() -> None:
    fp = data["material_nachweis_fingerprint"]
    mats = [m for m in ["Stahl", "Holz", "Glas", "Stahlbeton", "Beton", "Ziegel"] if m in fp]
    nw_set: list[str] = []
    for m in mats:
        for item in fp[m]["top_nachweise"]:
            if item["nachweis"] not in nw_set:
                nw_set.append(item["nachweis"])
    short = {
        "ProduktstatusUndLeistungserklaerung": "Produktstatus",
        "Materialpruefung": "Materialprüfung",
        "Standsicherheitsnachweis": "Standsicherheit",
        "U_WertOderEnergieInfo": "U-Wert/Energie",
        "Befestigungsnachweis": "Befestigung",
        "HerkunftsUndRueckbaudokumentation": "Herkunft/Rückbau",
        "HolzschutzmittelCheck": "Holzschutz",
        "SicherheitsglasInfo": "Sicherheitsglas",
        "RcGesteinskoernungEignung": "RC-Gesteinskörnung",
        "DauerhaftigkeitRestlebensdauer": "Restlebensdauer",
    }
    M = np.zeros((len(mats), len(nw_set)))
    for i, m in enumerate(mats):
        amap = {it["nachweis"]: it["anteil"] for it in fp[m]["top_nachweise"]}
        for j, nw in enumerate(nw_set):
            M[i, j] = amap.get(nw, 0.0)
    fig, ax = plt.subplots(figsize=(10, 4.6))
    im = ax.imshow(M, cmap="YlOrRd", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(nw_set)))
    ax.set_xticklabels([short.get(n, n) for n in nw_set], rotation=35, ha="right")
    ax.set_yticks(range(len(mats)))
    ax.set_yticklabels(mats)
    for i in range(len(mats)):
        for j in range(len(nw_set)):
            v = M[i, j]
            if v > 0:
                ax.text(j, i, f"{int(round(v*100))}", ha="center", va="center",
                        color="white" if v > 0.55 else "#333", fontsize=8)
    ax.set_title("Material → Nachweis-Fingerprint (Anteil der Bauteilgruppen, %)\n"
                 "Vorlage für die automatische Nachweis-Vorbelegung im Tool", fontsize=11)
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02, label="Anteil")
    fig.tight_layout()
    fig.savefig(OUT / "DEEP_fingerprint.png", dpi=150)
    plt.close(fig)


def fig_ranges() -> None:
    r = data["performance_ranges"]
    items = [
        ("CO₂-Reduktion (%)", r["co2_reduktion_prozent"]),
        ("Reuse-Anteil (%)", r["reuse_anteil_prozent"]),
    ]
    fig, ax = plt.subplots(figsize=(8, 3.0))
    ys = []
    for k, (lbl, d) in enumerate(items):
        if not d:
            continue
        ax.plot([d["min"], d["max"]], [k, k], color="#72B7B2", lw=6, solid_capstyle="round")
        ax.plot(d["median"], k, "o", color="#E45756", ms=11, zorder=3)
        ax.text(d["min"], k + 0.18, f"{d['min']:.0f}", ha="center", fontsize=8)
        ax.text(d["max"], k + 0.18, f"{d['max']:.0f}", ha="center", fontsize=8)
        ax.text(d["median"], k - 0.28, f"Median {d['median']:.0f}", ha="center",
                fontsize=8, color="#E45756")
        ys.append(lbl)
    ax.set_yticks(range(len(ys)))
    ax.set_yticklabels(ys)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Prozent")
    ax.set_title("Belegte Wirkungsspannen der Wiederverwendung (n je Reihe)", fontsize=11)
    ax.margins(y=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "DEEP_ranges.png", dpi=150)
    plt.close(fig)


def main() -> None:
    fig_brokers()
    fig_fingerprint()
    fig_ranges()
    for f in ["DEEP_brokers.png", "DEEP_fingerprint.png", "DEEP_ranges.png"]:
        p = OUT / f
        print(f"{f}: {p.exists()} {p.stat().st_size if p.exists() else 0} bytes")


if __name__ == "__main__":
    main()
