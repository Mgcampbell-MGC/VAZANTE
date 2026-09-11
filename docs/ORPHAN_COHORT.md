# Are the orphan estates already on the list, or the wrong asset class?

11 September 2026. One query, run before anyone is called. Reproduce with
`.venv/bin/python scripts/orphan_cohort.py`.

**The answer is both, and the split is clean.** The nine orphan funds worth buying are already on the target list
on their own merits, under their new administradores. The other 522 are financial-sector paper the desk cannot
use. Calling a receiver adds nothing the screen has not already given you.

---

## First, a correction to my own earlier count

I previously reported the orphan cohort as 161 classes, grouped by the administrador name showing in the July
2026 informe. That was wrong by a factor of more than three, and wrong in a way that mattered.

A fund whose administrador is liquidated keeps its own CNPJ and moves to a new administrador. Grouping on the
current name counts only the ones that have not moved yet. Built properly, from every administrador a class has
ever had across 44 months, plus Reag (which never appears as an administrador at all and shows up only as a
gestora in the live register, on 125 classes), the cohort is **780 classes**.

| | Classes |
|---|---|
| Ever under Trustee, Banvox, Master, CBSF, Sefer or Reag | 780 |
| Filed a July 2026 informe | 531 (68%) |
| Gone dark | 249 |
| Of the survivors, still under the old administrador's name | 161 |
| **Of the survivors, already moved to a new administrador** | **370** |

The estates have largely re-homed themselves. Where they went:

| New administrador | Classes taken on |
|---|---|
| Planner Corretora | 61 |
| Actual Distribuidora | 32 |
| Qore | 31 |
| ID Corretora | 30 |
| Catálise | 28 |
| Banco Daycoval | 27 |
| Limine Trust | 24 |
| FIDD | 23 |

---

## Which filter kills them

Walking the 531 survivors through the screen in order, and recording the first gate each one fails:

| Gate | Kills | PL behind it |
|---|---|---|
| Not a FIDC in the register | 4 | R$0.04bn |
| **Provision below 25% of carteira** | **428** | R$116.28bn |
| Business-to-business paper below 60% | 73 | R$8.09bn |
| Visibly captive | 14 | R$0.58bn |
| Carteira below R$60m | 11 | R$0.34bn |
| Survives every gate | 1 | R$0.36bn |

Two things fall out of this table, and the first is the surprise.

**The provision gate does most of the killing, which means these funds are not distressed.** 428 of 531 carry a
provision below 25% of the carteira. Only 100 have the loss booked. The orphan estates were orphaned by their
administrador's failure, not by their own credit going bad, and under a new administrador most of them are
carrying ordinary numbers. "Orphaned" and "broken" are different conditions, and the market narrative conflates
them.

**The one fund that survives every gate is Del Cred NP**, which is Master lineage and which the desk research
then disqualified as the captive vehicle of the Del Cred factoring group of Aracaju. So the honest count of
orphan funds that pass the screen and survive research is zero.

---

## The asset class, which is the decisive finding

The cohort's R$118.2bn of carteira, by what the CVM's own segment table says it is:

| Segment | Amount |
|---|---|
| **Financeiro** | **R$83.87bn** |
| of which "Financeiro — Outros" (II.f.8) | R$81.60bn |
| Comercial | R$5.49bn |
| Industrial | R$3.79bn |
| Serviços | R$2.63bn |
| Consignado | R$2.17bn |

**The median business-to-business share across the whole cohort is 0.0%.** Only 81 of 531 classes carry the
paper the desk buys.

Seventy percent of the estate is financial-sector credit, and R$81.6bn of that sits in a single residual bucket
the CVM calls "Financeiro — Outros": not personal credit, not payroll-deducted, not corporate, not vehicles, not
property. It is a category the filing does not describe. Whatever it is, it is not multicedente commercial
duplicata paper, it has no heterogeneity to decompose into Premium, Claims and Residual strips, and there is no
named cedente behind it to build a recourse claim against.

That is the answer to the question as posed. **The orphan estates are, in the main, the wrong asset class
entirely.**

---

## The nine that are already on the list

Nine of the 36 funds in the target universe are orphan-lineage. They reached the list on merit, through the
ordinary screen, with no knowledge of their estate history:

| Fund | Lineage | Now administered by | Gestor | Carteira | Provision |
|---|---|---|---|---|---|
| Del Cred NP Multissetorial | Master | Limine Trust | Tercon | R$344m | 37.8% — **excluded as captive** |
| Prosper | Trustee | Actual | Libertas | R$41m | 48.7% |
| Módena NP | Sefer | Sefer | Positiva | R$36m | 115.1% |
| Trinu | Master | Qore | Catálise | R$24m | 444.3% — **excluded as captive** |
| Milagre | Trustee | Actual | Libertas | R$20m | 162.8% |
| AGA NP Multissetorial | Master | Limine Trust | Tueri | R$18m | 34.6% |
| SX Corporate | CBSF | Finvest | C20 Quadrante | R$17m | 37.2% |
| Santoforte | Trustee | Actual | Libertas | R$6m | 36.9% |
| Canada Invest Multissetorial | Master | Actual | Tueri | R$5m | 54.3% |

Four of the seven that survive are administered by **Actual Distribuidora** and three of those are managed by
**Libertas Asset**. That is a cluster the earlier analysis did not name, because it was hidden by exactly the
grouping error this query corrects: these funds no longer carry a lineage name anywhere in the current filing.

---

## What this changes about who to call

**Do not call the receivers.** There is no bulk trade in the estates. The paper is financial-sector credit, the
provisions are ordinary, and the handful of funds worth having have already surfaced through the normal screen.
A receiver conversation buys access to R$118bn of assets the desk cannot resell.

**Call Actual Distribuidora and Libertas Asset instead.** Actual has taken on 32 orphan classes and administers
four of the seven live targets on this list. Libertas manages three of them: Prosper at R$41m, Milagre at R$20m
and Santoforte at R$6m, R$67m of carteira across three vehicles with one decision-maker. That is the same
bundle logic as Ouro Preto and Tercon, and it is a manager who has demonstrably been absorbing distressed books
from failed houses, which is the exiting-strategy archetype from the other side.

**Watch Planner Corretora, but do not call yet.** Planner absorbed 61 orphan classes, more than anyone, and
appears repeatedly among the large distressed near-misses: Araguaia at R$782m with a 57% provision, Credifix at
R$479m with 350%, San Marino at R$221m with 632%, Agross at R$102m with 114%. Every one of them fails the
business-to-business test, and several are in the unclassified bucket below, so what they hold is unknown. If
any of it turns out to be commercial paper, Planner becomes the largest single conversation in the market.

---

## A loose end worth an hour

Twenty-eight classes in the cohort have a carteira the segment table does not classify at all, 22 of them above
R$20m. The largest are Aconcágua at R$2.37bn under Sefer, Laguz I at R$800m under Planner, Platinum at R$527m
and Laperanta at R$407m under Planner, and ARC DIP JS at R$515m under Daycoval. The informe reports a carteira
and reports nothing about what is in it.

These cannot be screened. They are the one part of the estate where the public data genuinely fails, and the
only way to know is the regulamento on Fundos.NET. Given that ARC DIP JS sits at Daycoval, where Sutphin already
has a relationship, that is the cheapest of the five to resolve.
