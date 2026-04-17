import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")

COLORS = {
    "baseline": "#1f77b4",
    "with_co": "#d62728",
    "bpg_low": "#2ca02c",
    "bpg_high": "#9467bd",
    "acute": "#ff7f0e",
    "hb": "#4c78a8",
    "hbo2": "#f58518",
    "hbo22": "#54a24b",
    "hbo23": "#e45756",
    "hbo24": "#72b7b2",
}

def load_txt(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed", na=False)]
    df.columns = [str(c).lstrip("# ").strip() for c in df.columns]
    return df

def finish_plot(ax, xlabel, ylabel, title):
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, pad=10, weight="bold")
    ax.tick_params(labelsize=10)
    ax.legend(frameon=True, fontsize=9)
    plt.tight_layout()

def savefig(fig, name):
    fig.savefig(OUTPUT_DIR / name, dpi=300, bbox_inches="tight")
    plt.close(fig)

# Load data
baseline_time = load_txt(BASE_DIR / "model_data"/ "baseline_timecourse.txt")
baseline_po2 = load_txt(BASE_DIR / "model_data"/ "baseline_po2_scan.txt")
with_co_po2 = load_txt(BASE_DIR / "model_data"/ "with_co_po2_scan.txt")
acute_co = load_txt(BASE_DIR / "model_data"/ "acute_CO_poisoning.txt")
bpg_low = load_txt(BASE_DIR / "model_data"/ "bpg_low_scan.txt")
bpg_high = load_txt(BASE_DIR / "model_data"/ "bpg_high_scan.txt")
supp = load_txt(BASE_DIR / "model_data"/ "Supplementary Figure S1.txt")

# Figure 1A
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(
    baseline_time["Time"],
    baseline_time["Values[Relative_Saturation]"],
    linewidth=2.5,
    color=COLORS["baseline"],
    label="Baseline",
)
finish_plot(ax, "Time", "Relative Saturation", "")
savefig(fig, "Figure_1A_baseline_timecourse.png")

# Figure 1B
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(
    baseline_po2["Values[PO2].InitialValue"],
    baseline_po2["Values[Relative_Saturation]"],
    linewidth=2.5,
    color=COLORS["baseline"],
    marker="o",
    markersize=4,
    label="Baseline",
)
finish_plot(ax, "PO2", "Relative Saturation", "")
savefig(fig, "Figure_1B_baseline_PO2_vs_saturation.png")

# Figure 1C
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(
    baseline_po2["Values[PO2].InitialValue"],
    baseline_po2["Values[Relative_Saturation]"],
    linewidth=2.5,
    marker="o",
    markersize=4,
    color=COLORS["baseline"],
    label="No CO",
)
ax.plot(
    with_co_po2["Values[PO2].InitialValue"],
    with_co_po2["Values[Relative_Saturation]"],
    linewidth=2.5,
    marker="s",
    markersize=4,
    color=COLORS["with_co"],
    label="With CO",
)
finish_plot(ax, "PO2", "Relative Saturation", "")
savefig(fig, "Figure_1C_noCO_vs_withCO.png")

# Figure 2A
fig, ax = plt.subplots(figsize=(6.8, 4.5))
ax.plot(
    acute_co["Time"],
    acute_co["Values[Relative_Saturation]"],
    linewidth=2.5,
    color=COLORS["acute"],
    label="Acute CO poisoning",
)
ax.axvline(10, color="black", linestyle="--", linewidth=1.5, label="CO event (t=10)")
finish_plot(ax, "Time", "Relative Saturation", "")
savefig(fig, "Figure_2A_acute_CO_poisoning.png")

# Figure 2B
fig, ax = plt.subplots(figsize=(6.8, 4.8))
ax.plot(
    baseline_po2["Values[PO2].InitialValue"],
    baseline_po2["Values[Relative_Saturation]"],
    linewidth=2.5,
    marker="o",
    markersize=4,
    color=COLORS["baseline"],
    label="Normal 2,3-BPG",
)
ax.plot(
    bpg_low["Values[PO2].InitialValue"],
    bpg_low["Values[Relative_Saturation]"],
    linewidth=2.5,
    marker="^",
    markersize=4,
    color=COLORS["bpg_low"],
    label="Low 2,3-BPG-like",
)
ax.plot(
    bpg_high["Values[PO2].InitialValue"],
    bpg_high["Values[Relative_Saturation]"],
    linewidth=2.5,
    marker="s",
    markersize=4,
    color=COLORS["bpg_high"],
    label="High 2,3-BPG-like",
)
finish_plot(ax, "PO2", "Relative Saturation", "")
savefig(fig, "Figure_2B_BPG_shift.png")

# Supplementary Figure S1
fig, ax = plt.subplots(figsize=(7.2, 5.0))
time_col = "Time"
for col, color, label in [
    ("[Hb]", COLORS["hb"], "Hb"),
    ("[HbO2]", COLORS["hbo2"], "HbO2"),
    ("[HbO22]", COLORS["hbo22"], "Hb(O2)2"),
    ("[HbO23]", COLORS["hbo23"], "Hb(O2)3"),
    ("[HbO24]", COLORS["hbo24"], "Hb(O2)4"),
]:
    ax.plot(supp[time_col], supp[col], linewidth=2.2, color=color, label=label)

finish_plot(ax, "Time", "Concentration / Amount", "")
savefig(fig, "Supplementary_Figure_S1_species_dynamics.png")

print("Finished. Files saved in:", OUTPUT_DIR)
for p in sorted(OUTPUT_DIR.glob("*.png")):
    print(p.name)
