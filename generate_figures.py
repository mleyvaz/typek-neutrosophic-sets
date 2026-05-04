"""
Genera las 5 figuras del paper Type-k Neutrosophic Sets.
Salida: figures/fig1_hierarchy.png ... fig5_witness_mapping.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D

os.makedirs("C:/Users/HP/Documents/TypeK_Neutrosophic_Paper/figures", exist_ok=True)
OUT = "C:/Users/HP/Documents/TypeK_Neutrosophic_Paper/figures/"

PALETTE = {
    "red":    "#C62828",
    "blue":   "#1565C0",
    "green":  "#2E7D32",
    "orange": "#E65100",
    "purple": "#6A1B9A",
    "grey":   "#546E7A",
    "bg":     "#FAFAFA",
}

# ══════════════════════════════════════════════════════════════════
# FIG 1 — Type-k hierarchy: nested triplets diagram
# ══════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(13, 5), facecolor=PALETTE["bg"])
fig.suptitle("Figure 1. The Type-$k$ Neutrosophic Hierarchy",
             fontsize=13, fontweight="bold", y=1.01)

labels = ["Type-1", "Type-2", "Type-3"]
subtitles = ["3 scalars per element",
             "9 scalars (each component\nis a full triplet)",
             "27 scalars (each sub-component\nis a full triplet)"]
colors_tif = [PALETTE["red"], PALETTE["grey"], PALETTE["blue"]]
tif = ["T", "I", "F"]

for ax_i, (ax, lvl) in enumerate(zip(axes, [1, 2, 3])):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_facecolor(PALETTE["bg"])
    ax.set_title(f"{labels[ax_i]}\n{subtitles[ax_i]}",
                 fontsize=9, color="#333333")

    if lvl == 1:
        for i, (lbl, col) in enumerate(zip(tif, colors_tif)):
            box = FancyBboxPatch((1 + i*2.8, 3.5), 2.3, 3,
                                  boxstyle="round,pad=0.2",
                                  fc=col, ec="white", alpha=0.85)
            ax.add_patch(box)
            ax.text(2.15 + i*2.8, 5.0, lbl, ha="center", va="center",
                    fontsize=18, fontweight="bold", color="white")

    elif lvl == 2:
        for i, (lbl, col) in enumerate(zip(tif, colors_tif)):
            outer = FancyBboxPatch((0.5 + i*3.1, 1.5), 2.8, 7,
                                    boxstyle="round,pad=0.2",
                                    fc=col, ec="white", alpha=0.25, lw=2)
            ax.add_patch(outer)
            ax.text(1.9 + i*3.1, 8.2, lbl, ha="center", fontsize=12,
                    fontweight="bold", color=col)
            for j, (sub, sc) in enumerate(zip(tif, colors_tif)):
                inner = FancyBboxPatch((0.7 + i*3.1, 1.8 + j*2.1), 2.4, 1.7,
                                        boxstyle="round,pad=0.1",
                                        fc=sc, ec="white", alpha=0.75)
                ax.add_patch(inner)
                ax.text(1.9 + i*3.1, 2.65 + j*2.1,
                        f"${'TIF'[j]}_{lbl}$",
                        ha="center", va="center", fontsize=9,
                        fontweight="bold", color="white")

    else:  # lvl == 3
        for i, (lbl, col) in enumerate(zip(tif, colors_tif)):
            outer = FancyBboxPatch((0.3 + i*3.2, 0.5), 3.0, 9,
                                    boxstyle="round,pad=0.1",
                                    fc=col, ec="white", alpha=0.15, lw=1.5)
            ax.add_patch(outer)
            ax.text(1.8 + i*3.2, 9.3, lbl, ha="center", fontsize=10,
                    fontweight="bold", color=col)
            for j, (sub, sc) in enumerate(zip(tif, colors_tif)):
                mid = FancyBboxPatch((0.4 + i*3.2, 0.7 + j*2.9), 2.8, 2.5,
                                      boxstyle="round,pad=0.1",
                                      fc=sc, ec="white", alpha=0.25)
                ax.add_patch(mid)
                for k, (sub2, sc2) in enumerate(zip(tif, colors_tif)):
                    tiny = FancyBboxPatch((0.5 + i*3.2 + k*0.9, 0.9 + j*2.9), 0.75, 1.8,
                                          boxstyle="round,pad=0.05",
                                          fc=sc2, ec="white", alpha=0.8)
                    ax.add_patch(tiny)
                    ax.text(0.875 + i*3.2 + k*0.9, 1.8 + j*2.9,
                            f"${'TIF'[k]}$",
                            ha="center", va="center", fontsize=6,
                            color="white", fontweight="bold")

plt.tight_layout()
plt.savefig(OUT + "fig1_type_k_hierarchy.png", dpi=180,
            bbox_inches="tight", facecolor=PALETTE["bg"])
plt.close()
print("Fig 1 saved")

# ══════════════════════════════════════════════════════════════════
# FIG 2 — % Type-2 by protocol (bar chart)
# ══════════════════════════════════════════════════════════════════
protocols = ["S1", "S1.v2", "S1.v3", "S1-taut", "S4", "S4-N", "S4-O.C", "S4-O.A"]
pcts      = [0.0,  0.0,     0.0,     0.0,        0.0,  0.0,    38.1,      97.3]
ns        = [300,  120,     120,     90,          298,  294,    800,       300]
cols = [PALETTE["grey"] if p < 1 else
        PALETTE["orange"] if p < 60 else
        PALETTE["red"] for p in pcts]

fig, ax = plt.subplots(figsize=(10, 5), facecolor=PALETTE["bg"])
ax.set_facecolor(PALETTE["bg"])
bars = ax.bar(protocols, pcts, color=cols, edgecolor="white", linewidth=1.2, zorder=3)
ax.set_ylim(0, 110)
ax.set_ylabel("Responses requiring Type-2 representation (%)", fontsize=10)
ax.set_title("Figure 2. Type-2 Requirement by Protocol\n"
             "Standard protocols: 0% · Extended protocols: 38–97%",
             fontsize=11, fontweight="bold")
ax.axhline(0, color="#cccccc", linewidth=0.8)
ax.grid(axis="y", color="#e0e0e0", zorder=0)
ax.spines[["top","right"]].set_visible(False)

for bar, pct, n in zip(bars, pcts, ns):
    if pct > 0:
        ax.text(bar.get_x() + bar.get_width()/2, pct + 2,
                f"{pct:.1f}%\n(n={n})",
                ha="center", va="bottom", fontsize=9,
                fontweight="bold", color=PALETTE["red"])
    else:
        ax.text(bar.get_x() + bar.get_width()/2, 3,
                "0.0%", ha="center", va="bottom",
                fontsize=8, color="#888888")

ax.annotate("Protocol artefact:\nType-1 enforces [0,1]",
            xy=(2, 0), xytext=(2, 40),
            arrowprops=dict(arrowstyle="->", color=PALETTE["grey"]),
            fontsize=8, color=PALETTE["grey"], ha="center")
ax.annotate("LLMs immediately\nuse Type-2 when allowed",
            xy=(7, 97.3), xytext=(5.5, 85),
            arrowprops=dict(arrowstyle="->", color=PALETTE["red"]),
            fontsize=8, color=PALETTE["red"], ha="center")

plt.tight_layout()
plt.savefig(OUT + "fig2_type2_by_protocol.png", dpi=180,
            bbox_inches="tight", facecolor=PALETTE["bg"])
plt.close()
print("Fig 2 saved")

# ══════════════════════════════════════════════════════════════════
# FIG 3 — % Type-2 by vendor (horizontal bar)
# ══════════════════════════════════════════════════════════════════
vendors = ["Mistral\n(Medium-3.1)", "OpenAI\n(GPT-4o)",
           "Anthropic\n(Claude S4)", "Meta\n(Llama-4-M)",
           "DeepSeek\n(Chat)", "Alibaba\n(Qwen-3-235B)"]
vpcts   = [29.9, 26.5, 26.5, 22.8, 22.5, 19.6]

fig, ax = plt.subplots(figsize=(9, 5), facecolor=PALETTE["bg"])
ax.set_facecolor(PALETTE["bg"])
colors_v = [PALETTE["red"] if p > 27 else
            PALETTE["orange"] if p > 24 else
            PALETTE["blue"] for p in vpcts]
bars = ax.barh(vendors, vpcts, color=colors_v,
               edgecolor="white", linewidth=1.2, zorder=3)
ax.set_xlim(0, 40)
ax.set_xlabel("Responses requiring Type-2 representation (%)", fontsize=10)
ax.set_title("Figure 3. Cross-Vendor Consistency (S4-O protocols)\n"
             "All 6 independent vendors exhibit Type-2 behaviour (19–30%)",
             fontsize=11, fontweight="bold")
ax.axvline(0, color="#cccccc", linewidth=0.8)
ax.grid(axis="x", color="#e0e0e0", zorder=0)
ax.spines[["top","right"]].set_visible(False)
for bar, pct in zip(bars, vpcts):
    ax.text(pct + 0.5, bar.get_y() + bar.get_height()/2,
            f"{pct:.1f}%", va="center", fontsize=10, fontweight="bold")
ax.axvline(np.mean(vpcts), color=PALETTE["purple"], linestyle="--",
           linewidth=1.5, label=f"Mean: {np.mean(vpcts):.1f}%", zorder=4)
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(OUT + "fig3_type2_by_vendor.png", dpi=180,
            bbox_inches="tight", facecolor=PALETTE["bg"])
plt.close()
print("Fig 3 saved")

# ══════════════════════════════════════════════════════════════════
# FIG 4 — 3D scatter: S4-O responses in T×I×F space
# ══════════════════════════════════════════════════════════════════
df = pd.read_csv(
    "C:/Users/HP/Documents/BreakingChains_v3_Empirical/data/v3_multivendor_results.csv"
)
df["T"] = pd.to_numeric(df["T"], errors="coerce")
df["I"] = pd.to_numeric(df["I"], errors="coerce")
df["F"] = pd.to_numeric(df["F"], errors="coerce")
df = df.dropna(subset=["T","I","F"])
df["is_type2"] = (df["T"]<0)|(df["T"]>1)|(df["I"]>1)|(df["F"]>1)

sao = df[df["protocol"].isin(["S4-O.A","S4-O.C"])].copy()

fig = plt.figure(figsize=(10, 8), facecolor=PALETTE["bg"])
ax3 = fig.add_subplot(111, projection="3d", facecolor=PALETTE["bg"])

t1 = sao[~sao["is_type2"]]
t2 = sao[sao["is_type2"]]
ax3.scatter(t1["T"], t1["I"], t1["F"],
            c=PALETTE["grey"], alpha=0.35, s=18, label="Type-1 admissible")
ax3.scatter(t2["T"], t2["I"], t2["F"],
            c=PALETTE["red"], alpha=0.6, s=28, label="Requires Type-2")

# Witness
ax3.scatter([1.7], [1.8], [1.6], c=PALETTE["purple"], s=200,
            marker="*", zorder=10, label="Mistral witness (1.7, 1.8, 1.6)")

# Unit cube wireframe [0,1]^3
r = [0, 1]
for s, e in [(0,0),(0,1),(1,0),(1,1)]:
    ax3.plot([r[s],r[e]],[r[s],r[s]],[0,0], "k-", alpha=0.25, lw=0.8)
    ax3.plot([0,0],[r[s],r[e]],[r[s],r[e]], "k-", alpha=0.25, lw=0.8)
    ax3.plot([r[s],r[s]],[0,1],[r[s],r[s]], "k-", alpha=0.25, lw=0.8)
    ax3.plot([r[s],r[e]],[1,1],[r[s],r[s]], "k-", alpha=0.25, lw=0.8)
    ax3.plot([1,1],[r[s],r[e]],[r[s],r[s]], "k-", alpha=0.25, lw=0.8)
    ax3.plot([r[s],r[s]],[r[s],r[s]],[0,1], "k-", alpha=0.25, lw=0.8)

ax3.set_xlabel("T (Truth)", fontsize=9, labelpad=8)
ax3.set_ylabel("I (Indeterm.)", fontsize=9, labelpad=8)
ax3.set_zlabel("F (Falsity)", fontsize=9, labelpad=8)
ax3.set_title("Figure 4. LLM Responses in T × I × F Space (S4-O Protocols)\n"
              "Red = require Type-2 (outside unit cube) · Wireframe = Type-1 boundary",
              fontsize=10, fontweight="bold")
ax3.legend(fontsize=8, loc="upper left")
ax3.view_init(elev=22, azim=45)
plt.tight_layout()
plt.savefig(OUT + "fig4_scatter_3d.png", dpi=180,
            bbox_inches="tight", facecolor=PALETTE["bg"])
plt.close()
print("Fig 4 saved")

# ══════════════════════════════════════════════════════════════════
# FIG 5 — Witness mapping: Type-1 inadmissible → Type-2 representation
# ══════════════════════════════════════════════════════════════════
fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(13, 6),
                                         facecolor=PALETTE["bg"])
fig.suptitle(
    "Figure 5. Worked Example: Mistral Witness (T=1.7, I=1.8, F=1.6)\n"
    "Statement: \"Lying to save an innocent life is morally right and wrong at the same time.\"",
    fontsize=10, fontweight="bold"
)

# LEFT: Type-1 with crossed-out values
ax_left.set_xlim(0, 10); ax_left.set_ylim(0, 10)
ax_left.axis("off")
ax_left.set_title("Type-1 representation\n(INADMISSIBLE — values outside [0,1])",
                   fontsize=10, color=PALETTE["red"])
for i, (lbl, val, col) in enumerate(zip(["T","I","F"],
                                         [1.7, 1.8, 1.6],
                                         colors_tif)):
    box = FancyBboxPatch((1.5, 6.5 - i*2.8), 7, 2.2,
                          boxstyle="round,pad=0.3",
                          fc=col, ec="white", alpha=0.25, lw=2,
                          linestyle="--")
    ax_left.add_patch(box)
    ax_left.text(5.0, 7.6 - i*2.8, f"{lbl} = {val}",
                  ha="center", va="center", fontsize=16,
                  fontweight="bold", color=col)
    ax_left.text(5.0, 7.0 - i*2.8,
                  f"⚠ outside [0, 1]",
                  ha="center", va="center", fontsize=9,
                  color=PALETTE["red"])
    # Cross out
    ax_left.plot([1.5, 8.5], [6.5 - i*2.8, 8.7 - i*2.8],
                  color=PALETTE["red"], lw=2, alpha=0.6)
    ax_left.plot([1.5, 8.5], [8.7 - i*2.8, 6.5 - i*2.8],
                  color=PALETTE["red"], lw=2, alpha=0.6)

# RIGHT: Type-2 valid representation
ax_right.set_xlim(0, 10); ax_right.set_ylim(0, 10)
ax_right.axis("off")
ax_right.set_title("Type-2 representation\n(VALID — all sub-components in [0,1])",
                    fontsize=10, color=PALETTE["green"])

type2_data = [
    ("T", 1.7, [("T_T", 1.0, "Maximally true"),
                ("I_T", 0.7, "70% hyper-indeterminate"),
                ("F_T", 0.0, "Not false")]),
    ("I", 1.8, [("T_I", 1.0, "Indeterminacy confirmed"),
                ("I_I", 0.8, "80% uncertain about I"),
                ("F_I", 0.0, "Not absent")]),
    ("F", 1.6, [("T_F", 1.0, "Falsity present"),
                ("I_F", 0.6, "60% uncertain about F"),
                ("F_F", 0.0, "Not absent")]),
]

for i, (comp, val, subs) in enumerate(type2_data):
    y_outer = 8.8 - i * 3.1
    outer = FancyBboxPatch((0.3, y_outer - 2.5), 9.4, 2.8,
                            boxstyle="round,pad=0.2",
                            fc=colors_tif[i], ec="white", alpha=0.15, lw=1.5)
    ax_right.add_patch(outer)
    ax_right.text(0.7, y_outer - 0.9, f"{comp} = {val} →",
                   fontsize=11, fontweight="bold", color=colors_tif[i],
                   va="center")
    for j, (sub_lbl, sub_val, interp) in enumerate(subs):
        xpos = 2.5 + j * 2.5
        inner = FancyBboxPatch((xpos - 0.8, y_outer - 2.3), 2.2, 1.8,
                                boxstyle="round,pad=0.1",
                                fc=colors_tif[j], ec="white", alpha=0.7)
        ax_right.add_patch(inner)
        ax_right.text(xpos + 0.3, y_outer - 1.0,
                       f"{sub_lbl}\n= {sub_val}",
                       ha="center", va="center", fontsize=8,
                       fontweight="bold", color="white")
        ax_right.text(xpos + 0.3, y_outer - 2.05,
                       interp, ha="center", va="center",
                       fontsize=6, color="#444444")

plt.tight_layout()
plt.savefig(OUT + "fig5_witness_type2_mapping.png", dpi=180,
            bbox_inches="tight", facecolor=PALETTE["bg"])
plt.close()
print("Fig 5 saved")
print("\nAll figures saved to:", OUT)
