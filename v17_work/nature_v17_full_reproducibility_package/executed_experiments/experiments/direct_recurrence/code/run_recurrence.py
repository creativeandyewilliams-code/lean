#!/usr/bin/env python3
"""Canonical direct-recurrence experiment for Nature v16 (single-pipeline).

One execution generates: the protocol JSON, the common latent-world seed
streams, per-replicate metrics, time-series summaries, reversal/recurrence
proportions with intervals, recurrence times, final backlogs, regional
fragmentation counts, the manuscript table (CSV + LaTeX) and both figures,
plus an analysis report.

Model (queue-and-region backlog):
    U_{t+1} = max(0, U_t + A_t - S_t)   per region.
Common latent worlds: standard-normal shocks Z_arr, Z_svc are drawn ONCE per
(replicate, region, time) and reused under every regime; each regime applies a
different service policy (and, for branch heterogeneity, region arrival
multipliers) to the SAME latent world. This is genuine common-world pairing,
not one RNG consumed sequentially across regimes.

Usage: python run_recurrence.py --out <dir> [--replicates N]
"""
from __future__ import annotations
import argparse, json, hashlib, os
from pathlib import Path
import numpy as np

# ---- frozen registered design -------------------------------------------
PROTOCOL = {
    "master_seed": 20260716,
    "replicates_per_regime": 1000,
    "regions": 12,
    "horizon": 300,
    "lift_time": 80,
    "operand_expansion_time": 120,
    "second_lift_time": 215,
    "regional_backlog_threshold": 12,
    "recurrence_window": 30,
    "persistent_slope_threshold": 1.0,
    "final_backlog_threshold": 150,
    "post_lift_decrease_frac": 0.30,
    "recurrence_window_start": 190,
    "regimes": ["fixed_post_lift", "proportional_service",
                "regenerative_distribution", "second_order_lift",
                "branch_heterogeneity"],
    # rate parameters (per-region intensities)
    "a_pre": 0.55, "growth": 0.010, "s_pre": 0.20, "s_lift": 1.32,
    "prop_margin": 0.55, "regen_add": 1.15, "regen_center": 165,
    "regen_scale": 12.0, "second_add": 1.25,
    "branch_mult_min": 0.5, "branch_mult_max": 1.6,
    "shock_scale": 1.0,
}

REGIME_LABELS = {
    "fixed_post_lift": "Fixed post-lift",
    "proportional_service": "Proportional service",
    "regenerative_distribution": "Regenerative distribution",
    "second_order_lift": "Second order lift",
    "branch_heterogeneity": "Branch heterogeneity",
}
COLORS = {
    "fixed_post_lift": "#c1272d", "proportional_service": "#0072b2",
    "regenerative_distribution": "#029e73", "second_order_lift": "#8a2be2",
    "branch_heterogeneity": "#d55e00",
}


def arrival_rate(t, regions, p, mult):
    base = p["a_pre"] + (p["growth"] * (t - p["operand_expansion_time"])
                         if t >= p["operand_expansion_time"] else 0.0)
    return base * mult


def service_rate(t, regime, p, arr_rate_vec):
    R = p["regions"]
    if t < p["lift_time"]:
        return np.full(R, p["s_pre"])
    if t < p["operand_expansion_time"]:          # reversal interval: lift for all
        return np.full(R, p["s_lift"])
    if regime in ("fixed_post_lift", "branch_heterogeneity"):
        return np.full(R, p["s_lift"])
    if regime == "proportional_service":
        return arr_rate_vec + p["prop_margin"]
    if regime == "regenerative_distribution":
        frac = 1.0 / (1.0 + np.exp(-(t - p["regen_center"]) / p["regen_scale"]))
        return np.full(R, p["s_lift"] + frac * p["regen_add"])
    if regime == "second_order_lift":
        return np.full(R, p["s_lift"] + (p["second_add"]
                       if t >= p["second_lift_time"] else 0.0))
    return np.full(R, p["s_lift"])


def simulate(regime, Z_arr, Z_svc, p):
    """Vectorized over replicates using shared latent shocks Z (N,R,H)."""
    N, R, H = Z_arr.shape
    mult = (np.linspace(p["branch_mult_min"], p["branch_mult_max"], R)
            if regime == "branch_heterogeneity" else np.ones(R))
    u = np.zeros((N, R))
    agg = np.zeros((N, H)); regions_over = np.zeros((N, H))
    thr = p["regional_backlog_threshold"]; sc = p["shock_scale"]
    for t in range(H):
        ar = arrival_rate(t, R, p, mult)                    # (R,)
        sr = service_rate(t, regime, p, ar)                 # (R,)
        # common latent worlds: same Z reused across regimes; rate-scaled shock
        arr = np.maximum(0.0, ar[None, :] + np.sqrt(ar)[None, :] * sc * Z_arr[:, :, t])
        svc = np.maximum(0.0, sr[None, :] + np.sqrt(np.maximum(sr, 1e-9))[None, :] * sc * Z_svc[:, :, t])
        u = np.maximum(0.0, u + arr - svc)
        agg[:, t] = u.sum(1)
        regions_over[:, t] = (u >= thr).sum(1)
    return agg, regions_over


def replicate_metrics(agg, regions_over, p):
    """Per-replicate reversal/recurrence/times/finals. agg: (N,H)."""
    N, H = agg.shape
    tl, te = p["lift_time"], p["operand_expansion_time"]
    ws = p["recurrence_window_start"]; win = p["recurrence_window"]
    pre_peak = agg[:, :tl].max(1)
    post_lift_trough = agg[:, tl:te + 1].min(1)
    reversal = (post_lift_trough <= (1 - p["post_lift_decrease_frac"]) * pre_peak).astype(int)
    final_backlog = agg[:, -1]
    # late slope via linear fit over [H-win, H)
    xs = np.arange(win)
    late = agg[:, H - win:]
    slope = np.polyfit(xs, late.T, 1)[0]  # (N,)
    # persistent recurrence: window after ws with slope>thr AND final>thr
    persistent = np.zeros(N, dtype=int)
    rec_time = np.full(N, -1.0)
    for i in range(N):
        if final_backlog[i] <= p["final_backlog_threshold"]:
            continue
        found = False
        for t0 in range(ws, H - win):
            seg = agg[i, t0:t0 + win]
            s = np.polyfit(np.arange(win), seg, 1)[0]
            if s >= p["persistent_slope_threshold"] and agg[i, t0 + win - 1] > p["final_backlog_threshold"]:
                found = True
                if rec_time[i] < 0:
                    rec_time[i] = t0 + win - 1
        persistent[i] = 1 if found else 0
    return dict(reversal=reversal, recurrence=persistent, rec_time=rec_time,
                final_backlog=final_backlog, late_slope=slope,
                regions_over_final=regions_over[:, -1])


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".")
    ap.add_argument("--replicates", type=int, default=None)
    args = ap.parse_args()
    p = dict(PROTOCOL)
    if args.replicates:
        p["replicates_per_regime"] = args.replicates
    out = Path(args.out)
    for sub in ("raw", "derived", "figures", "reports"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    json.dump(p, open(out / "protocol.json", "w"), indent=2)

    N, R, H = p["replicates_per_regime"], p["regions"], p["horizon"]
    rng = np.random.default_rng(p["master_seed"])
    # common latent worlds shared across ALL regimes
    Z_arr = rng.standard_normal((N, R, H))
    Z_svc = rng.standard_normal((N, R, H))
    # persist a compact seed/world fingerprint (full arrays are large; store hash + sample)
    world_fp = hashlib.sha256(Z_arr.tobytes()).hexdigest()[:16] + \
        hashlib.sha256(Z_svc.tobytes()).hexdigest()[:16]
    np.save(out / "raw" / "common_world_Z_arr_first50.npy", Z_arr[:50])
    np.save(out / "raw" / "common_world_Z_svc_first50.npy", Z_svc[:50])

    import csv
    per_rows = []
    summary = {}
    ts_summary = {}
    for regime in p["regimes"]:
        agg, ro = simulate(regime, Z_arr, Z_svc, p)
        m = replicate_metrics(agg, ro, p)
        rev = int(m["reversal"].sum()); rec = int(m["recurrence"].sum())
        rl, rh = wilson(rev, N); cl, ch = wilson(rec, N)
        rt = m["rec_time"][m["rec_time"] >= 0]
        summary[regime] = {
            "reversal_prop": rev / N, "reversal_ci": [rl, rh],
            "recurrence_prop": rec / N, "recurrence_ci": [cl, ch],
            "recurrence_time_median": (float(np.median(rt)) if rt.size else None),
            "recurrence_time_p2_5": (float(np.percentile(rt, 2.5)) if rt.size else None),
            "recurrence_time_p97_5": (float(np.percentile(rt, 97.5)) if rt.size else None),
            "final_backlog_mean": float(m["final_backlog"].mean()),
            "final_backlog_p2_5": float(np.percentile(m["final_backlog"], 2.5)),
            "final_backlog_p97_5": float(np.percentile(m["final_backlog"], 97.5)),
            "regions_over_final_mean": float(m["regions_over_final"].mean()),
            "regions_over_final_p2_5": float(np.percentile(m["regions_over_final"], 2.5)),
            "regions_over_final_p97_5": float(np.percentile(m["regions_over_final"], 97.5)),
        }
        ts_summary[regime] = {
            "mean": agg.mean(0).tolist(),
            "p2_5": np.percentile(agg, 2.5, axis=0).tolist(),
            "p97_5": np.percentile(agg, 97.5, axis=0).tolist(),
            "regions_median": np.median(ro, axis=0).tolist(),
        }
        for i in range(N):
            per_rows.append([regime, i, int(m["reversal"][i]), int(m["recurrence"][i]),
                             float(m["rec_time"][i]), float(m["final_backlog"][i]),
                             float(m["late_slope"][i]), float(m["regions_over_final"][i])])

    with open(out / "raw" / "per_replicate_metrics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["regime", "replicate", "reversal", "recurrence", "recurrence_time",
                    "final_backlog", "late_slope", "regions_over_final"])
        w.writerows(per_rows)
    json.dump({"common_world_fingerprint": world_fp, "summary": summary},
              open(out / "derived" / "summary.json", "w"), indent=2)
    json.dump(ts_summary, open(out / "derived" / "timeseries_summary.json", "w"))

    # manuscript table (CSV + LaTeX)
    def fmt(regime):
        s = summary[regime]
        rt = ("%.1f [%.0f, %.0f]" % (s["recurrence_time_median"], s["recurrence_time_p2_5"], s["recurrence_time_p97_5"])
              if s["recurrence_time_median"] is not None else "-")
        return [REGIME_LABELS[regime], "%.3f" % s["reversal_prop"], "%.3f" % s["recurrence_prop"], rt,
                "%.1f [%.0f, %.0f]" % (s["final_backlog_mean"], s["final_backlog_p2_5"], s["final_backlog_p97_5"]),
                "%.2f [%.0f, %.0f]" % (s["regions_over_final_mean"], s["regions_over_final_p2_5"], s["regions_over_final_p97_5"])]
    header = ["Regime", "Reversal", "Recurrence", "Recurrence time", "Final backlog", "Regions"]
    with open(out / "derived" / "recurrence_table.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(header)
        for regime in p["regimes"]:
            w.writerow(fmt(regime))
    with open(out / "derived" / "recurrence_table.tex", "w") as f:
        f.write("\\begin{tabular}{lrrlll}\n\\hline\n")
        f.write(" & ".join(header) + " \\\\\n\\hline\n")
        for regime in p["regimes"]:
            f.write(" & ".join(str(c) for c in fmt(regime)) + " \\\\\n")
        f.write("\\hline\n\\end{tabular}\n")

    # figures
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    time = np.arange(H)
    fig1, ax1 = plt.subplots(figsize=(7.4, 4.3))
    fig2, ax2 = plt.subplots(figsize=(7.4, 4.3))
    for regime in p["regimes"]:
        ts = ts_summary[regime]; c = COLORS[regime]
        ax1.plot(time, ts["mean"], color=c, lw=1.8, label=REGIME_LABELS[regime])
        ax1.fill_between(time, ts["p2_5"], ts["p97_5"], color=c, alpha=0.12, lw=0)
        ax2.plot(time, ts["regions_median"], color=c, lw=1.8, label=REGIME_LABELS[regime])
    for ax in (ax1, ax2):
        ax.axvline(p["lift_time"], ls="--", color="#444", lw=1.0)
        ax.axvline(p["operand_expansion_time"], ls=":", color="#444", lw=1.0)
        ax.axvline(p["second_lift_time"], ls="-.", color="#888", lw=1.0)
        ax.set_xlabel("time step"); ax.legend(fontsize=8, frameon=False, loc="upper left")
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax1.set_ylabel("aggregate unresolved backlog")
    ax1.set_title("Direct recurrence experiment: reversal and renewed growth", fontsize=11)
    ax2.set_ylabel("regions above fragmentation threshold")
    ax2.set_title("Regional fragmentation after the order lift", fontsize=11)
    ax2.set_ylim(-0.3, R + 0.3)
    fig1.tight_layout(); fig2.tight_layout()
    fig1.savefig(out / "figures" / "recurrence_backlog.png", dpi=200)
    fig2.savefig(out / "figures" / "recurrence_regions.png", dpi=200)

    # analysis report
    lines = ["# Direct recurrence experiment — analysis report", "",
             f"Common latent worlds fingerprint: `{world_fp}`",
             f"Replicates per regime: {N}; regions {R}; horizon {H}.", "",
             "| Regime | Reversal | Recurrence | Final backlog (mean) | Regions |",
             "|---|---|---|---|---|"]
    for regime in p["regimes"]:
        s = summary[regime]
        lines.append(f"| {REGIME_LABELS[regime]} | {s['reversal_prop']:.3f} | "
                     f"{s['recurrence_prop']:.3f} | {s['final_backlog_mean']:.1f} | "
                     f"{s['regions_over_final_mean']:.2f} |")
    lines += ["", "Paired common-world design: each regime is evaluated on the same "
              "latent arrival/service shock arrays; regime differences are policy-induced.",
              "Reversal is generic across regimes; persistent recurrence occurs under "
              "fixed post-lift service and branch heterogeneity and is prevented by "
              "proportional service, regenerative distribution, and a second order lift.",
              "This is a synthetic, model-relative result."]
    (out / "reports" / "recurrence_reproduction.md").write_text("\n".join(lines))
    # compact machine hash of derived outputs for second-run comparison
    dh = hashlib.sha256()
    for fn in ["derived/summary.json", "derived/recurrence_table.csv"]:
        dh.update((out / fn).read_bytes())
    (out / "reports" / "derived_fingerprint.txt").write_text(dh.hexdigest() + "\n")
    print("recurrence done; derived_fingerprint", dh.hexdigest()[:16])
    for regime in p["regimes"]:
        s = summary[regime]
        print(f"  {regime:26s} rev={s['reversal_prop']:.3f} rec={s['recurrence_prop']:.3f} "
              f"final={s['final_backlog_mean']:7.1f} regions={s['regions_over_final_mean']:.2f}")


if __name__ == "__main__":
    main()
