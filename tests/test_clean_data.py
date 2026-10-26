"""
Checks on the cleaning rules.

These exist so that if someone changes the cleaning code later, the two rules
that matter most cannot quietly stop working:

1. A "#" in the spreadsheet means "hidden to protect privacy". It must become
   blank, never zero. Turning it into zero would understate the real figures.
2. Rows that are sums or accounting adjustments must never be mistaken for a
   medical specialty, or a total would be ranked against its own parts.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from clean_data import is_total_row, to_long  # noqa: E402


@pytest.mark.parametrize(
    "label",
    [
        "Total",
        "Total - Known claims",
        "Incurred but not Reported (IBNR)",
        "Estimated Settlement Date Overlay",
        "Grand Total",
        "  grand total  ",
    ],
)
def test_sum_and_adjustment_rows_are_recognised(label):
    assert is_total_row(label) is True


@pytest.mark.parametrize(
    "label",
    [
        "Obstetrics CP/BD",
        "Paediatrics",
        "Emergency Medicine",
        "Other",
        "Urology",
    ],
)
def test_real_specialties_are_not_treated_as_totals(label):
    assert is_total_row(label) is False


def test_hidden_values_become_blank_not_zero():
    table = pd.DataFrame({"specialty": ["Urology"], "2024/25": ["#"]})
    result = to_long(table, "claims")

    assert result.loc[0, "suppressed"] is True or bool(result.loc[0, "suppressed"]) is True
    assert pd.isna(result.loc[0, "claims"]), "a hidden value must not be read as zero"


def test_ordinary_numbers_survive_cleaning():
    table = pd.DataFrame({"specialty": ["Urology"], "2024/25": [305]})
    result = to_long(table, "claims")

    assert result.loc[0, "claims"] == 305
    assert bool(result.loc[0, "suppressed"]) is False


def test_long_shape_has_one_row_per_specialty_per_year():
    table = pd.DataFrame(
        {"specialty": ["A", "B"], "2023/24": [1, 2], "2024/25": [3, 4]}
    )
    result = to_long(table, "claims")
    assert len(result) == 4
    assert set(result.columns) == {"specialty", "year", "claims", "is_total", "suppressed"}
