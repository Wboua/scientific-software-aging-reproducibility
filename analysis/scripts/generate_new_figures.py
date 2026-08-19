"""Generate reviewer-oriented figures from validated data without changing sources."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "results" / "normalized" / "master_matrix.csv"
DENOMS = ROOT / "results" / "tables" / "dimension_denominators.csv"
YEARS = ROOT / "analysis" / "publication_years.csv"
OUT = ROOT / "results" / "figures"

PASS = "#2a9d8f"
PARTIAL = "#e9c46a"
FAIL = "#e76f51"
NA = "#b8b8b8"
UNKNOWN = "#6c757d"
NAVY = "#17324d"

plt.rcParams.update({"font.family": "serif", "font.size": 10, "axes.titlesize": 12})


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def save(fig: plt.Figure, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def timeline(matrix: list[dict[str, str]]) -> None:
    year_by_case = {r["case_id"]: int(r["publication_year"]) for r in rows(YEARS)}
    missing = {r["case_id"] for r in matrix} - year_by_case.keys()
    if missing:
        raise ValueError(f"Missing publication years: {sorted(missing)}")
    color = {"PASS": PASS, "PARTIAL": PARTIAL, "N/A": NA, "UNKNOWN": UNKNOWN, "FAIL": FAIL}
    ordered = sorted(matrix, key=lambda r: r["case_id"], reverse=True)
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    for y, row in enumerate(ordered):
        start = year_by_case[row["case_id"]]
        ax.barh(y, 2026 - start, left=start, height=.55, color=color[row["E"]], edgecolor="white")
        ax.scatter(start, y, s=26, color=NAVY, zorder=3)
        ax.text(2026.15, y, f"{row['repair_level']} · H={row['H']}", va="center", fontsize=8)
    ax.set_yticks(range(len(ordered)), [r["case_id"] for r in ordered])
    ax.set_xlim(2010.5, 2028.2); ax.set_xticks(range(2011, 2027, 3))
    ax.set_xlabel("Publication year to evaluation year (2026)")
    ax.set_title("Artifact age at evaluation, colored by executability outcome")
    ax.grid(axis="x", alpha=.22)
    ax.legend(handles=[Patch(color=color[s], label=s) for s in ("PASS", "PARTIAL", "N/A", "UNKNOWN")], ncol=4, loc="lower left")
    fig.tight_layout(); save(fig, "fig_timeline_aging")


def dimension_records() -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for row in rows(DENOMS):
        dim = row["dimension"]
        rec = result.setdefault(dim, {"denominator": float(row["denominator"]), "na": float(row["excluded_na"]), "unknown": float(row["excluded_unknown"])})
        rec[row["state"].lower()] = float(row["numerator"])
    return result


def chain_profiles() -> None:
    recs = dimension_records(); dims = list("AIBENP"); x = np.arange(len(dims))
    passed = np.array([recs[d].get("pass", 0) for d in dims]); partial = np.array([recs[d].get("partial", 0) for d in dims])
    failed = np.array([recs[d].get("fail", 0) for d in dims]); excluded = np.array([recs[d]["na"] + recs[d]["unknown"] for d in dims])
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.bar(x, passed, .68, color=PASS, label="PASS")
    ax.bar(x, partial, .68, bottom=passed, color=PARTIAL, label="PARTIAL")
    ax.bar(x, failed, .68, bottom=passed+partial, color=FAIL, label="FAIL")
    ax.bar(x, excluded, .68, bottom=passed+partial+failed, color=NA, label="N/A + UNKNOWN (excluded)")
    for i, d in enumerate(dims):
        ax.text(i, 10.15, f"eligible n={int(recs[d]['denominator'])}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x, dims); ax.set_ylim(0, 11.15); ax.set_ylabel("Cases in the closed corpus")
    ax.set_xlabel("Capability dimension")
    ax.set_title("Capability chain: eligible cases and outcome distribution")
    ax.legend(ncol=2, loc="lower left"); ax.grid(axis="y", alpha=.2)
    fig.text(.5, .005, "Aggregate layer profiles, not individual transition flows; N/A and UNKNOWN are excluded from rates.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0,.04,1,1)); save(fig, "fig_chain_degradation")


def sensitivity() -> None:
    recs = dimension_records(); dims = list("IBENP"); y = np.arange(len(dims))[::-1]
    strict=[]; inclusive=[]; low=[]; high=[]
    for d in dims:
        r=recs[d]; den=r["denominator"]; unk=r["unknown"]; p=r.get("pass",0); part=r.get("partial",0)
        strict.append(100*p/den); inclusive.append(100*(p+part)/den)
        low.append(100*p/(den+unk)); high.append(100*(p+unk)/(den+unk))
    fig, ax = plt.subplots(figsize=(8.3, 4.8))
    for yi, lo, hi in zip(y, low, high): ax.hlines(yi, lo, hi, color=UNKNOWN, lw=4, alpha=.7)
    ax.scatter(strict, y, color=PASS, s=48, label="Strict PASS", zorder=3)
    ax.scatter(inclusive, y, color=NAVY, marker="s", s=46, label="Inclusive PASS+PARTIAL", zorder=3)
    ax.set_yticks(y, dims); ax.set_xlim(-2,102); ax.set_xticks(range(0,101,20), [f"{v}%" for v in range(0,101,20)])
    ax.set_xlabel("Observed or sensitivity-bounded rate")
    ax.set_title("Classification sensitivity: strict, inclusive, and UNKNOWN bounds")
    ax.legend(handles=[Line2D([],[],color=UNKNOWN,lw=4,label="UNKNOWN bounds"), Line2D([],[],marker="o",color="none",markerfacecolor=PASS,label="Strict PASS"), Line2D([],[],marker="s",color="none",markerfacecolor=NAVY,label="Inclusive PASS+PARTIAL")], ncol=3, loc="lower center")
    ax.grid(axis="x", alpha=.2)
    fig.text(.5,.005,"Bounds classify applicable UNKNOWN cells as all-fail or all-pass; they are not confidence intervals.",ha="center",fontsize=8)
    fig.tight_layout(rect=(0,.05,1,1)); save(fig, "fig_sensitivity_bounds")


def preservation_matrix() -> None:
    # Analytical coverage coding requested by the manuscript audit; it is not a case-outcome matrix.
    labels=["Container\n(PS002)","VM\n(PS007)","Pinned deps\n(PS005)","Source only\n(PS001/006/009)"]
    dims=list("AIBENPH")
    data=np.array([[1,1,1,0,0,0,0],[1,1,1,0,0,0,0],[1,1,0,0,0,0,1],[1,0,0,0,0,0,1]])
    from matplotlib.colors import ListedColormap
    fig, ax=plt.subplots(figsize=(8.4,4.4)); ax.imshow(data,aspect="auto",cmap=ListedColormap([FAIL,PASS]),vmin=0,vmax=1)
    ax.set_xticks(range(7),dims); ax.set_yticks(range(4),labels)
    for i in range(4):
        for j in range(7): ax.text(j,i,"documented" if data[i,j] else "not guaranteed",ha="center",va="center",fontsize=7,color="white" if data[i,j] else NAVY)
    ax.set_title("Analytical preservation scope across capability layers")
    ax.set_xlabel("Capability or external condition")
    ax.legend(handles=[Patch(color=PASS,label="Documented preservation scope"),Patch(color=FAIL,label="Not guaranteed by mechanism alone")],ncol=2,loc="lower center",bbox_to_anchor=(.5,-.28))
    fig.text(.5,.005,"Schematic interpretation of retained packaging; not an experimental success matrix. H=1 denotes no external device/startup dependence in this coding.",ha="center",fontsize=8)
    fig.tight_layout(rect=(0,.1,1,1)); save(fig,"fig_preservation_matrix")


def corpus_comparison() -> None:
    studies=[("ReproScore\n(Samuel 2026)",423,1),("Al Muttakin\n(ICSE 2026)",100,2),("CompRep\n(Costa 2025)",38,2),("Present study\n(SCIREPRO)",10,5)]
    fig,ax=plt.subplots(figsize=(8.2,5.0))
    for name,n,g in studies:
        current=name.startswith("Present")
        ax.scatter(n,g,s=90+np.sqrt(n)*11,color=PASS if current else "#457b9d",edgecolor="white",linewidth=1.2,zorder=3)
        ax.annotate(name,(n,g),xytext=(7,7),textcoords="offset points",fontsize=8)
    ax.set_xscale("log"); ax.set_xlim(7,650); ax.set_ylim(.5,5.6); ax.set_yticks(range(1,6),["Binary outcome","Effort categories","Dimension scores","Repair tracing","Claim-level provenance"])
    ax.set_xlabel("Corpus size (log scale)"); ax.set_ylabel("Analytical measurement resolution")
    ax.set_title("Corpus size versus measurement granularity in related studies")
    ax.annotate("N/P separated + H eligibility",xy=(10,5),xytext=(35,4.4),arrowprops={"arrowstyle":"->","color":NAVY},color=NAVY,fontsize=9)
    ax.grid(alpha=.2); fig.tight_layout(); save(fig,"fig_corpus_comparison")


def main() -> None:
    matrix=rows(MATRIX)
    timeline(matrix); chain_profiles(); sensitivity(); preservation_matrix(); corpus_comparison()
    print("Generated 5 new figures as 300-DPI PNG and vector PDF; source data unchanged.")


if __name__ == "__main__":
    main()
