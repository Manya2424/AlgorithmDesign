import random
import time
import csv
import statistics
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

def fractional_knapsack(weights, profits, capacity):

    n = len(weights)
    items = [(profits[i] / weights[i], weights[i], profits[i]) for i in range(n)]

   
    items.sort(key=lambda x: x[0], reverse=True)

    total_profit = 0.0
    remaining   = capacity
    fractions   = []

    for ratio, w, p in items:
        if remaining <= 0:
            fractions.append(0.0)
        elif w <= remaining:
            fractions.append(1.0)
            total_profit += p
            remaining    -= w
        else:
            frac = remaining / w
            fractions.append(frac)
            total_profit += frac * p
            remaining     = 0

    return total_profit, fractions



def generate_best_case(n, capacity):
   
    weights = [random.uniform(1, 10) for _ in range(n)]
    ratios  = sorted([random.uniform(1, 20) for _ in range(n)], reverse=True)
    profits = [r * w for r, w in zip(ratios, weights)]
  
    cap = sum(weights) * 0.9
    return weights, profits, cap


def generate_average_case(n, capacity):
  
    weights = [random.uniform(1, 50) for _ in range(n)]
    profits = [random.uniform(1, 100) for _ in range(n)]
    cap     = sum(weights) * 0.5
    return weights, profits, cap


def generate_worst_case(n, capacity):
    
    weights = [random.uniform(1, 10) for _ in range(n)]
    ratios  = sorted([random.uniform(1, 20) for _ in range(n)]) 
    profits = [r * w for r, w in zip(ratios, weights)]
    cap     = sum(weights) * 0.1 
    return weights, profits, cap



def measure_time(generator, n, capacity, repeats=15):
   
    times = []
    for _ in range(repeats):
        weights, profits, cap = generator(n, capacity)
        t0 = time.perf_counter()
        fractional_knapsack(weights, profits, cap)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return statistics.median(times)




def run_experiments(sizes, repeats=15):
    
    best_times    = []
    average_times = []
    worst_times   = []

    print(f"\n{'n':>8} | {'Best (µs)':>12} | {'Average (µs)':>14} | {'Worst (µs)':>12}")
    print("-" * 56)

    for n in sizes:
        cap = n * 25 
        bt = measure_time(generate_best_case,    n, cap, repeats)
        at = measure_time(generate_average_case, n, cap, repeats)
        wt = measure_time(generate_worst_case,   n, cap, repeats)

        best_times.append(bt)
        average_times.append(at)
        worst_times.append(wt)

        print(f"{n:>8} | {bt*1e6:>12.3f} | {at*1e6:>14.3f} | {wt*1e6:>12.3f}")

    return best_times, average_times, worst_times


def save_csv(sizes, best_times, average_times, worst_times, filename="knapsack_results.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "Best_Case_us", "Average_Case_us", "Worst_Case_us"])
        for n, b, a, w in zip(sizes, best_times, average_times, worst_times):
            writer.writerow([n, round(b*1e6, 4), round(a*1e6, 4), round(w*1e6, 4)])
    print(f"\n✔  Results saved to '{filename}'")


COLORS = {
    "best":    "#2ecc71",  
    "average": "#3498db",   
    "worst":   "#e74c3c",  
}

def style_ax(ax, title, xlabel="Input size (n)", ylabel="Time (µs)"):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=10)


def plot_individual_cases(sizes, best_times, average_times, worst_times, out_dir="."):
   
    cases = [
        ("Best Case",    best_times,    "best"),
        ("Average Case", average_times, "average"),
        ("Worst Case",   worst_times,   "worst"),
    ]
    filenames = []
    for label, times, key in cases:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        t_us = [t * 1e6 for t in times]
        ax.plot(sizes, t_us, marker="o", linewidth=2,
                color=COLORS[key], label=label)
        ax.fill_between(sizes, t_us, alpha=0.12, color=COLORS[key])

    
        x = np.array(sizes, dtype=float)
        nlogn = x * np.log2(x + 1)
        scale = max(t_us) / max(nlogn) if max(nlogn) > 0 else 1
        ax.plot(sizes, nlogn * scale, linestyle="--", linewidth=1,
                color="grey", alpha=0.6, label="O(n log n) ref")

        style_ax(ax, f"Fractional Knapsack — {label}")
        plt.tight_layout()
        fname = os.path.join(out_dir, f"knapsack_{key}_case.png")
        fig.savefig(fname, dpi=150)
        plt.close(fig)
        filenames.append(fname)
        print(f"✔  Saved '{fname}'")
    return filenames


def plot_combined(sizes, best_times, average_times, worst_times, out_dir="."):
   
    fig, ax = plt.subplots(figsize=(9, 5))
    for label, times, key in [
        ("Best Case",    best_times,    "best"),
        ("Average Case", average_times, "average"),
        ("Worst Case",   worst_times,   "worst"),
    ]:
        t_us = [t * 1e6 for t in times]
        ax.plot(sizes, t_us, marker="o", linewidth=2,
                color=COLORS[key], label=label)

    style_ax(ax, "Fractional Knapsack — Best / Average / Worst Case Comparison")
    plt.tight_layout()
    fname = os.path.join(out_dir, "knapsack_combined.png")
    fig.savefig(fname, dpi=150)
    plt.close(fig)
    print(f"✔  Saved '{fname}'")
    return fname


def plot_comparison_bar(sizes, best_times, average_times, worst_times, out_dir="."):
   
    fig, (ax_bar, ax_pie) = plt.subplots(1, 2, figsize=(14, 5.5),
                                          gridspec_kw={"width_ratios": [2, 1]})

    x      = np.arange(len(sizes))
    width  = 0.26
    b_us   = [t * 1e6 for t in best_times]
    a_us   = [t * 1e6 for t in average_times]
    w_us   = [t * 1e6 for t in worst_times]

    bars_b = ax_bar.bar(x - width, b_us, width, label="Best",    color=COLORS["best"],    alpha=0.85)
    bars_a = ax_bar.bar(x,          a_us, width, label="Average", color=COLORS["average"], alpha=0.85)
    bars_w = ax_bar.bar(x + width, w_us, width, label="Worst",   color=COLORS["worst"],   alpha=0.85)

    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels([str(s) for s in sizes], rotation=45, ha="right")
    style_ax(ax_bar,
             "Grouped Bar: Time per Input Size",
             xlabel="Input size (n)")

   
    for rect in list(bars_b) + list(bars_a) + list(bars_w):
        h = rect.get_height()
        if h > 0:
            ax_bar.annotate(f"{h:.1f}",
                            xy=(rect.get_x() + rect.get_width() / 2, h),
                            xytext=(0, 3), textcoords="offset points",
                            ha="center", va="bottom", fontsize=6.5)

  
    totals = [sum(b_us), sum(a_us), sum(w_us)]
    labels = ["Best", "Average", "Worst"]
    explode = (0.04, 0.04, 0.04)
    wedges, texts, autotexts = ax_pie.pie(
        totals,
        labels=labels,
        autopct="%1.1f%%",
        colors=[COLORS["best"], COLORS["average"], COLORS["worst"]],
        explode=explode,
        startangle=140,
        textprops={"fontsize": 11},
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
    ax_pie.set_title("Total Time Share\n(summed across all n)", fontsize=12, fontweight="bold")

    fig.suptitle("Fractional Knapsack — Best / Average / Worst Case Comparison",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    fname = os.path.join(out_dir, "knapsack_bar_pie_comparison.png")
    fig.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"✔  Saved '{fname}'")
    return fname


if __name__ == "__main__":
    random.seed(42)  

    SIZES   = [10, 50, 100, 250, 500, 750, 1000, 2000, 3000, 5000]
    REPEATS = 20     
    OUT_DIR = "."     
    CSV_FILE = os.path.join(OUT_DIR, "knapsack_results.csv")

    print("=" * 56)
    print("  Fractional Knapsack — Timing Experiment")
    print(f"  Sizes   : {SIZES}")
    print(f"  Repeats : {REPEATS}")
    print("=" * 56)

    
    best_t, avg_t, worst_t = run_experiments(SIZES, repeats=REPEATS)


    save_csv(SIZES, best_t, avg_t, worst_t, filename=CSV_FILE)

    print("\nGenerating plots …")
    plot_individual_cases(SIZES, best_t, avg_t, worst_t, out_dir=OUT_DIR)
    plot_combined(SIZES, best_t, avg_t, worst_t,         out_dir=OUT_DIR)
    plot_comparison_bar(SIZES, best_t, avg_t, worst_t,   out_dir=OUT_DIR)

    print("\n✅  All done!")
    print("Generated files:")
    for f in [
        "knapsack_best_case.png",
        "knapsack_average_case.png",
        "knapsack_worst_case.png",
        "knapsack_combined.png",
        "knapsack_bar_pie_comparison.png",
        "knapsack_results.csv",
    ]:
        print(f"   • {f}")

    print("\nDisplaying Average Case graph …")
    t_us  = [t * 1e6 for t in avg_t]
    x     = np.array(SIZES, dtype=float)
    nlogn = x * np.log2(x + 1)
    scale = max(t_us) / max(nlogn) if max(nlogn) > 0 else 1

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(SIZES, t_us, marker="o", linewidth=2.5,
            color=COLORS["average"], label="Average Case", zorder=3)
    ax.fill_between(SIZES, t_us, alpha=0.15, color=COLORS["average"])
    ax.plot(SIZES, nlogn * scale, linestyle="--", linewidth=1.5,
            color="grey", alpha=0.7, label="O(n log n) reference")

   
    for xi, yi in zip(SIZES, t_us):
        ax.annotate(f"{yi:.1f}",
                    xy=(xi, yi), xytext=(0, 8),
                    textcoords="offset points",
                    ha="center", fontsize=8, color="#2c3e50")

    style_ax(ax, "Fractional Knapsack — Average Case vs Time")
    fig.suptitle(f"Repeats per size: {REPEATS}  |  Sizes: {SIZES[0]}–{SIZES[-1]}",
                 fontsize=9, color="grey", y=0.01)
    plt.tight_layout()
    plt.show()   