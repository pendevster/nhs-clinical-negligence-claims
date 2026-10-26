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



def draw_trend() -> Path:
    """
    Money owed on known claims, year by year.

    The important feature is the break. From 2022/23 NHS Resolution changed how
    this sum is worked out, so the figures before and after are not measuring
    the same thing. The chart marks that rather than drawing one smooth line
    through it, because a reader who joined the two halves would conclude that
    costs spiked and then collapsed, which is not what happened.
    """
    money = pd.read_csv(ROOT / "data" / "processed" / "liabilities_by_specialty.csv")
    totals = money[money["specialty"] == "Total - Known claims"].copy()
    totals = totals.sort_values("year")
    totals["billions"] = totals["liability_gbp"] / 1e9

    old_method = totals[totals["year"] <= "2021/22"]
    new_method = totals[totals["year"] >= "2022/23"]

    figure, axes = plt.subplots(figsize=(10, 5.5))
    axes.plot(old_method["year"], old_method["billions"], marker="o",
              color="#4878A8", label="Worked out the old way")
    axes.plot(new_method["year"], new_method["billions"], marker="o",
              color="#B5451C", label="Worked out the new way, from 2022/23")

    boundary = list(totals["year"]).index("2022/23") - 0.5
    axes.axvline(boundary, color="#888", linestyle="--", linewidth=1)
    axes.annotate("method changed here",
                  xy=(boundary, axes.get_ylim()[1] * 0.97),
                  xytext=(boundary + 0.15, axes.get_ylim()[1] * 0.97),
                  fontsize=9, color="#444", va="top")

    axes.set_ylabel("GBP billions owed on known claims\n(cash terms, not adjusted for inflation)")
    axes.set_title("The 2021/22 peak is a change of method, not a change in costs\n"
                   "NHS clinical negligence, England",
                   loc="left", fontsize=13, fontweight="bold")
    axes.legend(loc="lower right", frameon=False)
    axes.spines[["top", "right"]].set_visible(False)
    axes.tick_params(axis="x", rotation=45)

    figure.text(0.01, -0.06,
                "Before 2022/23 the sum used an estimated settlement date for each claim. From "
                "2022/23 it uses an actuarial view of when claims\nwill actually be paid. The two "
                "halves are therefore not comparable, and the apparent peak and fall should not be "
                "read as costs\nrising and then dropping. Figures before 2015/16 are not published "
                "at this level of detail.\nFigures are in cash terms at each year end, so part of the rise is general price inflation rather than more or costlier claims.\nSource: NHS Resolution, Annual Report Statistics 2025/26.",
                fontsize=7.5, color="#444", va="top")

    figure.tight_layout()
    target = OUTPUTS / "money_owed_over_time.png"
    figure.savefig(target, dpi=160, bbox_inches="tight")
    print(f"chart written to {target}")
    return target



def draw_bands() -> Path:
    """
    The same finding reached a second way: by size of payout.

    This is the clearer picture of the two, because it compares like with like.
    Most claims are small and account for almost none of the money. A small
    number of very large claims account for most of it.
    """
    table = pd.read_csv(OUTPUTS / "money_vs_claims_by_band.csv")
    table = table.iloc[::-1]

    positions = range(len(table))
    height = 0.4

    figure, axes = plt.subplots(figsize=(10, 6))
    axes.barh([p + height / 2 for p in positions], table["money_share"],
              height=height, label="Share of money owed", color="#B5451C")
    axes.barh([p - height / 2 for p in positions], table["claims_share"],
              height=height, label="Share of claims reported", color="#4878A8")

    axes.set_yticks(list(positions))
    axes.set_yticklabels(table["band"])
    axes.set_xlabel("Percent")
    axes.set_ylabel("Size the claim is valued at")
    axes.set_title("Most claims are small. Most of the money is in a few very large ones.\n"
                   "NHS clinical negligence, England, 2025/26",
                   loc="left", fontsize=13, fontweight="bold")
    axes.legend(loc="upper right", frameon=False)
    axes.spines[["top", "right"]].set_visible(False)

    figure.text(0.01, -0.02,
                "Claims valued at GBP 4.5m and over are 2.6% of the claims reported in 2025/26 and "
                "80.3% of the money owed.\nClaims reported during the year (15,236). Money owed on "
                "all open known claims at 31 March 2026 (GBP 37.6bn). The two measures\ncover "
                "different groups of claims. Source: NHS Resolution, Annual Report Statistics "
                "2025/26.",
                fontsize=7.5, color="#444", va="top")

    figure.tight_layout()
    target = OUTPUTS / "money_vs_claims_by_band.png"
    figure.savefig(target, dpi=160, bbox_inches="tight")
    print(f"chart written to {target}")
    return target


if __name__ == "__main__":
    draw()
    draw_bands()
    draw_trend()
