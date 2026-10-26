# Working notes

Every judgement call made while cleaning or analysing goes here, with the date and the reason.
These notes are the most valuable part of the project. They are what turns a chart into evidence
of analytical judgement, and they are what an interview panel will ask about.

Record, at minimum:

- a decision you made about the data, and the alternative you rejected
- a point where two sources disagreed, and which you trusted
- an assumption you had to make, and what would change if it were wrong
- something you expected to see and did not

## Log

### 26 October 2026 — first look at the data

**What we have.** One spreadsheet from NHS Resolution covering 2006/07 to 2025/26, with six
tables: claims reported, claims settled, and money owed, each split two ways, by medical
specialty and by the size of the payout. Each table is repeated for every insurance scheme, plus
a combined "all schemes" version.

**Trap 1: nine years of the money data are blank, not zero.**
The money owed column reads 0 for every year from 2006/07 to 2014/15, then jumps to £22.9bn in
2015/16. Anyone plotting that straight would show costs exploding out of nothing. The spreadsheet's
own notes explain it:

> "Granular level financial liabilities data in respect of known claims is only available from
> 2015/16 onwards."

So those zeros mean "we did not record it this way back then". Any analysis of money owed has to
start at 2015/16.

**Trap 2: the £20bn jump in 2021/22 is a change of method, not a change in reality.**
Money owed runs 37.0, 39.7, then **59.5** in 2021/22, then falls back to 40.9. A reader would
conclude costs spiked and then collapsed. The notes say the calculation itself changed:

> "For the financial years 2021/22 and prior, the Estimated Settlement Date (ESD) element ... was
> used to calculate the known claims provision ... Since 2022/23, an actuarial view on payment
> patterns has instead been used"

So the figures before and after 2022/23 are not measuring the same thing in the same way.

**Three more breaks in the data, from the same notes:**

- Any count below 5, or any amount below £5,000, is replaced with "#" to stop individual patients
  being identified. Those cells need handling, not deleting.
- A "Neonatology" specialty was created on 1 April 2021. Before that those claims sat inside
  "Other", so both series bend at that point.
- A scheme covering GP care (CNSGP) started on 1 April 2019, so the combined totals grow partly
  because new kinds of claim were added, not because existing claims grew.

**One thing already visible.** In the latest year, obstetric brain-damage and cerebral-palsy
claims account for roughly £20.8bn of the £37.6bn owed on known claims. One category, more than
half the money. That is the long-tail shape we wanted to test for.

**The data covers England only.**

### 26 October 2026 — the finding, and the thing to be careful about

**The finding.** In 2025/26, obstetric claims involving cerebral palsy or brain damage were
**252 of the 15,236 claims reported, about 1.7%**. That same category accounts for
**£20.8bn of the £37.6bn owed on known claims, about 55%**. Four categories account for 80% of
the money. At the other end, the "Other" grouping produced 39% of claims and 8% of the money.

**The care point, which must stay in the write-up.** The two percentages are not slices of the
same pie. Claims reported counts claims that arrived during 2025/26. Money owed covers every open
claim at the year end, including ones reported years earlier. Brain injury claims take a long time
to settle, so they build up in the open pile. Saying "1.7% of claims cause 55% of costs" would be
wrong. Saying "this category is a small share of new claims and a large share of money owed" is
right, and is still the point.

**Why the finding is not surprising once you think about it.** A birth injury can mean a lifetime
of care for someone who would otherwise have had a full life expectancy, so a single claim can run
to millions. Most other claims are far smaller. This is the normal shape of insurance costs and it
is why an average claim cost tells you very little on its own.

**What this does not show.** Nothing about whether care is getting better or worse, nothing about
fault, and nothing about claims in Scotland, Wales or Northern Ireland, since NHS Resolution covers
England only.
