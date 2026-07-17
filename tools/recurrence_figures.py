#!/usr/bin/env python3
"""Regenerate the two direct-recurrence figures for Supplement v15.

Implements the queue-and-region backlog model of the open-gate closure note
(U_{t+1} = max{0, U_t + A_t - S_t}) with the frozen protocol constants
(seed 20260716; 12 regions; horizon 300; lift 80; operand expansion 120;
second lift 215) and the five post-lift service regimes. The stochastic
replicate mean and 95% simulation band are drawn; the printed summary in the
Supplement quotes the closure note's executed Table 4.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 20260716
REGIONS = 12
HORIZON = 300
T_LIFT = 80
T_EXPAND = 120
T_SECOND = 215
REG_THRESH = 12
REPLICATES = 1000

REGIMES = ["fixed post lift", "proportional service", "regenerative distribution",
           "second order lift", "branch heterogeneity"]
COLORS = {
    "fixed post lift": "#c1272d",
    "proportional service": "#0072b2",
    "regenerative distribution": "#029e73",
    "second order lift": "#8a2be2",
    "branch heterogeneity": "#d55e00",
}


A_PRE = 0.55      # pre-lift per-region arrival intensity
GROWTH = 0.010    # post-expansion arrival growth per step
S_PRE = 0.20      # pre-lift service intensity
S_LIFT = 1.32     # post-lift service capacity
PROP_MARGIN = 0.12
REGEN_ADD = 1.15
SECOND_ADD = 1.25


def arrival_mean(t, mult):
    """Per-region mean arrival intensity, shape (REGIONS,)."""
    base = A_PRE + (GROWTH * (t - T_EXPAND) if t >= T_EXPAND else 0.0)
    return base * mult


def service_mean(t, regime, arr_mean):
    """Per-region mean certified service intensity, shape (REGIONS,)."""
    if t < T_LIFT:
        return np.full(REGIONS, S_PRE)
    if t < T_EXPAND:            # reversal interval: the lift boosts all regimes
        return np.full(REGIONS, S_LIFT)
    if regime in ("fixed post lift", "branch heterogeneity"):
        return np.full(REGIONS, S_LIFT)
    if regime == "proportional service":
        return arr_mean + PROP_MARGIN
    if regime == "regenerative distribution":
        frac = 1.0 / (1.0 + np.exp(-(t - 165) / 12.0))
        return np.full(REGIONS, S_LIFT + frac * REGEN_ADD)
    if regime == "second order lift":
        return np.full(REGIONS, S_LIFT + (SECOND_ADD if t >= T_SECOND else 0.0))
    return np.full(REGIONS, S_LIFT)


def run_batch(regime, rng):
    """Vectorized over replicates: returns agg (R,H) and regions_over (R,H)."""
    R = REPLICATES
    u = np.zeros((R, REGIONS))
    if regime == "branch heterogeneity":
        mult = np.linspace(0.5, 1.6, REGIONS)
    else:
        mult = np.ones(REGIONS)
    agg = np.zeros((R, HORIZON))
    regions_over = np.zeros((R, HORIZON))
    for t in range(HORIZON):
        am = arrival_mean(t, mult)
        sm = service_mean(t, regime, am)
        arr = rng.poisson(np.maximum(am, 0) * 4.0, size=(R, REGIONS)) / 4.0
        svc = rng.poisson(np.maximum(sm, 0) * 4.0, size=(R, REGIONS)) / 4.0
        u = np.maximum(0.0, u + arr - svc)
        agg[:, t] = u.sum(1)
        regions_over[:, t] = (u >= REG_THRESH).sum(1)
    return agg, regions_over


def main(outdir):
    rng = np.random.default_rng(SEED)
    time = np.arange(HORIZON)
    fig1, ax1 = plt.subplots(figsize=(7.4, 4.3))
    fig2, ax2 = plt.subplots(figsize=(7.4, 4.3))
    for regime in REGIMES:
        aggs, regs = run_batch(regime, rng)
        agg_mean = aggs.mean(0)
        agg_lo = np.percentile(aggs, 2.5, axis=0)
        agg_hi = np.percentile(aggs, 97.5, axis=0)
        reg_med = np.median(regs, axis=0)
        print(f"{regime:26s} final_backlog={agg_mean[-1]:7.1f} "
              f"regions_over={reg_med[-1]:5.2f}")
        c = COLORS[regime]
        ax1.plot(time, agg_mean, color=c, lw=1.8, label=regime)
        ax1.fill_between(time, agg_lo, agg_hi, color=c, alpha=0.12, lw=0)
        ax2.plot(time, reg_med, color=c, lw=1.8, label=regime)

    for ax in (ax1, ax2):
        ax.axvline(T_LIFT, ls="--", color="#444444", lw=1.0)
        ax.axvline(T_EXPAND, ls=":", color="#444444", lw=1.0)
        ax.axvline(T_SECOND, ls="-.", color="#888888", lw=1.0)
        ax.set_xlabel("time step")
        ax.legend(fontsize=8, frameon=False, loc="upper left")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    ax1.set_ylabel("aggregate unresolved backlog")
    ax1.set_title("Direct recurrence experiment: reversal and renewed growth",
                  fontsize=11)
    ax2.set_ylabel("regions above fragmentation threshold")
    ax2.set_title("Regional fragmentation after the order lift", fontsize=11)
    ax2.set_ylim(-0.3, REGIONS + 0.3)
    fig1.tight_layout(); fig2.tight_layout()
    fig1.savefig(outdir + "/recurrence_backlog.png", dpi=200)
    fig2.savefig(outdir + "/recurrence_regions.png", dpi=200)
    # report endpoints for sanity
    print("done")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
