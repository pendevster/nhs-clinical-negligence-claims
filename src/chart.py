"""
Draw the picture.

One chart, showing for each medical specialty two things side by side:
how big a share of the claims it produced, and how big a share of the money it
accounts for. Where the two bars differ sharply, a small number of claims is
driving a large amount of money.

The two bars are measured on different bases, which the caption says plainly:
claims are those reported during the year, money is what is owed on every open
claim at the year end. They are not two slices of the same pie.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"


def draw() -> Path:
    table = pd.read_csv(OUTPUTS / "money_vs_claims_latest_year.csv")
    table = table.dropna(subset=["money_share"]).head(10).iloc[::-1]

    positions = range(len(table))
    height = 0.4

    figure, axes = plt.subplots(figsize=(10, 6))
    axes.barh([p + height / 2 for p in positions], table["money_share"],
              height=height, label="Share of money owed", color="#B5451C")
    axes.barh([p - height / 2 for p in positions], table["claims_share"],
              height=height, label="Share of claims reported", color="#4878A8")

    axes.set_yticks(list(positions))
    axes.set_yticklabels(table["specialty"])
    axes.set_xlabel("Percent")
    axes.set_title("A small number of claims accounts for most of the money\n"
                   "NHS clinical negligence, England, 2025/26",
                   loc="left", fontsize=13, fontweight="bold")
    axes.legend(loc="lower right", frameon=False)
    axes.spines[["top", "right"]].set_visible(False)

    figure.text(0.01, -0.02,
                "Claims reported during 2025/26 (15,236 in total). Money owed on all open known "
                "claims at 31 March 2026 (GBP 37.6bn).\nThe two measures cover different groups of "
                "claims and are shown together for comparison, not as parts of one whole.\n"
                "Source: NHS Resolution, Annual Report Statistics 2025/26.",
                fontsize=7.5, color="#444", va="top")

    figure.tight_layout()
    target = OUTPUTS / "money_vs_claims.png"
    figure.savefig(target, dpi=160, bbox_inches="tight")
    print(f"chart written to {target}")
    return target


if __name__ == "__main__":
    draw()
