# The 18, and what they turned out to be

Answer to MGC, 11 September 2026. The screen's first run produced 18 names. This is what they are, what the
screen got wrong, and what a corrected screen produces instead.

Reproduce with `.venv/bin/python scripts/screen.py`. Cedente identities resolved through Minha Receita.

---

## The short version

Most of the 18 are not targets. The screen found funds with a high provision and commercial paper, which is not
the same thing as a broken multicedente book. What it mostly caught was captive originator funds: a single
company financing its own customers or its own suppliers, where a 30% provision is the expected loss of that
business, there is no heterogeneity to decompose, and the sponsor would never sell.

Two names have the shape the desk is actually looking for. A third cluster, which the screen was not built to
find, looks more valuable than either.

---

## The 18, by what they are

### Captive originator books. The sponsor is the cedente, and the sponsor is in the fund's name.

Resolving the named cedente CNPJs settled these. In each case the cedente is the company the fund is named after.

| Fund | PL | The cedente resolves to | Why it fails |
|---|---|---|---|
| Havan FIDC | R$3,676m | HAVAN S.A., the retailer | 100% varejo. Retail consumer credit, not duplicatas. Provision flat at 34.6% since 2023 |
| Mercado Crédito | R$3,064m | Mercado Crédito SCFI, Mercado Livre's lender | Captive fintech lending book |
| Mercado Crédito II Brasil | R$1,803m | same group | same |
| Mercado Crédito I Brasil | R$731m | Mercado Crédito SCFI, named directly | same |
| FIDC Agro Capital Finance | R$489m | ALBAUGH AGRO BRASIL, a pesticide maker | Captive supplier finance |
| Workcap Agro | R$443m | ALBAUGH AGRO BRASIL again, same CNPJ | Same sponsor, second vehicle |
| Opea Agro Sumitomo Chemical | R$190m | SUMITOMO CHEMICAL BRASIL | Captive, and it says so in the name |
| Katch Diversified | R$329m | BMP Sociedade de Crédito ao Microempreendedor | Captive microcredit lender |
| Grupo Casas Bahia FIDC | R$160m | not named, but the name is the sponsor | Single-obligor supply chain |
| HC Hidrocarbon NP | R$150m | not named | Fuel sector, gestor and administrador are the same house |
| Medsystems-style vehicles | — | — | Corporate name in the fund name |

Havan alone is R$3.7bn, and it was the largest name on the list. A retailer's own consumer book at a 34.6%
provision held flat for three years is a business model, not a distress event.

### Genuine multicedente books with the right shape

**PONTUAL BRASIL FIDC MULTISSETORIAL.** R$170m PL, R$170m carteira, provision 46.8% and up 17.2 points over
twelve months, 64% business-to-business paper. QI Corretora administers, Ouro Preto Gestão manages. Three named
cedentes, all unrelated industrials, and the mix is exactly the pathology the desk is built for:

- ALUMINUM BRASIL S.A., cable maker, capital of R$200,000 against the face it owes
- FURNAX COMERCIAL E IMPORTADORA, industrial machinery wholesaler
- DIOXYL REVESTIMENTOS QUIMICOS, paint maker, **in judicial recovery**

**DEL CRED NP FIDC MULTISSETORIAL.** R$357m PL, R$344m carteira, provision 37.8% and up 17.0 points, 65%
business-to-business. Limine Trust administers, Tercon Investimentos manages. No cedente above 10% of PL, which
for a fund named multissetorial is consistent with a genuinely diversified book.

These two are the answer to "what are the 18". Everything else is either captive, consumer, or too small.

### Also carrying cedentes in judicial recovery

Two more of the 18 have cedentes in RJ, which is where the Claims strip comes from, but both are small:

- **FS FIDC NP**, R$93m: cedentes are COMPANHIA BRASILEIRA DE ESTIRENO and CANGURU PLASTICOS, the latter in RJ.
- **TRINU**, R$179m PL but a carteira collapsed 80% to R$24m with a provision at 444%: cedentes are B. INVEST
  SECURITIZADORA, capital R$1m, and NUTRI AGROINDUSTRIA, in RJ. This one is genuinely broken and there is
  almost nothing left in it.

---

## What the screen got wrong, and the fixes now in the code

**1. "Comercial" in the CVM taxonomy includes retail consumer credit.** Segment II.c covers II.c.1 comercial
proper, II.c.2 varejo and II.c.3 arrendamento. 35% of the commercial face in the first result set was varejo.
Fix: compute the share from II.a industrial plus II.c.1 only, and exclude any fund with 10% or more varejo.

**2. A high provision is a level, and the desk needs an event.** Havan, Mercado Crédito and Katch have carried
25% to 50% provisions since the panel begins. Fix: require a rise of at least 10 percentage points over twelve
months. This alone drops the population that passes from 420 to 382 and removes the business-model cases.

**3. Captive books have to be excluded, and mostly cannot be seen.** Where cedentes are named, a single cedente
above 50% of PL is the tell. But naming is a reporting habit, not a property of the book: it runs from 0% of
classes at Trustee, Banvox and Merito to 95% at Catálise, and only 44% of the population names anyone at all.
Where the administrador names nobody, a captive book is invisible and only the fund's name gives it away.
Business case 2.1 says cedentes are "usually empty in a genuine multicedente book". Empty is common, but
emptiness is driven by who administers the fund, not by what is in it. Treat any survivor with a corporate name
in its title as captive until a human says otherwise.

With all three corrections the screen returns 5 names instead of 18, and surfaces one the original missed
(Medsystems B24 II). Of those 5, two are captive by name, one is single-obligor, and the two that survive are
Del Cred and Pontual.

---

## The finding worth more than the list

Broken multicedente books cluster by gestora, and the cluster is worth more than any single fund.

35 classes pass every quality gate. Only 5 clear the R$60m carteira floor. But they are not spread evenly:

| Gestora | Broken books | Combined carteira | The anchor |
|---|---|---|---|
| Tercon Investimentos | 5 | R$378m | Del Cred NP Multissetorial, R$344m |
| Ouro Preto Gestão | 3 | R$207m | Pontual Brasil Multissetorial, R$170m |
| Kanastra | 2 | R$99m | Medsystems B24 II |
| Libertas Asset | 2 | R$60m | Prosper, R$41m |
| Tueri Gestora | 2 | R$24m | AGA Multissetorial |

By administrador the concentration is the same: Limine Trust has 6 of the 35, BTG has 7, Actual has 3.

One conversation with Tercon reaches R$378m of broken business-to-business face across five vehicles. One with
Ouro Preto reaches R$207m across three. That changes the approach in two ways.

It solves the size problem. No single vehicle at Ouro Preto clears R$60m except Pontual, but the three together
are R$207m. If the desk can buy across vehicles from one decision-maker, the floor binds on the bundle rather
than on the fund, and the business case's own economics say the floor is what caps deal count.

And it is the best willingness signature available. A gestora holding several broken books of the same kind is
archetype G, the gestora exiting a strategy, which the business case calls the cleanest single signature and
the highest willingness in the table. It has one decision to make across five vehicles rather than five separate
fiduciary conversations.

---

## Where this leaves the supply count

The count of 18 was right arithmetically and wrong commercially. The honest numbers:

| Measure | Count |
|---|---|
| FIDC classes filing at 2026-07 | 4,321 |
| Provision at or above 25% of carteira | 420 |
| Right paper, business-to-business, no material retail | 91 |
| Provision is an event, not a level | 67 |
| Not visibly captive | 36 |
| Carteira at or above R$60m | 5 |
| Survive the name test for captive | 2 |
| Gestora clusters worth a single conversation | 5 |

Two single vehicles and five gestora clusters, against a business case that needs six to ten trades. That is
tight but not empty, and the cluster route is the one that has room in it.

The filter still missing is the one that matters most. Redemption suspension, the art. 44 §3 trigger, is the
best willingness proxy in the design and needs Fundos.NET. Until it is built, this is a research list and not a
calling list.
