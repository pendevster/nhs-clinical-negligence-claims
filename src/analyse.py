"""
Step 3 of 3: work out where the money sits.

Question: in the most recent year, which medical specialties account for the
money the NHS owes on clinical negligence claims, and how concentrated is it?

The interesting comparison is between how MANY claims a specialty produces and
how MUCH money it accounts for. If those two line up, cost is spread evenly. If
they do not, a small number of claims drive most of the cost, which is the
normal shape for insurance and matters a great deal for planning.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

KNOWN_CLAIMS_TOTAL = "Total - Known claims"
CLAIMS_TOTAL = "Total"


def latest_year(frame: pd.DataFrame) -> str:
    return sorted(frame["year"].unique())[-1]


def share_table() -> pd.DataFrame:
    money = pd.read_csv(PROCESSED / "liabilities_by_specialty.csv")
    claims = pd.read_csv(PROCESSED / "claims_by_specialty.csv")

    year = latest_year(money)

    money_year = money[(money["year"] == year) & (~money["is_total"])]
    money_total = money[(money["year"] == year)
                        & (money["specialty"] == KNOWN_CLAIMS_TOTAL)]["liability_gbp"].iloc[0]

    claims_year = claims[(claims["year"] == year) & (~claims["is_total"])]
    claims_total = claims[(claims["year"] == year)
                          & (claims["specialty"] == CLAIMS_TOTAL)]["claims"].iloc[0]

    merged = money_year[["specialty", "liability_gbp"]].merge(
        claims_year[["specialty", "claims"]], on="specialty", how="outer"
    )
    merged["money_share"] = merged["liability_gbp"] / money_total * 100
    merged["claims_share"] = merged["claims"] / claims_total * 100
    merged = merged.sort_values("liability_gbp", ascending=False).reset_index(drop=True)
    merged["money_share_cumulative"] = merged["money_share"].cumsum()
    merged.attrs["year"] = year
    merged.attrs["money_total"] = money_total
    merged.attrs["claims_total"] = claims_total
    return merged


if __name__ == "__main__":
    OUTPUTS.mkdir(exist_ok=True)
    table = share_table()
    year = table.attrs["year"]

    print(f"\nYear: {year}")
    print(f"Money owed on known claims: GBP {table.attrs['money_total']/1e9:,.1f}bn")
    print(f"Claims reported that year:  {table.attrs['claims_total']:,.0f}\n")

    show = table[["specialty", "liability_gbp", "money_share", "claims", "claims_share",
                  "money_share_cumulative"]].copy()
    show["liability_gbp"] = (show["liability_gbp"] / 1e9).round(2)
    show = show.round(1)
    show.columns = ["specialty", "GBPbn", "money %", "claims", "claims %", "cumulative money %"]
    print(show.to_string(index=False))

    table.to_csv(OUTPUTS / "money_vs_claims_latest_year.csv", index=False)
