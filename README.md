# Where the money sits in NHS clinical negligence claims

**In one sentence:** a small group of birth-injury claims accounts for more than half of all the
money the NHS in England owes on clinical negligence claims, while the great majority of claims
account for very little of it.

![Share of claims against share of money owed, by specialty](outputs/money_vs_claims.png)

## The question

When the NHS is sued over care that went wrong, the money owed has to be estimated years before
most of it is paid. If that money is spread evenly across all claims, planning for it is
straightforward. If a handful of claims drive most of the cost, it is not, because a change in a
few large cases moves the total far more than a change in the many small ones.

So: **which parts of the NHS account for the money owed, and how concentrated is it?**

## What the figures show

In 2025/26:

- The NHS in England owed **£37.6 billion** on clinical negligence claims it already knows about.
- **15,236** new claims were reported during the year.
- **Obstetric claims involving cerebral palsy or brain damage** made up about **1.7%** of the
  claims reported, and account for about **55%** of the money owed.
- **Four categories account for 80%** of the money: obstetric brain injury, paediatrics, the mixed
  "Other" grouping, and other obstetric claims.
- At the opposite end, the "Other" grouping produced **39% of claims** and about **8%** of the
  money.

Once you think about what a birth injury means, the result makes sense. A child who needs care for
the whole of a normal lifespan is enormously expensive to compensate, while most claims are far
smaller. This is the usual shape of insurance costs, and it is why an average claim cost on its own
tells you almost nothing.

## Two things in the data that could have produced a wrong answer

**Nine years of zeros that are not zeros.** The money column reads 0 for every year from 2006/07
to 2014/15. That is not because nothing was owed. NHS Resolution's own notes say this level of
detail "is only available from 2015/16 onwards". Charting those years as written would show costs
appearing out of nowhere. They are excluded.

**A £20 billion jump that is a change of method, not of reality.** Money owed runs £37.0bn, then
£39.7bn, then £59.5bn in 2021/22, then falls back to £40.9bn. The notes explain that from 2022/23
the sum is worked out differently, using an actuarial view of when claims will be paid rather than
an estimated settlement date. Figures either side of that change are not measuring the same thing,
so the change is marked rather than smoothed over.

## What this does not show, and one thing to read carefully

The two bars on the chart are **not two slices of one pie**. Claims reported counts claims that
arrived during the year. Money owed covers every claim still open at the year end, including ones
reported long before. Brain injury claims take years to resolve, so they build up in the open pile.
It would be wrong to say "1.7% of claims cause 55% of costs". What is right, and is still the
point, is that this category is a small share of new claims and a very large share of money owed.

The figures also say nothing about whether care is getting better or worse, nothing about fault,
and nothing about Scotland, Wales or Northern Ireland. NHS Resolution covers England only.

Counts below 5 and amounts below £5,000 are hidden in the published data to protect patient
privacy. Those are treated as missing, never as zero.

## Where the numbers come from

NHS Resolution, *Annual Report Statistics 2025/26*, covering 2006/07 to 2025/26.
Published at <https://resolution.nhs.uk/resources/annual-statistics-including-factsheet-5/>

## Running it yourself

Everything runs from the three scripts in `src/`, in order. The spreadsheet is downloaded once and
reused, so the result is the same every time.

```
python3 -m venv .venv
./.venv/bin/pip install pandas matplotlib requests openpyxl pytest

./.venv/bin/python src/fetch_data.py    # download the published spreadsheet
./.venv/bin/python src/clean_data.py    # turn it into clean tables
./.venv/bin/python src/analyse.py       # work out the shares
./.venv/bin/python src/chart.py         # draw the chart

./.venv/bin/python -m pytest tests/     # check the cleaning rules still hold
```

## How it is put together

| Folder | What is in it |
|---|---|
| `src/` | The four steps: fetch, clean, analyse, chart |
| `data/raw/` | The spreadsheet exactly as published, never edited |
| `data/processed/` | Clean tables written by the cleaning step |
| `outputs/` | The chart and the summary table |
| `tests/` | Checks on the two cleaning rules that matter most |
| `NOTES.md` | Every judgement call made along the way, and why |

Raw data is never edited by hand. Every change happens in a script, so anyone can see what was done
and get the same answer. `NOTES.md` is the honest record of the decisions, including the ones that
were not obvious.
