"""
Step 1 of 3: fetch the published figures.

This downloads the yearly statistics that NHS Resolution publishes about
clinical negligence claims, and saves the file into data/raw/.

Why a script rather than clicking a download link: so that anyone, including
you in six months, can run one command and get exactly the same starting data.
If the file is already there, it is not downloaded again.
"""

from pathlib import Path
import requests

# Where the published figures live. Source page:
# https://resolution.nhs.uk/resources/annual-statistics-including-factsheet-5/
SOURCES = {
    "annual_statistics_2025_26.xlsx": (
        "https://resolution.nhs.uk/wp-content/uploads/2026/10/"
        "Annual-Reports-Statistics-NHS-Resolution-2025_26-ACC-CHECKED.xlsx"
    ),
}

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def fetch(filename: str, url: str) -> Path:
    """Download one file into data/raw, unless we already have it."""
    RAW.mkdir(parents=True, exist_ok=True)
    target = RAW / filename

    if target.exists():
        print(f"already have   {filename}  ({target.stat().st_size:,} bytes)")
        return target

    print(f"downloading    {filename}")
    response = requests.get(url, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    target.write_bytes(response.content)
    print(f"saved          {filename}  ({target.stat().st_size:,} bytes)")
    return target


if __name__ == "__main__":
    for name, url in SOURCES.items():
        fetch(name, url)
