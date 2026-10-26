"""
Step 2 of 3: turn the spreadsheet into clean tables.

The published spreadsheet is built for people to read, not for a computer.
Each sheet stacks several tables on top of each other, headings sit in odd
places, and some cells hold a "#" instead of a number. This script pulls out
the two tables we need and writes them as plain CSV files.

Two rules are applied here, both explained in NOTES.md:

1. "#" means the real figure was hidden to protect patient privacy, because it
   was under 5 claims or under GBP 5,000. It is NOT zero, so it becomes blank.
2. Money figures before 2015/16 are blank in the source, not zero, because NHS
   Resolution did not record them at this level of detail then. Those years are
   dropped from the money table.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "annual_statistics_2025_26.xlsx"
PROCESSED = ROOT / "data" / "processed"

# Rows that are sums rather than real specialties. Kept out of the specialty
# tables so that we never accidentally add a total to its own parts.
# Rows that are sums or accounting adjustments rather than a medical specialty.
# "Estimated Settlement Date Overlay" and "Incurred but not Reported" are
# actuarial adjustments to the total, not claims against a department, so they
# must never be ranked alongside specialties.
TOTAL_ROWS = {
    "total",
    "total - known claims",
    "incurred but not reported",
    "estimated settlement date",
    "grand total",
}

# Money at this level of detail only exists from this year onwards.
MONEY_FIRST_YEAR = "2015/16"


def is_total_row(name: str) -> bool:
    """True if this row is a sum rather than a single specialty."""
    cleaned = str(name).strip().lower()
    return any(cleaned.startswith(t) for t in TOTAL_ROWS)


def read_table(sheet: str, table_label: str, row_label: str = "Specialty") -> pd.DataFrame:
    """
    Pull one table out of one sheet.

    We do not trust row numbers, because they differ between sheets. Instead we
    find the table's heading, then the first row underneath it whose first cell
    matches `row_label`. That row holds the years. Everything below it, until
    the first empty row, is the data.

    `row_label` is "Specialty" for the tables split by medical specialty, and
    "Damages value band" for the tables split by size of payout.
    """
    sheet_data = pd.read_excel(RAW, sheet_name=sheet, header=None)
    labels = sheet_data[2].astype(str)

    start = labels[labels.str.startswith(table_label)].index
    if len(start) == 0:
        raise ValueError(f"Could not find {table_label!r} on sheet {sheet!r}")
    start = start[0]

    header_matches = labels[(labels.index > start) & (labels.str.strip() == row_label)].index
    if len(header_matches) == 0:
        raise ValueError(f"No {row_label!r} heading under {table_label!r}")
    header_row = header_matches[0]

    years = [str(y).strip() for y in sheet_data.iloc[header_row, 3:].tolist()]
    years = [y for y in years if y != "nan"]

    rows = []
    for position in range(header_row + 1, len(sheet_data)):
        name = sheet_data.iloc[position, 2]
        if pd.isna(name) or str(name).strip() == "":
            break
        rows.append([str(name).strip()] + sheet_data.iloc[position, 3 : 3 + len(years)].tolist())

    table = pd.DataFrame(rows, columns=["category"] + years)
    return table


def to_long(table: pd.DataFrame, value_name: str, label: str = "specialty") -> pd.DataFrame:
    """
    Reshape from one-column-per-year into one row per category per year.

    This shape is easier to filter and chart, and it is the shape most analysis
    tools expect.
    """
    if "specialty" in table.columns:
        table = table.rename(columns={"specialty": "category"})
    long = table.melt(id_vars="category", var_name="year", value_name=value_name)
    long = long.rename(columns={"category": label})
    long["is_total"] = long[label].map(is_total_row)

    # "#" means hidden for privacy. Treat as missing, never as zero.
    long["suppressed"] = long[value_name].astype(str).str.strip() == "#"
    long[value_name] = pd.to_numeric(long[value_name], errors="coerce")
    return long


def build() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)

    claims = to_long(read_table("B", "Table B.1"), "claims")
    money = to_long(read_table("F", "Table F.1"), "liability_gbp")

    # The same two measures, split by the size of the payout instead of by
    # medical specialty. This gives a second, independent way of checking
    # whether a few large claims drive most of the money.
    band_label = "Damages value band"
    claims_band = to_long(read_table("A", "Table A.1", band_label), "claims", label="band")
    money_band = to_long(read_table("E", "Table E.1", band_label), "liability_gbp", label="band")

    # Drop the years where money was not recorded at this level of detail.
    money = money[money["year"] >= MONEY_FIRST_YEAR].copy()
    money_band = money_band[money_band["year"] >= MONEY_FIRST_YEAR].copy()

    claims.to_csv(PROCESSED / "claims_by_specialty.csv", index=False)
    money.to_csv(PROCESSED / "liabilities_by_specialty.csv", index=False)
    claims_band.to_csv(PROCESSED / "claims_by_band.csv", index=False)
    money_band.to_csv(PROCESSED / "liabilities_by_band.csv", index=False)

    print(f"claims notified   {claims['year'].min()} to {claims['year'].max()}  "
          f"{claims['specialty'].nunique()} rows per year, "
          f"{int(claims['suppressed'].sum())} hidden cells")
    print(f"money owed        {money['year'].min()} to {money['year'].max()}  "
          f"{money['specialty'].nunique()} rows per year, "
          f"{int(money['suppressed'].sum())} hidden cells")
    print(f"by payout size    claims {claims_band['band'].nunique()} bands, "
          f"money {money_band['band'].nunique()} bands, "
          f"{int(claims_band['suppressed'].sum()) + int(money_band['suppressed'].sum())} hidden cells")


if __name__ == "__main__":
    build()
