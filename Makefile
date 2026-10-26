# Run the whole thing with a single command:  make
#
# Each step depends on the one before it, so `make` will fetch the data, clean
# it, work out the figures, draw the charts and run the checks, in that order.

PYTHON = ./.venv/bin/python

.PHONY: all setup clean-outputs test

all: outputs/money_vs_claims.png outputs/money_owed_over_time.png test

setup:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

data/raw/annual_statistics_2025_26.xlsx:
	$(PYTHON) src/fetch_data.py

data/processed/liabilities_by_specialty.csv: data/raw/annual_statistics_2025_26.xlsx src/clean_data.py
	$(PYTHON) src/clean_data.py

outputs/money_vs_claims_latest_year.csv: data/processed/liabilities_by_specialty.csv src/analyse.py
	$(PYTHON) src/analyse.py

outputs/money_vs_claims.png outputs/money_owed_over_time.png: outputs/money_vs_claims_latest_year.csv src/chart.py
	$(PYTHON) src/chart.py

test:
	$(PYTHON) -m pytest tests/ -q

clean-outputs:
	rm -f data/processed/*.csv outputs/*.png outputs/*.csv
