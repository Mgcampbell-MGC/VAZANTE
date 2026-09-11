# VAZANTE
VAZANTE Falling Funds in Brazil 

VAZANTE
The business case, final.
A finite principal desk that buys whole broken FIDC carteiras for one cash price and resells them in three pieces under pre-locked buyer commitments.


Sutphin Ltd. — MGC / GC — São Paulo — 10 September 2026 — confidential
Status: final. Supersedes the 8 September rebuild and the compiled "02 VAZANTE" working document wherever they conflict. Where this document and the compiled document disagree, the number here is the one that was computed and checked; Part 0 lists every disagreement.
Built from six independent work-streams run 10 September 2026: P1 pre-exclusivity intelligence, P2 supply, P3 legal and tax, P4 buyer package, P5 economics (P5_model.py, 2,500 Monte-Carlo paths per scenario), P6 red team. Every load-bearing figure carries one of five tags: VERIFIED (primary source fetched), MODEL (an output of the arithmetic), ASSUMPTION (a parameter we set), GATED (cannot be settled from a desk; the condition that settles it is named), DECISION (a choice, not a finding).

How to read this in twenty minutes. Part 0 (four pages) is what the audit changed and why; read it before anything else, because it corrects the arithmetic that the rest of the compiled document was built on. Part 1 is the business in one page. Part 9 is the decision and the dated conditions. Everything in between is the evidence, section by section, in the order a hostile reader would attack it.
What is in the companion document. The buyer outreach package — the calibration pack in Portuguese, the three standing buy boxes, the openers and the Deal 0 protocol — is delivered separately as "VAZANTE — Pacote de Compradores" so that GC can send pages from it without sending this.


Contents

1.  The business in one page — What VAZANTE is, in MGC's words, corrected
2.  Before the fund gives us anything — The pre-exclusivity answer: what is knowable from outside, how, and what it is worth
3.  Supply — who can sell, and the honest count — Seven seller archetypes, the willingness problem, ≈14 executable situations now, 6–10 trades
4.  The Oracle and the three exits — Five dimensions, the forensic bridge, routing into Premium / Claims / Residual
5.  The buyers and the standing boxes — The map, the first three calls, what counts as a yes
6.  Entity, tax, title, warranties, settlement — The Ltda and the captive FIDC-NP; the receita bruta question; the closing sequence
7.  Economics as the model computes them — One trade, the size floor, the cost base, capital, the 48-month campaign
8.  Red team, condensed — Sixteen attacks and their verdicts; the five numbers most likely to be wrong
9.  The decision — GO WITH CONDITIONS — five dated gates, Deal 0 and a tiny Deal 1 in parallel, the first 120 days
A.  Appendices — The one-page tax consulta; the Day-1 sheet; the verification register


Part 1 — The business in one page
VAZANTE is a finite-life, capital-light, principal credit trading desk. It finds broken Brazilian FIDCs from public CVM data, uses the Oracle to establish what is really there on five separate dimensions, buys the whole carteira at one cash price with the carve kept private, and resells it into three exits under buyer commitments locked before the seller ever hears a number. It never quotes a firm price to a seller until firm onward exits cover the all-in basis, tax included, by 1.20×. It settles all legs on the same day through one bank instruction, all-or-none. It runs six to ten trades over 24–36 months and then stops, because the paper it needs — legacy unregistered duplicatas inside orphaned funds — stops being made in January 2028 and the liquidation wave normalises.
The edge is three things and not a fourth. Detection: the machine reads every FIDC informe every month and ranks the broken ones before anyone is told they are broken. Speed: a pre-exclusivity pack in 3.5–5 hours, a Day-1 indicative range, an exclusivity window of 7–10 business days, cash on day 8. Access: both sides take GC's call — the sellers because we are buying an asset and asking for no fee, mandate or report; the buyers because Prisma has already paid Sutphin for deals and the others have standing boxes. It is not structuring, servicing, fund management or advice. VAZANTE renders no service to anyone; it buys and sells.
Element
What it is
Seller
Whoever holds the pen on a carteira whose loss is already booked or whose signer has no NAV to protect: a provisioned bank, a fund in liquidação, a substitute administrador after the first write-down, a senior cotista who took the paper in kind, a gestora exiting, a patrimônio separado with insufficiency declared.
Asset
Whole carteira, R$60m+ documented face (≈R$85–100m informe), multicedente commercial duplicata / NF-e paper, Master/Reag lineage (lastro gap 25–60%) — the book nobody else can read in ten days.
Price to seller
One cash number for everything. Never a parcel. Never more than ~73¢ per R$1 of FIRM onward proceeds (72¢ if characterised as factoring, 80¢ inside a FIDC wrapper).
The carve
Private. Premium (a-vencer / <30dpd, sacado-confirmed cash, title clean) → performing-receivables gestoras at 25–75¢. Claims (evidenced recourse, solvent cedente or bound sócios) → Prisma and peers at ~12¢, unconditional and same-day only. Residual (everything that meets a standing box) → one backstop at a grid, 1.5–4¢. Zero: NV / no lastro / fails every box.
Settlement
Buyers fund T−2 into escrow; seller paid at T 10:30 only after the escrow agent certifies all buyer funds; VAZANTE paid at 11:30. No leg releases unless the prior one is certified. Partial closings are forbidden in the instruction itself.
Entity
A Ltda drafted to survive the factoring characterisation for deals 1–3; a captive FIDC-NP with a partner gestora from deal 4 if the tax gate clears (it moves the biddable price by ≈R$1m per reference deal).
Capital
R$3.0m at risk (fixed stack, dead exclusives, warranty tail, tax paid in good years) plus a R$5m committed settlement line from deal 3–5, never from an exit buyer. Third-party capital where needed; Sutphin takes the residual….GC MIGHT NOT BE NEED MIGHT E BETTER WAY TO DO THIS instead of a bridge 
Economics
Locked after-tax contribution = L ÷ 6 per trade by construction; R$2.3m on the reference book. Base campaign ≈6 closes, R$18.4m pre-tax, R$10.9m after tax over 48 months; R$28k locked profit per partner-day.
Kill conditions
Cannot establish transferable title to enough value. Firm exits below 1.20× tax-inside basis. Locked after-tax contribution below R$1.5m (R$2.0m from deal 6, R$2.5m from deal 10). A material unresolved fact that could exceed the locked contribution. Any one fires: no bid.
What VAZANTE never does
Bid on a parcel. Quote before three FIRM exits exist. Finance a book. Take a fee. Say the word "laudo" to a seller. Sell a strip to a fomento mercantil vehicle. Enter a competitive process ("if a book has an advisor and a deadline, don't bid"). Let one counterparty be both funder and exit.


The one sentence for GC. "We buy your whole carteira, cash, one price, in ten business days — no report, no fee, no mandate" — GC the seller  never see how we cut it up and break down the brick.

Part 2 — Before the fund gives us anything
MGC's question was direct: how do we get information on a fund before the fund gives us information? The answer is that most of what prices a broken FIDC is already public, monthly, free, and nobody reads it in combination. This part sets out what is knowable from outside, source by source; what is not, plainly; the method that turns the public record into a Day-1 range GC can say out loud; what that range is worth; and the two-page sheet he carries into the first call. It is the operational core of Detection and Speed, and it is the reason the exclusivity ask is credible: we arrive already knowing what broke, when, and roughly what it is worth.
2.1 What is public, and what each source is good for
Every FIDC files an Informe Mensal with the CVM, and the CVM publishes the whole population as open data, monthly, with history to 2013 and a weekly refresh (VERIFIED, dataset present and updated 7 Sep 2026; bulk download blocked from this sandbox, not from a Brazilian desk). Its structure under Res. CVM 175 Suplemento G is the pre-exclusivity engine. The compiled document's tab mapping was wrong and would have broken the most important query; the correct map, and the second finding that changes the pack design, are below.
Informe table
What it actually holds (VERIFIED)
What it tells us before exclusivity
Tabela I — Ativo
Carteira, PDD; items a.11 / b.11 name a cedente only above 10% of PL
The coverage gap. Cedentes: usually empty in a genuine multicedente book
Tabela II — Carteira por segmento
Industrial / comercial / serviços / consignado / cartão…
Whether the book is the paper we want (≥60% industrial + comercial)
Tabelas V / VI — Comportamento da carteira
The ageing ladder, com / sem aquisição substancial; a vencer, inadimplentes por faixa, pagos antecipadamente
Migration, the 180+ bucket, pré-pagamento — the C dimension at fund level
Tabela VII — Negócios no mês
Aquisições, alienações, substituições, recompras, Valor vs Valor Contábil
The recompra pathology: who has been paying instead of the debtors
Tabela VIII — 25 maiores sacados
CPF/CNPJ, R$, % PL — every month, every fund
The D dimension, named, with face. Typically 20–35% of face directly evidenced
Tabela IX — Taxas praticadas
Discount rates
Whether the pricing was ever real
Tabela X — Outras informações
Cotas/subclasses, rentabilidade, resgates, RESG_SOLIC, liquidez
The quota-return tell; unpaid redemptions


Around the informe sit the other public layers, each with a different lag and a different reliability: the cadastral register (cad_fi, daily, official — administrador, gestor, custodiante, auditor, diretor responsável and every change to them); Fundos.NET (regulamento, demonstrações contábeis with the auditor's parecer, atas, convocações, fatos relevantes, lâmina — the lâmina names the top-5 devedores and coobrigados by name); rating agency reports where they exist (independent, 12–30 months stale, but they name counterparties and publish vintage loss curves); Receita Federal via Minha Receita (situação cadastral, capital social, QSA, address, per CNPJ); CENPROT protest (values, but blind at cartório level in São Paulo); DJEN publications (free, by party name) and the paid court aggregators (per CNPJ); BCB regimes especiais (weekly OData) and liquidation editais; and the registradoras, which as a non-participant give a paid, limited certidão in five business days and as an opted-in participant give position-level truth in hours — post-exclusivity only.
The finding that redesigns the pack. The informe names sacados generously and cedentes almost never. So the D dimension (is the debtor real, alive, solvent, unprotested, not in RJ?) runs beautifully from public data on 25 named counterparties with face. The R dimension (is there recourse, against whom, and is that party collectable?) does not run off the informe at all for a multicedente fund and has to be reconstructed from five other routes: the lâmina's named coobrigados; the regulamento's cedente eligibility and coobrigação clauses; the rating report; the fund's own litigation searched by fund name; and the DFs' related-party notes. Where the cedentes cannot be named, R collapses to the fund-level com/sem-aquisição-substancial split and the clause — and the Claims strip cannot be priced from outside.

2.2 What cannot be known from outside — plainly
Fact
Why it waits for exclusivity
Position-level existence
No public source is position-level. Tabela VIII is a 25-row aggregate by counterparty.
NF-e XML / digVal
Consultation by chave de acesso needs the chave, which is in the seller's tape.
CNAB payer identity
Bank files. The single most decisive evidence on C — who actually sent the money — is entirely seller-side.
Registry title
Non-participants get a limited certidão in five days; the opt-in executed in VAZANTE's CNPJ is the real route and needs the seller's instruction.
The assignment contracts
The regulamento says what the termos de cessão should say. Only the contracts say what they do say — and undisclosed side agreements are, by the design's own warranty list, invisible until disclosed.
Sacado confirmations
Need the seller's authority or the fund's identity; doing it without either is commercially reckless.


Scored dimension by dimension on outside-only evidence: D substantially (this is where the band narrows); R substantially if the cedentes can be named, otherwise barely; C partially — enough to establish that the cedente has been paying instead of the debtors, not which positions; E barely; T barely. The two dimensions that determine whether the asset exists and whether we can own it are the two that outside evidence cannot reach, and they jointly drive roughly half the width of any Day-1 range. The Day-1 range therefore cannot honestly be tighter than about 1.5× top to bottom, and that floor holds only when the top-counterparty run has been done. Say the corollary on the call: the width is what verification is for. That sentence is the reason for the exclusivity ask, and it is true.
2.3 The method: from informe face to a number GC can say
Five steps, run backwards from the 1.20× rule. Step A, informe face to ledger face: the reconciliation residual across tabelas and across months (0.88–0.98). Step B, ledger face to documented face: the lastro-gap prior by lineage tier — 3–15% for a healthy orphan, 25–60% for the Master/Reag lineage — which is judgement wearing a number's clothes, rests on n = 1 reference book, and contributes ~44% of the band width; print the n on the pack. Step C, the E/T/C/D/R state mix from the public signals. Step D, map to the three exits at standing grids. Step E, divide by 1.20 with tax inside the basis, subtract costs, and that is the maximum seller price under each of three scenarios. The Day-8 firm bid is then computed from scratch off contracted buyer prices; the Day-1 number is never an input to it.
Worked on the reference book — what we know at 09:00 on Day 0, no seller file touched
Informe face R$210m; PL ≈ R$185m; Master/Reag lineage; administrator in liquidação; recompra intensity in the top decile for 14 consecutive months and then a stop; ageing ladder migrating; PDD coverage of 90+ paper at 0.4; senior quota return variance near zero for 19 months; Tabela VIII top-25 at ~31% of PL.
Scenario
Documented face
Onward estimate
Max seller price, no counterparty run
Max seller price, with the run
Pessimistic
R$105m
R$5.8m / R$8.1m
R$4.0m
R$6.0m
Central
R$136.5m
R$10.2m / R$11.5m
R$7.7m
R$8.8m
Optimistic
R$163.8m
R$15.6m / R$15.8m
R$12.2m
R$12.4m
Realised, Day 8 (pricing engine)
R$150m
R$11.7m
R$9.0m
R$9.0m


Without the run the Day-1 quote is "R$4–8m, whole portfolio, cash, subject to verification" — a 1.9× band whose top sits 14% below the eventually-computed maximum, which is the right direction (a seller never objects to being raised). With the run — the 25 named sacados resolved through Receita, CENPROT and the courts, ninety queries, about R$100 and forty minutes — the named top-10 carry R$52m of face (25% of informe face) and price at 11.1¢ with a ±20% band against ±60% on everything unnamed, and the quote becomes "R$6–8.5m": the floor rises 48%, the band tightens from 1.92× to 1.47×, and the top sits 2% below the realised maximum. That is the difference between a number a seller dismisses and a number that gets exclusivity. (P1 §2.6, §4; all pricing MODEL, carried from the audited engine; the counterparty pricing is a hypothetical top-10 until the first real pack.)
Band-widening rules, applied without discussion: informe dark for two months or more → widen ~2× and drop the floor 30%; no current rating and no clean audit → full lineage band; a current rating report → contract by a third; an auditor ressalva on lastro → shift documented face to the bottom third of the band, do not widen; closing likely to slip twelve months (authority contested, no assembly convened, liquidante not appointed) → −34% on value, and it belongs in the range, not in a footnote.
2.4 Reading the break: the 24-month reconstruction
Every single indicator has an innocent explanation — high recompras alone is a healthy revolving fund exercising substitution rights; a flat senior return alone is a CDI-plus target with adequate subordination; a coverage gap alone is a disclosed PDD methodology. The conjunction has no innocent explanation. BREAK-FLAG fires when at least three of four primary conditions hold in the same month for two consecutive months: (A) recompra intensity above 3% of carteira per month or twice the fund's own trailing-12 median; (B) churn-to-default migration below 0.35; (C) PDD ÷ 90+ vencidos below 0.60; (D) senior quota 12-month return standard deviation below 0.15% while the 180+ bucket grew more than 50%. Nine secondary signals confirm and never trigger alone (alienações ao cedente exceeding alienações a terceiros; recompra Valor ≈ Valor Contábil ten months in twelve; pré-pagamento above 15% of liquidations; RESG_SOLIC outstanding two months; late, restated or omitted informe; counterparty changes; top-25 churn outside 20–70%; auditor ressalva). Thresholds are ASSUMPTION and must be fitted on the labelled set — Master, Reag, Trustee, Banvox lineage funds whose break dates are now known from the BCB decrees. That labelled set is free, already ours, and the single highest-value calibration exercise available; build it before the first live pack (GATED).
Two dates fall out of the series and the second matters more: t_peak, the month of maximum recompra, when the cedente was still solvent and still hiding; and t_stop, when recompra intensity falls below a quarter of its trailing peak and stays there — the cedente did not choose to stop, it ran out of money. They partition the book into three vintages that route to three exits: V1 pre-break residue (the honest tail → Residual), V2 the churn zone between the two dates (the most suspect paper in the fund, price at zero until evidenced), V3 post-break (the true default cohort, never cleaned, but the cohort where the recourse claim is cleanest → Claims). The specific Day-1 check: on the reference book the freshest substituted paper, S1, is 5.3% of face and 44.8% of the block bid. If S1 sits in V3 the central scenario holds; if it sits in V2, move to the pessimistic scenario regardless of everything else, because the strip carrying half the bid sits in the vintage with the highest existence risk. This is the red team's adverse-selection warning turned into a rule that runs from public data before anyone quotes.
2.5 What it costs and how long it takes
Stage
Machine
Human
Note
Bulk layer (24 months × ~4,200 funds; cad_fi daily)
resident
0
Cron. Zero marginal time per deal.
History reconstruction, indicators, conjunction rule
< 2 min
0
Pure computation on resident data.
FNET pull: regulamento, last 2 DFs + pareceres, 12 months of atas / fatos relevantes, lâmina
~15 min
45–90 min
Reading the disposal-authority and coobrigação clauses and the auditor's notes. Not automatable, not skippable.
Rating sweep (6 agencies)
~5 min
15 min


Counterparty run: 25 sacados + named cedentes ≈ 30 names × Receita + protest + court
10–20 min
30–45 min
Adjudicating ambiguous names and the relatedness graph.
Grid application, three scenarios, 1.20× backwards
< 1 min
15 min
Human sets the lineage tier and signs the band.
Two-page write-up
—
30 min


Total
~45 min
2.5–3.5 h
Flagged 09:00 → pack on GC's desk by 16:00, same day. Marginal cost R$90–150.


Against a R$1.5m minimum contribution the cost of the pack is not a decision variable; even at ten times the figure it rounds to zero. The binding constraint is analyst attention on the regulamento and the auditor's notes, so the machine must rank, not merely score: a weekly top-20, with full packs built only for the three to five GC can actually call that week. And kill condition three is checkable from informe face alone on Day 0 — below roughly R$85–100m of informe face, do not build a pack.
2.6 The two-page sheet GC carries into the Day-1 call
Page 1 is what he says; page 2 is what he says it from. The full eighteen fields are in Appendix B. The three that buy exclusivity are on page 1, field 8 — the three sentences that prove we have read the fund: the recompra fact with dates ("your repurchases ran at N% of the carteira for fourteen months and stopped in March"); the sacado fact with a name ("four of your twenty-five largest sacados, holding R$X, are baixada, inapta, falida or in RJ; two more share an address and R$11,000 of combined capital"); the quota fact ("your senior class has returned CDI + N% to eight decimals for nineteen months while your 180-plus bucket tripled"). Then the indicative range with its cents on informe face, the exclusivity ask (7–10 business days), the three things needed on day 1 of exclusivity named now so there is no negotiation later — the position-level tape with CNPJ do sacado and CNPJ do cedente per line, the termos de cessão and aval/coobrigação schedules, and the registradora opt-in executed in VAZANTE's CNPJ plus the custodiante's last art. 38 verification report — and field 9, what we do not need: no report, no fee, no mandate, no ninety-day engagement. He is selling us an asset.
Two governance rules protect the channel. The Day-1 range is never revised downward after exclusivity except on a named, evidenced, documented fact — "the tape was worse than we thought" is not a fact; "eleven of the twenty-five largest sacados have no NF-e matching the assigned duplicata" is. And every Day-1 range, every Day-8 firm bid and the ratio between them is logged; indicative-to-firm is a standing KPI with a target band of 0.85–1.15. Drift below means the priors are too generous; drift above means we are losing deals we should have won.
2.7 Where the method is weak
Twelve weaknesses are named in P1 §7; the six that matter most, in the order a hostile reader would raise them. The lastro-gap prior is n = 1 and drives 44% of the width. Nothing on Day 1 is FIRM — the range is built on GRID and ESTIMATE inputs, legitimate for an indicative and nothing else. The informe is a seller-side fact: cross-tabela and cross-time reconciliation catch clerical error and crude fabrication, not a competent administrator who has decided to lie consistently for two years, and that administrator exists in this population. A live sacado does not make a real receivable — a solvent debtor with fabricated paper is indistinguishable from a solvent debtor with real paper from outside, which is exactly why E and T score "barely". CENPROT is blind in São Paulo, where most of these counterparties are (GATED: test twenty known-protested SP CNPJs before relying on the protest column). And the funds we most want — the ones that have gone dark — are the ones the method prices worst: the last filed informe is the only anchor and the band roughly doubles. The honest response to that is a wider band said out loud, not a narrower one and hope.

Part 3 — Supply: who can sell, and the honest count
The fee model died on the seller side: a liquidante who could not lawfully contract a success fee, an administrador who had no upside, seventy percent dead work. The principal model inverts the counterparty problem — a liquidante who cannot contract a fee can sell an asset — and P2 tested whether that inversion produces sellers in numbers. It does, but the count is smaller than the compiled document assumes, the floor is higher, and the filter that decides everything is not authority but willingness.
3.1 Authority: two signatures, no assembly
Res. CVM 175 Anexo II art. 70 lists the assembly's exclusive competences exhaustively: accounts, substitution of an essential service provider, new closed-class issuance, merger / spin / transformation / liquidação, regulation amendment, the negative-PL plan, the insolvency petition. Alienação of the carteira is not on the list. Art. 84 gives the gestor "poderes para praticar os atos necessários à gestão da carteira" and art. 86 the competence to "negociar os ativos da carteira, bem como firmar todo e qualquer contrato ou documento relativo à negociação de ativos"; a real regulamento confirms the administrador may, on the gestor's instruction, "celebrar qualquer ato de alienação ou transferência relacionado aos Direitos Creditórios" (VERIFIED). Assembly cover is legally unnecessary and commercially requested in perhaps 45% of cases where the sale is substantially the whole carteira at a deep discount; it is unavoidable for a securitizadora's patrimônio separado (Lei 14.430 art. 30) and it adds 4–5 weeks. A BCB massa liquidanda selling its own book needs prior BCB authorisation (Lei 6.024 art. 16) and is very slow. Everything else is two signatures.
3.2 Willingness: the accounting test that decides who sells
ICVM 489 art. 11 recognises a provision "sempre que houver evidência de redução no valor recuperável". The recompra pathology — the cedente repurchasing defaulting paper at face so that no default ever ages — is precisely the mechanism that suppresses that evidence, so a fund kept clean by recompra carries its carteira at or near face. Selling it at 6–9¢ crystallises an 85–94% write-down in one informe, on one date, attributable to one named diretor responsável. The adverse selection is built into the origination signal: the funds the machine finds best are the funds whose signatories can least afford to sell. The operating rule that follows is the whole supply strategy in one line:
Sell to us only if the loss is already booked, or if the signer has no NAV to protect. Everything else is a conversation about why the seller should destroy his own mark — and that conversation is lost before it starts.
That reduces the supply to a short list: a bank that has provisioned (BRB has booked R$2.6bn against Tirreno paper at the BCB's written instruction, VERIFIED); a fund already in fund-level liquidação; a patrimônio separado already impaired; a cotista who has taken the paper in kind and now owns it on balance sheet; a gestora exiting a strategy; and a substitute administrador in 2027–28 who will not own the first write-down. And it names the lever nobody else is pulling: the default liquidation path under art. 44 §3 IV is dação em pagamento, not sale. Once a senior cotista holds the paper in kind he is a principal with a marked asset and no fiduciary to protect — so the pitch to the bank or insurer holding the senior class is not "sell us the fund's carteira", it is "take it in kind; we bid on your asset." That manufactures a principal seller out of a fiduciary one. It is unproven (GATED), and every point of improvement in the willingness pass rate is worth more than any improvement in origination volume.
3.3 Seven seller archetypes
#
Archetype
Who signs / authority
Willingness
Count over 36 months
A
FIDC under a substitute administrador after the original was liquidated
Gestor (art. 86) + substitute administrador; assembly only for the substitution
Poor now, good 2027–28: the receiver will not own the first write-down
Largest pool (Trustee 63, Reag 110, Master 53 funds)
B
FIDC in fund-level liquidação
Administrador on gestor instruction
Good — but the default path is dação em pagamento, not sale
12–25 standing; few convert to sales
C
BCB massa liquidanda selling its own book
Liquidante + prior BCB authorisation
Maximal; regulator-constrained; very slow
2–5
D
Senior cotista block
Cannot order a sale; can substitute the gestor, resolve liquidação, or take in kind
Bank / insurer high; feeder FIC lowest
An access route, not a count
E
Bank / IF holding acquired paper on its own balance sheet, provisioned
The institution; one signature; no CVM perimeter
Best in market
3–8
F
Securitizadora, patrimônio separado with insufficiency declared
Assembleia de titulares + agente fiduciário (Lei 14.430 art. 30)
High where declared; slow (30–60 days)
3–6
G
Gestora exiting / the in-kind holder
Cleanest single signature
Highest, by construction
2–5, plus the manufactured route



3.4 The count
Central case: ≈14 executable FIDC situations standing today (plausible range 9–19 until the one bulk query that converts it from ASSUMPTION to VERIFIED is run — join twelve informes to cad_fi ADMIN, filter to the Trustee / Banvox / Reag / CBSF / Master administrators, bucket by segment share, PL, PDD share and recompra share; an afternoon's work from a Brazilian desk). With maturation of the A-cohort and new orphan flow: 25–32 over 24 months, 39–47 over 36, including the non-FIDC archetypes. At the R$100m documented floor that supports a R$3m-per-trade band, about 20 over 36 months. So: comfortably more than ten; not sixty — sixty would need every willingness, authority and perimeter pass rate to be wrong in the same direction.
Executable situations are not trades. At 60% exclusivity-on-approach and 40% close-on-exclusivity, ten trades consume about 42 serious approaches and twenty consume 83, against a universe of about forty over three years; and a failed approach permanently burns the counterparty about a quarter of the time. The campaign consumes more than half its own universe to reach ten trades. That is why "never enter a competitive process" is an economic rule and not a preference: a lost auction burns a counterparty and returns nothing.
3.5 Named live situations, ranked by executability
#
Situation
Archetype
Authority × willingness
Verdict
1
BRB / Tirreno Master book — R$12.2bn acquired; R$2.6bn provision ordered by BCB 7 Jan 2026; Quadra block sale expired 6 Jul 2026; BRB selling directly, R$370m of CCBs placed piecemeal 28 Aug
E
Best in the market on both
Worst perimeter: BCB found "insubsistência dos ativos", referred to MPF, ~R$1.2bn blocked in court. If a name must be picked today it is a defined tranche with a 25–35% title/existence holdback released on the Oracle's findings at 90 days — never the book; and it will be a competitive process, which halves the contribution.
2
A multicedente duplicata FIDC whose class has been closed for redemptions > 5 business days and whose art. 44 §3 assembly is convened — a shape, not a name
B / D
Gestor + administrador; assembly already convened for other reasons, so cover is free
The correct Deal 1 shape. The suspension is the admission. Found by the five-filter screen in 3.6, not by reading the press. No public name satisfies it cleanly today.
3
Trustee / Banvox estate — 63 FIDCs, R$14.1bn, liquidated 3 Sep 2026; receivers unpublished
A
Good in law, blocked until a receiver exists
Largest single pool; not a 2026 seller. Instrument the weekly cad_fi ADMIN diff now; approach in 2027.
4
Reag Trust successors — 110 FIDCs, liquidated 15 Jan 2026; orphaned once, some twice
A
Better than #3: twenty months elapsed, an audited cycle under a successor's name
Highest-priority A-cohort. Successors already named in cad_fi; a pull, not a diff.
5
Master / Banco Master FIDCs — 53 funds, 52 "à deriva", R$3.1bn; none had convened the substitution assembly
A, degraded
No valid administrador signature exists
Excluded as unsignable. Converts only through the cotista channel: force convocation at ≥ 5% and put resgate em ativos on the agenda.
6
The 46 dark FIDCs across 12 administrators — non-filers in July 2026
A, degraded
Same failure as #5
The best free lead source in the market and the worst signature. Use it to find #2, not to sell to.
7
Casas Bahia's 12 linked FIDCs — R$3.95bn PL; IBCB-AF01 alone R$1.085bn; stay to 15 Feb 2027
D / B
Court-blessed route available
Wrong shape. Single-obligor risco sacado has no heterogeneity to decompose. Prisma buys the claim directly and does not need us.
8
Electra Energia complex — RJ filed 27 May 2026, Curitiba; JIF II FIDC R$494m; SIGA funds R$184m, within Sutphin's Daycoval reach
D / B
Daycoval takes the call
Best access, wrong shape — single-obligor. One call to test the relationship, not to trade.
9
Fictor Invest FIDC — R$272m; Apex renúncia 19 Feb 2026; assembleia 9 Mar 2026 with a liquidation proposal; accounts found "praticamente zerados"
B
High in form
Perimeter failure; cotistas inherit the litigation. Excellent Deal 0, unbuyable Deal 1.
10
A defaulted CRA series where the agente fiduciário puts a lastro sale to the titulares (Lei 14.430 art. 30)
F
Best-written statute
Cleanest law, slowest clock. Start one now so it lands in year two.


The honest position is that no publicly identifiable situation today satisfies authority, willingness, shape and perimeter simultaneously. That is not a research gap; it is the finding. The situations that pass all four are, by construction, ones nobody has written about — a fund whose class quietly closed for redemptions, whose gestor is still in place, whose senior cotista is a provisioned bank, and whose carteira is multicedente duplicata paper. The funnel says roughly fourteen of them exist. Deal 1 should be a fund nobody has heard of.
3.6 The screen that finds Deal 1
Five filters over two public datasets, not yet run because bulk download is blocked from the sandbox; it is the first query to run from a Brazilian desk: (i) class closed for redemptions more than five business days — the art. 44 §3 trigger, disclosed on Fundos.NET as a fato relevante or comunicado; and (ii) PDD ≥ 25% of carteira in the latest informe — the loss is already booked; and (iii) ≥ 60% of carteira in industrial / comercial direitos creditórios; and (iv) PL ≥ R$85m (the R$50m documented floor at a 0.58 ratio; raise to R$100m for the preferred band); and (v) gestor CNPJ still active and distinct from the administrador. What comes out is the calling list, ranked by the conjunction rule. Everything in Part 2 is then built for the top three to five.
3.7 Competition: sell to them, do not bid against them
JiveMauá deployed R$1.8bn across 20–25 transactions in fifteen months — 1.3–1.7 deals a month at R$72–90m average, single names, case by case (VERIFIED, NeoFeed 24 Jun 2026). Grupo IOX runs a R$350m NPL FIDC and says deal flow is up 50% or more and "não tem 20 players bons nesse mercado". Recovery (Itaú) holds 25–30% share but is 95% consumer. Möbius has R$1bn targeting CDI+17. None of them reads a multicedente duplicata book in ten days, and all of them are exits, not rivals, for the pieces. The question "can a two-person desk with a machine win a book against JiveMauá?" has a precise answer: not in a process, and it should never try — a competitive process halves the contribution and a lost one burns the counterparty. The desk wins books nobody else can read, uncontested, and sells the pieces to the people who would have been its competitors.
3.8 Cadence: what a two-partner desk can actually close
Phase
Fast lane
With assembly cover
Note
Detection → contact → indicative → exclusivity granted
2 weeks
2 weeks


Exclusivity window (tape, verification, three FIRM prices, max bid, firm bid)
2 weeks
2 weeks
The design's 7–10 business days, treated as unachievable on deals 1–3
Documents
1 week
1 week


Assembly cover (edital, quorum, deliberation)
—
4–5 weeks
≈45% of attempts (ASSUMPTION)
Closing, matched settlement, onward transfers, post-close
2 weeks
2 weeks


Per attempt
7 weeks
12 weeks
Blended 9.2 weeks


Concurrency is one live deal in year one, 1.8 in year two, 2.0 in year three — matched settlement needs both partners through the window and the closing. Win rate from exclusivity to close 35% in year one and 42% thereafter, deliberately low because the four kill conditions are absolute; a desk that closes 70% of its exclusivities is not applying them. Result: 1.4 closes in year one, 5.2 cumulative by month 24, 9.5 by month 36. Ten is reached around month 30–34. Twenty needs a third executor and lands around month 48. Thirty is not reachable in 36 months on any parameter set tested. The third slot is worth about three additional closes over 36 months — R$6–9m of locked contribution — and it is the clearest hiring decision in the plan: after deal 3, not before deal 1.
Where it stalls, in order: willingness (step five of the funnel removes 70% of the pool); the assembly clock (about one close a year; mitigate by putting the sale authority on an assembly that is already being convened for substitution or liquidation, so the marginal delay is zero); the buyer side (three FIRM prices inside a five-day sub-window from specialists running 1.4 deals a month each is only arithmetically possible with standing grids — they are not a nice-to-have, they are the timeline); concurrency; counterparty consumption; and the clock nobody controls — duplicata escritural full regime January 2028, liquidations normalising to 2–4 a year from 2028. The window is H2 2026 to 2028 and it closes on its own schedule. Front-load the campaign and let the hurdle rise as designed.

Part 4 — The Oracle and the three exits
The Oracle is the verification engine inside Codex. It is not a fraud detector, and the design is explicit about the trap: a fantastic machine that proves a bad book is bad is not monetisable. Every check it runs has to answer one question — does knowing this change our purchase price or an onward buyer's price? — and the product is not a grade, it is a sentence: here is exactly which reais of this book we can prove sufficiently for buyer X to pay Y. The money is in finding the good assets hiding inside the bad wrapper; the fraud is usually just the reason the opportunity exists.
4.1 Five dimensions, never one grade
Dim.
Question
Best evidence (truth hierarchy, top down)
Economic consequence of a miss
E existence
Does this invoice / title exist as a fiscal document at this value?
NF-e XML from the custodian, its infNFe hashed and matched to SEFAZ's digVal — binds this document to this value. A DANFE proves nothing; canonicalisation mismatches (~2%) are adjudicated by a human.
Position goes to zero. On a Master-lineage book 25–60% of face fails here.
T title
Does the seller own the right, exclusively, and can he transfer it?
Registradora consulta de duplicidade in VAZANTE's own name; executed termo de cessão with the art. 288 form; custodian release. No registry hit ≠ fake; valid NF-e ≠ seller owns the right.
The most valuable and least testable dimension; the one the Oracle concedes it cannot fully test pre-exclusivity. A competing assignment converts a Premium position to zero after the money has moved.
C cash
Who actually sent the money over 24 months?
CNAB return files, payer identified by raiz-8 CNPJ: third-party (sacado) cash versus cedente cash. Never the cedente's spreadsheet.
Cedente-supported cash above 70% is a buyer hard reject; a "performing" strip that was performing because the cedente paid is the recompra pathology and is priced as tail.
D debtor
Is the sacado real, alive, solvent, unprotested, not in RJ, not a shell related to the cedente?
Receita situação cadastral, capital social, QSA and address; CENPROT; DJEN and the paid court aggregators; the relatedness graph.
Small — this is where public data narrows the band. But a live sacado does not make a real receivable.
R recourse
Is there a coobrigação / recompra / aval, against whom, and is that party collectable?
The termo de cessão clause actually read; the aval by the sócios; cedente solvency dated; STJ 4ª Turma 16 Dec 2025 — RJ does not suspend actions against coobrigados.
Decides whether the Claims strip is an exit or zero-basis upside (Part 0.3).


The five are never collapsed into one grade because the buyers do not buy one grade. A Premium buyer wants E hard-confirmed, T at least partial, C strong or mixed, DPD ≤ 30, top-debtor concentration below 15%; a Claims buyer wants R evidenced and D solvent and does not care about C; a backstop buyer wants tonnage that meets a box and does not need to believe any individual position. The truth hierarchy that ranks evidence is fixed: cryptographic or official (SEFAZ digVal, registradora, Receita) > bank-originated (CNAB) > registry (RTD, CENPROT, courts) > executed documents (termos, avais) > seller systems > seller spreadsheets > verbal. Nothing from the bottom three tiers ever raises a grade; it can only flag where to look.
4.2 The forensic bridge
Every book is walked across the same bridge, and each step is a subtraction the buyer can recompute himself from the retained evidence: seller-reported face → canonical (deduplicated, reconciled to the informe and the ledger) → existence-supported → title-supported → third-party-cash-supported → buyer-eligible (meets at least one standing box) → FIRM take-out (a buyer has signed for it at a price) → zero / unresolved. On the compiled document's illustration a R$200m reported book decomposes into R$35m clearly nonexistent or problematic, R$45m unresolved, R$20m good enough for a Premium buyer, R$30m producing credible recourse and R$70m fitting a backstop box. A normal buyer sees a R$200m problem. VAZANTE sees three saleable products and two zero-value categories. That is the arbitrage, and it is the reason the carve is kept private: the decomposition is the entire value added, and showing it to the seller is giving it away.
Coverage rule, carried from the audited design: test the top 80% of face — everything above R$250k plus every sacado in the top 80% — position by position, roughly 850 of 4,000 positions, with 100% machine coverage of anything costing R$1 or less; sell the remaining ~20% untested and labelled as such. An extrapolated grade is a claim a buyer cannot check; a labelled untested block is a fact he can price. Every finding is wrapped in a pull() record with a pull_id and a SHA-256 of the source, so a buyer can rederive any classification and VAZANTE never asks anyone to believe anything. The machine proposes; a human signs every existence failure and every title exception above R$250k; a partner signs the book; ties break to the lower grade, because there are eight to ten real buyers and we sell to them repeatedly — a grade that is generous once is expensive forever.
4.3 The Oracle tells you what information is worth buying
Because the buy boxes are machine-readable, the Oracle outputs buyer-specific value consequences rather than grades. For position #918 — E hard-confirmed, T unverified, C strong, D clean, R none, face R$800k — Buyer A is eligible at 14¢ today and at 21¢ if title is confirmed; the value of the title check is R$56,000 and its cost is R$600; the action is RUN TITLE CHECK. Aggregated over a book this is the Lift List: every position one named document away from a higher grade, with the face at stake — on the reference book +R$2.17m of proceeds for under R$35k of cure. Inside the exclusivity window it decides the order of verification work; it is also the single most defensible thing to show a buyer who asks why a strip is priced where it is. And it is why the Oracle and the buy boxes must become one system: an expensive investigation that produces fascinating evidence but moves no buyer's eligibility or price is not done.
4.4 Routing the documented face into three exits
Only FIRM contracted proceeds count. Two design consequences follow and both cut the number down: self-settlement (sacados paying) is a recovery assumption, not a buyer, so its face rides into the residual at the backstop grid and its uplift is carried at zero; and a cedente buyback cannot be firmed inside a ten-day exclusive, so what is sold is the recourse claim, to a claims buyer, at the price of certainty (≈12¢) rather than the price of negotiating the buyback oneself (≈20¢). On the reference book (informe R$210m → documented R$150m, ~4,000 positions, Master/Reag grade mix):
Exit
Slice
Face R$m
FIRM price
Proceeds R$m
Premium
S1 a-vencer / < 30 dpd, sacado-confirmed, title clean
8.0
75¢
6.00
Premium
C1 rest: título executivo, third-party cash ≥ 40%, no competing assignment
10.0
25¢
2.50
Claims
Recourse: coobrigação / recompra clause read, dated solvency file
21.0
12¢
2.52
Claims
Fraud / simulation claims (F1–F3)
15.0
4¢
0.60
Residual
Backstop grid tier 1: C2 / C3 / X1 residue + self-settlement face
51.0
4.0¢
2.04
Residual
Backstop grid tier 2: X2 / X3 tail
19.5
1.5¢
0.29
Zero
NV / no lastro / F rest — fails every box
25.5
0
0
Total
Locked onward proceeds — 9.30¢ documented, 6.64¢ informe
150.0


13.95


Calibrated so the engine reproduces the audited pricing engine exactly (MODEL). Against the engine's full carve of R$18.69m, R$4.74m is not locked and is carried at zero — mostly the cedente buyback that the red team says is most likely worth nothing anyway. Two things to read off the table. Premium is 61% of locked proceeds on 12% of face: one buyer and one R$8m strip of a-vencer paper carry the trade, which is why the Premium price can fall only 10.9% before the reference trade stops existing while Claims can fall 30% and the residual grid 40%. And the residual is 17% of proceeds on 47% of face: the backstop grid matters for certainty, not for value — it is what makes the whole book saleable at one price at all, which is why it is worth signing even at a poor price. Do not confuse "the grid is the floor" with "the grid is the money".
With the Part 0.3 correction applied — Claims counted as locked only where the buyer's payment is unconditional and settles on closing day — the R$2.52m recourse line is the number most likely to shrink on a real book, toward a quarter of itself. The bid sheet must show both the FIRM Claims figure and the zero-basis remainder separately, and the seller bid is computed on the FIRM figure only.
4.5 What the Oracle does not build
No statistical sampling engine (the census rule replaced it). No case-management system and no collection floor — VAZANTE assigns and audits, it does not collect. No client-facing product: the thin Streamlit UI (UPLOAD → RUN → SEE WHAT'S REAL → SEE WHO BUYS → SEE MAX BID) is for the two partners and the developer. No administration or custody technology, ever — it would make VAZANTE the counterparty of the people it sells to. Nothing that resembles a report a seller could pay for, because the moment a seller pays for a report the business is the one MGC refused to be in. And a naming discipline that is not negotiable: never auditoria, never parecer, never laudo in a seller's hearing — acting as an auditor without registration is a crime under Lei 6.385 art. 27-E, and a fund-level score is never published to anyone.

Part 5 — The buyers and the standing boxes
The buyer side is what makes the timeline arithmetically possible. Three FIRM prices inside a five-day sub-window, from specialists who each run more than a deal a month, cannot be obtained deal by deal; they can only be obtained by having the box signed in advance and treating each tape as exception analysis against it. Standing grids are therefore not a nice-to-have; without them VAZANTE is a sixty-day process business with no exclusivity. The full package — the calibration pack in Portuguese, the thirty archetypes, the three synthetic carteiras, the evidence ladder, the three Caixa de Compra Permanente templates with their Parte A / Parte B structure, the machine-readable box and the openers — is the companion document. This part is what MGC needs to hold in his head.
5.1 The map, by exit
Exit
Who, in call order
Note
Premium — performing, 0–30 dpd, cash-confirmed, held as yielding paper
SRM / Empírica; Fram; Aporema; B Invest; Cupertino. Second wave: Riza, Kinea, Augme, Galápagos, Artica. Liqi and XP as distribution only, never calibration.
The buyer is buying duration and yield, not recovery; hurdle 25–28%. A risco-sacado platform is not a secondary buyer — its model runs on an approved corporate limit and the sacado's own confirmation, both absent in a stranger's aged duplicatas — except for the sub-strip where VAZANTE has obtained written sacado confirmation, which is exactly their artefact. The dependable Premium buyers are performing-receivables gestoras. Starboard: do not call. Pátria / Solis: a ten-day exclusivity cannot survive their committee.
Claims — evidenced recourse, fraud / recourse claims, RJ-adjacent
Prisma (first call in the package); Möbius (runs a fund literally named Möbius Legal Claims 1 – FIDC, VERIFIED); JiveMauá (also residual); Root.
The buyer is buying a legal outcome, priced in years; one question above all others: is there a solvent person at the end of the claim? The fact that sets the grid: STJ 4ª Turma, 16 Dec 2025 — an RJ does not suspend actions against coobrigados and avalistas — so a personal aval from the sócios is worth roughly four times a bare recourse clause. Put that in front of Prisma in the first ten minutes.
Residual / backstop — everything else that meets a standing box, at a grid
JiveMauá (first backstop call; GC has the relationship); Recovery; Paramis (reported Oct 2025 buying a multicedente/multissacado FIDC house, VERIFIED); IOX; then 051, MA7, Rooftop, BlueOak. Enforce / BTG only under three conditions.
The buyer is buying tonnage at a price and monetises it on his own floor; hurdle ≈35% for an NPL FIDC. Two live grids, never one. Enforce / BTG — largest balance sheet, worst partner — only when the residual block exceeds ~R$40m, a second grid is already signed, and VAZANTE is not asking them for money in the same conversation; approach for a grid in writing, never for a deal.

5.2 How a box is manufactured: three passes
Pass 1, synthetic calibration. Forty-five minutes on screen, in the room, with someone who can price: thirty standardised archetypes, all synthetic, no NDA; for each, four ten-second answers — buy / pass / analyse; price per real of face; maximum size; the one fact that would change the answer. Then three synthetic carteiras and the evidence ladder (what makes you pay more: written sacado confirmation, digVal match, registry title, CNAB third-party cash). Output: BUY_BOX_V0, returned as a pre-filled Parte A for the buyer to tick, strike or overwrite. Pass 2, shadow portfolio. V0 run against one real anonymised book: "our reading says you buy these 263 positions for about R$4.2m and pass on these 911 — directionally right?" The buyer corrects at position level, or he has not read it. Signing Parte B — one page — converts the corrected box into a standing monthly mandate: box, grid, capacity, validity, retrade list, signed by someone with power to bind. Output: V1. Pass 3, the real transaction. What they bid, what committee rejected, what they retraded, what settled. Output: OBSERVED_BUY_BOX_V2, which dominates from deal 3 onward: when the stated box and the observed box disagree the observed box wins and the difference is logged — buyer says 15¢, has paid 11.7¢; says title does not bother him, retraded four of four times when T was unconfirmed. Every bid is stored forever.
Price status on every line of every box is one of FIRM / RECENT OBSERVED / GRID / HISTORICAL / ESTIMATE, and confidence is CONFIRMED / OBSERVED / INFERRED / UNKNOWN. Only FIRM enters locked proceeds. A grid is a price list, not a bid.
5.3 The first three calls, and why in that order
Prisma, Claims, this week so the session costs nothing in relationship capital and can be run badly without damage. The pack has never been in front of a real buyer; it will have three questions that do not land, one ambiguous archetype and a scale that reads wrong. Find that out at Prisma, fix the pack the same afternoon, then take it where a fumbled session costs a relationship. JiveMauá, residual backstop, same week or next — the backstop grid is the binding constraint on every future bid and the longest document to negotiate, because a standing monthly commitment clears a committee, not a trader; the target of the first meeting is agreement in principle that a standing box refreshed monthly is a thing they will sign, and if they will not sign a standing anything VAZANTE learns it in week one rather than on Day 7 of a live exclusivity. SRM / Empírica, Premium, week two — the strip where the money is per unit of work and the easiest yes, which is why it goes third: an easy yes teaches nothing about the pack, and Premium buyers are the most replaceable of the three roles. Then revise the pack once, then Möbius, Recovery and Paramis, Fram: seven sessions, two counterparties per exit plus a spare.
5.4 What counts as a yes
Stage
Event
The test
Does not count
0
Reply to the email
Nothing. A reply is not a stage.
"Interesting, send more"
1
Session held
45 minutes with someone who can price; ≥ 20 of 30 archetypes answered with a number or range
A meeting with IR / BD; "we'd have to look at it" × 30
2
V0 box returned
Parte A back, marked up, hard filters stated, at least four price lines carrying a number
"The box looks about right"
3
Shadow-portfolio correction
Corrections at position level, naming lines or rules
"Roughly, yes" — politeness; the V0 was never read
4
V1 — Parte B signed
A standing monthly mandate signed by someone with power to bind
A signed Parte A alone
5
First real bid
A dated indicative on a specific pool with an expiry, a named signatory and a stated route to FIRM; enters locked proceeds only when FIRM
A grid


"Just send us what you find" is a soft no. The answer is never a generic letter and never a second explanation of VAZANTE; it is an indicative request on one specific anonymised pool with a date on it — thirty-eight sacados, R$14.2m of face, digVal matched on 94%, 68% of 24-month cash from the sacado by raiz-8 — because specificity moves the question from "do I want to be on your list" to "do I want this, at this price, by Friday", and the second question cannot be deferred with a pleasantry. The pool must be real (Deal 0's tape, anonymised) or the trick works once.
5.5 The structural conflict that the org chart creates
Prisma is the natural Claims buyer, the most likely bridge lender, GC's office, GC's friend and the one counterparty that has already paid. Absolute rule 4 — never let one buyer control both funding and essentially all exit pricing — is breached by the org chart before anyone makes a decision. The mitigation is mechanical, not moral: Prisma is never the settlement facility; Claims is never more than one of three FIRM legs; and a second Claims counterparty (Möbius) is calibrated before deal 2. The friendship is an asset for the first session and a risk for the tenth, and the boxes are what make the tenth session a transaction rather than a favour.

Part 6 — Entity, tax, title, warranties, settlement
Four sentences carry this part. There is no licence: buying direitos creditórios with own money and reselling them is a Civil Code assignment (CC arts. 286–298), not banking (Lei 4.595 art. 17 needs third-party funds), not a securities activity (direitos creditórios are absent from the Lei 6.385 art. 2 list), and not something the Banco Central authorises (VERIFIED). The whole tax answer turns on one word — deságio — and its base. IOF runs the wrong way from what you would guess: it is triggered by the acquirer being a factoring company and the contribuinte is the assignor. And same-day is the cash-safe design and the tax-dangerous one: a purchase contractually conditioned on the resales invites Receita to say VAZANTE never owned anything and is really an intermediary earning a fee.
6.1 The buying entity
Vehicle
Title and licence
Tax posture on the spread
Verdict
Ltda
Holds title; no licence
Presumido contested (PN 5/2014); Lucro Real base case ≈ 32–37% of spread
Deals 1–3. Days to set up, ≈R$5k. The cheapest path to a real transaction
S.A. fechada
Same
Identical
Only if debt funding or CR issuance is later needed
SCP
Cannot hold title — CC art. 991: the activity is carried on by the sócio ostensivo in his own name
Equiparada a PJ; no saving
Not the buying entity. A per-deal profit-sharing wrapper over a Ltda at most
Captive FIDC-NP
Holds title; rented regulated plumbing
Best available: no IRPJ / CSLL / PIS / COFINS / IOF at fund level; 15% at the cotista if PF and if entidade de investimento
From deal 4, if three gated questions clear. 45–90 days; R$200–400k/yr
Securitizadora shell (e.g. rented via EMCASH)
Holds title
Worst of both: Lei 9.718 art. 14 VII now reads "securitização de crédito" — Lucro Real; SC Cosit 99/2023
Reject. Take EMCASH's registradora plumbing and their name on the buy side of a strip; never the wrapper


The factoring characterisation is not decided by the company's form but by whether it carries on "prestação cumulativa e contínua de serviços de assessoria creditícia … compras de direitos creditórios" (Lei 9.249 art. 15 §1 III d; Lei 9.718 art. 14 VI). CARF held unanimously on 2 July 2026 (Acórdão 3101-004.842, VERIFIED, administrative, single turma, not binding) that the services element is a requirement, not decoration. That is the drafting instruction: everything in VAZANTE's constitutive documents, contracts, invoices and correspondence must be consistent with buying and selling assets on own account and inconsistent with providing a continuous service to cedentes. The objeto social in P3 §1.3 writes the three defences into the contrato social — no services to third parties and no fee, commission or success-based remuneration (the CARF defence); no mútuo, desconto or intermediation of third-party funds (the Lei 4.595 / 7.492 defence); no dealing in valores mobiliários (the Lei 6.385 defence). CNAE: never 6491-3/00 (fomento mercantil); the accountant records in writing why not. And the anti-factoring facts are documented from day one: purchase from a holder, not the sacador; no ad valorem commission; no continuous credit services to anyone.
The captive FIDC-NP is a tax wrapper, not fund management — no third-party capital, no management fee, no cotista to answer to, no fundraising — and it is by an order of magnitude the largest single lever in the design: on the worked deal the tax on R$3.5m of spread is R$1.2m in a Ltda forced to Lucro Real and R$0.5m in a captive fund with PF cotistas; over twenty deals the gap is roughly R$13.8m against R$0.6–1.2m of running cost; on the reference book it moves the biddable price by ≈R$1m. It has four real problems, each GATED: the 15% is definitive only for individuals, so MGC and GC hold quotas personally (PJ cotistas land at ~34%); an NP class is for investidores profissionais only (Res. CVM 175 Anexo II art. 15), so both must individually pass the R$10m test; the entidade de investimento test (Res. CMN 5.111/2023) requires discretionary professional management, and the more captive the fund the more fragile that claim — the first question to put to a candidate administrador in writing before any spend; and art. 42 forbids acquiring from related parties, so the fund buys directly from the seller with VAZANTE as consultoria especializada, never from VAZANTE. Run the three questions with Vórtx, Oliveira Trust, Singulare or BRL from week one; migrate from deal 4 if all clear; otherwise stay in the Ltda and fight the presumido question on the CARF reasoning. Do not stand up the fund before the questions are answered in writing.
6.2 Tax: the question that decides the chapter
Lei 9.718 art. 14 VI obliges to Lucro Real any PJ engaged in "compras de direitos creditórios resultantes de vendas mercantis a prazo" as factoring (VERIFIED). What is not settled is the base. Three readings of receita bruta on the worked deal: (i) the spread, R$3.5m; (ii) the resale price, R$11.0m; (iii) the literal PN Cosit 5/2014 §32 and Decreto 4.524/2002 art. 10 §3 reading — face minus cost, R$142.5m — under which the PIS/COFINS bill alone is R$5–13m and total tax R$25–34m on a R$3.5m spread. The third is low-probability, has never appeared in any VAZANTE document, and is the only exposure in this business that ends the company. Its sole defence is that VAZANTE is not an empresa de fomento comercial — a facts-and-circumstances question decided on habituality, CNAE, contract form and whether it buys from the sacador or from a third-party holder. It is the first question for counsel, and the opinion only counts if it contains a number: total transaction tax as a percentage of gross onward proceeds, with express positions on Decreto 4.524 art. 10 §3, Lei 9.718 art. 14 VI, and LC 214/2025 from 1 January 2027 (the CBS/IBS transition — if the resale sits inside the regime específico de serviços financeiros the base is the margin and the desk survives; if in the regime geral the base is gross and it does not; nobody has asked). The one-page consulta is Appendix A. R$12–18k, 25 days, and it must be bought before Deal 1, because changing the corporate form afterwards is a taxable reorganisation.
Two further tax facts with operating rules attached. IOF-crédito on an assignment is triggered by the acquirer being a factoring company (Decreto 6.306 art. 3 §3 II) and the contribuinte is the assignor (art. 4 p.ú.) with the acquirer as responsável; so on the buy leg it is the fund's tax with VAZANTE collecting it — and in practice a number the seller pushes straight back into the price — and on the sell leg it is VAZANTE's only if a buyer is a factoring house. Rule: never sell a strip to a fomento mercantil vehicle; sell to FIDCs and securitizadoras. And the Lucro Presumido ceiling of R$78m of receita bruta a year means that if the resale price is the base, eight deals in a calendar year blow it and force Lucro Real the year after — a scheduling constraint, not a theoretical one. The favourable authorities (CARF 3101-004.842; SC Cosit 169/2018) are administrative and non-binding; PN Cosit 5/2014 is the binding internal instruction and points the other way. The adverse case is modelled as the base case for that reason, and any better outcome is upside.
6.3 Title: the instrument and the fastest lawful path
The cessão is a single Instrumento de Cessão de Direitos Creditórios with the art. 288 form (public instrument or private instrument registered at the RTD for efficacy against third parties), tradição of the títulos and the lastro archive as a condition precedent (CC art. 291), the art. 295 existence warranty expressly affirmed, and the custodiante's written release. Notice to thousands of sacados (CC art. 290) is done once, at the buyer's election and cost, through the fund-letterhead notificação de cessão at about R$9 a position; it perfects efficacy against the debtor, it does not perfect title. The registradora layer is where title is actually tested: participant contracts with CERC and Núclea in VAZANTE's own name, giving it its own consulta de duplicidade, before Deal 1 — not a fund instruction that can be withdrawn mid-deal. Whether the registradoras will contract with a two-person Ltda at all is GATED and is condition 2 of the decision; if they will not, the C1-E exclusivity grade cannot exist and the desk must restrict itself to books where the paper is already registered, a much smaller and later market.
Day
Act
Owner
Gate
D−10
Regulamento read; assembly question answered in writing; custodiante identified and contacted
VAZANTE
No answer → no exclusivity
D−7
Instrumento de Cessão and the three onward instruments in final form; custodian and registradora instructions drafted as annexes
Counsel


D−5
Seller signs the custodian and registradora instructions, held in escrow, effective on closing
Seller
The condition precedent that most often slips
D−3
Custodiante confirms in writing: archive inventory count and face reconciled to the ledger; split into three sub-archives agreed
Custodiante
< 90% match on count and face → pause
D−2
Buyers' funds cleared into the conta vinculada; escrow agent confirms
Escrow bank
All three by 17:00 or the sequence resets
D0
The matched settlement (6.5)
All
All-or-none
D0–D+2
RTD registration of all four instruments (São Paulo, electronic)
VAZANTE
Third-party efficacy
D+1–D+5
Registradora movements confirmed; sub-archives delivered against receipt
VAZANTE




One business day for the economics, three to five for the registry layer. The binding constraint is not the law; it is the custodiante's operational calendar and the seller's willingness to sign the custodian instruction early — both visible on day one, which is why they are gates. If an assembly is required, add 15–30 days (convocação at least ten days in advance under Res. CVM 175 art. 72).
6.4 Warranties: the narrow list, and why the remedy is an index
The seller warrants eight things on the signing and closing dates, and nothing else: existence (CC art. 295 affirmed, not excluded — the opposite of most Brazilian NPL contracts); title and absence of prior dispositions (art. 298; no cessão, endosso, promessa, garantia or dupla cessão); completeness of the specified fields — anchored to a named schedule the parties acknowledge as the basis of the price, which converts a vague completeness warranty into a testable one; no undisclosed settlements, side letters or adjustments; the full 36-month history of substituições and recompras by position, trigger, date and value — the two things the seller alone can know and the Oracle cannot see; integrity of source records (CC art. 225, so a manipulated file is a breach of a representation rather than a forensic argument); powers and regularity, including that the sale does not need BCB authorisation because the carteira is not bem da massa; and cessibility. The seller does not warrant solvency, collection, recovery or enforceability; the cessão is pro soluto under art. 296.
The remedy is arithmetic, not litigation: put-back at the implied price per real of eligible face (purchase price ÷ eligible face, fixed at closing) for existence and title breaches, and indemnity at that price × affected face for the rest, drawn first from a conta vinculada de retenção in the seller's own name — 15–22% of price for 120 days on the data warranties and 24 months on existence and title — so that the fund's cotistas received the whole price and part of it simply cannot move. Disputes on quantum go to a single expert within fifteen business days; a 120-day escrow with no fast mechanism is a 400-day escrow. Global cap 15% of price except for dolo or fraud, where there is no cap and no time limit.
VAZANTE's own reps to buyers are capped, time-limited (120 days, 15% of the buyer's price) and pass-through: it warrants that it holds title, has not encumbered the paper, delivered the tape and evidence archive unaltered, actually ran the tests described in the Memorial de Verificação with evidence a buyer can rederive, and hid nothing it knew — process risk, which is exactly MGC's allocation. Everything else it assigns back-to-back: all of its warranty claims against the seller, in proportion, including direct access to the seller's retention account. That clause is what makes a same-day flip commercially honest — a buyer who takes a VAZANTE warranty is taking a covenant from a company with no balance sheet, and what he actually wants is a claim against the fund, which has money at closing. Whether the art. 295 warranty can be capped at all against a professional buyer is GATED; if it cannot, the seller retention must always equal or exceed the sum of the buyer retentions (on the worked deal 22% of R$7.5m against 15% of R$11.0m), and VAZANTE is never net short on escrow.
6.5 The matched settlement
Brazil has no delivery-versus-payment infrastructure for a cessão, and no bank has yet been asked — that is condition 5. The design is one Instrução Irrevogável e Conjunta de Liquidação, signed by the seller, VAZANTE, all three buyers and the bank at T−5, that makes the whole sequence a single indivisible instruction: no step releases unless the previous one is certified, and a partial closing is forbidden in the instruction itself so that no individual can improvise one at 11:00 on a Friday.
T
Step
If it fails
T−2
All three buyers fund the conta vinculada
Not all funded by 17:00 → closing does not occur; sequence resets
09:00
Escrow bank certifies cleared, irrevocable funds for all three buyers ("cleared" defined in writing as settled, not a TED in flight)
Abort. Seller not paid. Arras retained from the failing buyer
09:30
VAZANTE certifies conditions precedent; custodiante confirms archive ready
Abort
10:00
Seller executes the Instrumento de Cessão (ICP-Brasil); registradora instruction transmitted


10:30
Bank releases 85% of the price to the fund's own account; 15% to the seller retention account


11:00
Custodiante releases the archive under a termo de entrega with a hash manifest; VAZANTE executes the three onward instruments; three registradora instructions transmitted


11:30
Bank releases 85% of each buyer price to VAZANTE; 15% into each buyer retention account


12:00
Net proceeds retained; RTD filings lodged




Who bears the risk if a buyer fails after the seller has transferred: nobody, because the sequence makes it impossible, and where it is not impossible it is priced. A buyer failing before 09:00 leaves VAZANTE in breach of the purchase contract, so VAZANTE's own arras to the seller are capped at what it can pay from cash — 3–5% of price, R$225–375k on the worked deal — and never more; this is the one uninsured cash exposure in the design and it is sized deliberately. Resale conditionality lives in the escrow instruction, not in the purchase contract, and the purchase contract names no buyer — which is also the tax answer to "VAZANTE never owned anything". If a seller will not accept a simultaneous closing conditional on three buyer fundings, the correct answer is to shrink the book, not to finance it: the unmatched exposure on the largest book in a base-case campaign is R$15m at P50 and R$31m at P90, which is a different business.
The retrade is defeated by two rules working together. Rule 1 protects only if "contracted" means signed with arras: the firm whole-book bid goes to the seller only after all three onward contracts are signed and the 10% arras confirmatórias (CC arts. 417–420) are in the account — which moves the buyer contracts from Day 9–10 to Day 7 in the compiled timetable, and it is a real change. The take-out form states the price is firm and irrevocable to a date, that confirmatory verification was completed before signing, and — the clause that does the work — that a change in market conditions, CDI, appetite, internal policy, committee, funding or any new analysis is not a condition, excuse or ground for termination; naming the excuses is worth more than a large multa because the retrading buyer's position depends on ambiguity. Rule 4 is the structural protection: on the worked deal the residual buyer is more than half of proceeds, which is already close to a breach — split the residual across two backstop houses or price the retrade option in. Res. CVM 160 art. 8 is not relevant: there is no securities offer, so there is nothing to exempt; the moment a strip is wrapped in an SCP participation, a CR, a note or a "co-investment" the entire CVM regime attaches. The principal design's greatest legal virtue is that it never issues anything.
6.6 Perimeters, LGPD, and what VAZANTE must never say
OAB: none of this is consultoria jurídica because VAZANTE advises no one — it reads contracts to price its own purchase; it never opines to a seller or buyer on their rights, and never uses the words laudo, parecer or auditoria. CVM: three perimeters, all clear — no securities are issued, no third-party assets are managed, no consultoria de valores mobiliários is rendered — with one trap: the captive fund makes VAZANTE a consultoria especializada under Anexo II, a role the regulation contemplates without registration. BCB: a fund whose administrador is under a liquidante sells its own carteira, which is not bem da massa, so Lei 6.024 art. 16 authorisation is not needed (the warranty says so expressly); a massa liquidanda selling its own book does need it. COAF: the activity is inside Lei 9.613 art. 9 p.ú. V and Res. Coaf 41/2022 — registration and reporting from day one, and it goes in the counsel letter. LGPD: the status changes — VAZANTE becomes controlador of the data it buys, not operador for a client — so the RIPD, the lawful basis for each dimension (legítimo interesse for verification; execução de contrato for the resale), the retention rule, and the five things that must exist before the first real portfolio are built during the Deal 0 window, not after it. The pull_id evidence architecture applies to who accessed data as well as what the Oracle found.

Part 7 — Economics as the model computes them
P5_model.py replaces the fee-model Monte Carlo entirely: no fee, no mandate, no waterfall. VAZANTE buys the whole book for cash and resells three pieces. Every figure below is MODEL unless tagged, and the base tax characterisation is the favourable one (T1: Lucro Real, spread as receita financeira, 37.1% of spread); the adverse readings are run as sensitivities and reported. The reference book is the one the pricing engine was audited on: informe R$210m → documented R$150m, ~4,000 positions, Master/Reag grade mix, locked onward proceeds R$13.95m (Part 4.4).
7.1 One trade
Reference book
R$m
Note
Locked onward proceeds L (FIRM only)
13.953
9.30¢ documented, 6.64¢ informe
Non-purchase costs C (data 55k, registries 18k, counsel 180k, notification 36k, closing 45k, specialists 45k, funding 25k, warranty reserve 174k)
0.578
R$0.781m on deals 1–3 (×1.35). Driven by position count, not face
Maximum firm seller bid (1.20×, tax inside basis, T1)
9.679
6.45¢ documented, 4.61¢ informe. ≈ 73¢ per R$1 of L
Tax at that bid
1.370
37.1% of spread
All-in cash basis
11.627
L ÷ basis = 1.200×
Locked gross contribution
3.695


Locked after-tax contribution
2.325
= L ÷ 6, in any regime
Zero-basis upside carried at nil
4.738
The engine's full carve less the FIRM number


The 1.20× rule binds, not the hurdle, and by a wide margin: the hurdle alone would allow a bid of R$11.87m; the rule allows R$9.68m. The discipline gives away R$2.2m of biddable price, 22.7% of the bid. That is the price of not becoming a distressed fund, and it is the number a partner will want to negotiate away on deal 6. Against the pricing engine's own seller floor (1.3× hold-case-at-CDI, capped at 0.85× block bid — R$9.0m), the max bid clears by R$0.68m, 7.5%: that is the entire negotiating room on the reference book, and it is thin by construction.
Sensitivity
L
Max bid
Gross contribution
Δ contribution
Base
13.95
9.68
3.70
—
Premium buyer's price 20% lower
12.25
8.43
3.25
−0.45; −R$1.25m of bid, 12.9% — kills the trade against 7.5% of room
Residual grid 1¢ lower, both tiers
13.25
9.16
3.51
−0.19; 5.4% of bid
20% of Claims fails evidence, found pre-bid
13.54
9.38
3.59
−0.11
Same defect found post-bid
13.02
9.68
2.76
−0.94 — 8.7× the pre-bid cost
Seller asks 15% above max bid
13.95
11.13
2.24
L ÷ basis 1.11× — pass; L would need +7.9%


The asymmetry in the third and fourth rows is the entire argument for the design: the same evidence failure costs R$0.11m before the bid and R$0.94m after. Break-evens, and only one matters: the R$1.5m hurdle bites only if L falls 59% (decorative on a reference-sized book); against the seller's floor, the Premium price may fall 10.9% before the trade stops existing, Claims 30%, the residual grid 40%. The Premium strip is the trade; everything else is padding.
Tax as a bidding variable, on the same book: max bid R$9.68m under T1, R$9.49m as factoring (T2), R$8.56m under the adverse gross-receita reading (T3, −12%, more than the whole negotiating room), and R$10.64m inside a FIDC wrapper (+R$0.96m). After-tax contribution is R$2.33m in every one of them. Tax does not cut margin; it cuts the bid, and therefore the deal count.
7.2 The distribution of books, and the size floor
Face R$m
Lineage
L
Max bid
Binds
After tax
P(trade)
Seller floor
35
deep
3.26
1.38
hurdle
0.94
10%
2.02
60
deep
5.58
3.67
hurdle
0.94
58%
3.46
100
deep
9.30
6.35
1.20×
1.55
63%
5.77
150
deep
13.95
9.68
1.20×
2.33
65%
8.65
250
deep
23.25
16.33
1.20×
3.88
66%
14.42
100
healthy
19.21
13.52
1.20×
3.20
32%
14.99
150
healthy
28.82
20.42
1.20×
4.80
33%
22.48


A healthy-but-orphaned book has twice the locked yield (19.2¢ against 9.3¢) and is still the worse trade: four other buyers can price it, so its seller's reservation sits near 78% of L, above the 73.5% payout cap. P(trade) is a third lower at every size. The floor is a locked-proceeds number — L ≥ R$5.66m at the R$1.5m hurdle, R$7.55m at R$2.0m, R$9.44m at R$2.5m — which on the deep-gap lineage at the seller's own floor is R$58m / R$74m / R$90m of documented face. The floor is set by the seller's reservation price, not by our cost stack; R$295k of the per-deal cost is fixed regardless of size, 9% of L on a R$35m book and 1.3% on a R$250m book.
7.3 The cost base
Monthly fixed stack
R$k / month
Note
Developer (Codex / the Oracle), existing Sutphin head, fully loaded
32


Permanent forensic lead
0
Contract specialists at R$45k per deal instead — the single largest saving
Infra: cloud, model spend, CVM pipeline, evidence store
18


Data: Serasa PJ minimum, CENPROT, courts, registradora, Uqbar
14


Counsel retainer
12


E&O
0
VAZANTE renders no service; there is nothing to insure
D&O
3


Accounting (Lucro Real bookkeeping, audit-ready)
9


Overhead: co-working (GC sits at Prisma), travel
16


BD / channel
8
The machine flags, GC calls; no pré-leitura factory
Total
112
Months 1–3 R$92k; from deal 6 add one analyst → R$131k


Against the fee model's R$230k a month, 51% lower and structural, not a squeeze: the fee model carried people to produce reports on a schedule; this one carries a machine and rents humans per trade. MGC and GC take no salary; their return is the residual. One-off at inception R$350k over months 1–3 — structure opinion, tax opinion on one worked transaction, master SPA, three master onward-sale contracts, LGPD architecture — above the fee model's R$200k because principal, title and tax all have to be papered before deal 1, and worth ≈R$1m of biddable price per reference deal.
The funnel, ASSUMPTION throughout and to be replaced by observation after ten real approaches: seller grants exclusivity 28–50%; survives verification 55–72%; three buyers give FIRM prices 55–75%; seller accepts the max bid — derived, not fixed, from a lognormal reservation price (deep-gap median 62% of L, healthy 78%) compared with the 1.20× bid, which is why healthy books die and ugly ones close; documents and settlement complete 88–95%. Base case: approach → exclusivity 44%; exclusivity → close 15%; approach → close 7%. About three exclusives in four die — worse than the fee model's 70% of engagements — but each death costs R$108–243k rather than a fully loaded 90-day engagement, and dead work is 36% of cash cost rather than 87% of lifetime pre-tax.
7.4 Capital
Under matched settlement VAZANTE never finances the book, and cash is still at risk in four places. At-risk operating capital — the fixed stack while the pipeline is empty, dead-deal cash, warranty draws, and tax paid in good years that is not refunded in bad ones — is R$2.8m at P50 and R$6.7m at P90 on the base case, R$5.4m / R$8.5m on the conservative: hold R$3.0m, and understand that R$8.5m is what it takes to survive the conservative case nine paths in ten. That number is not better than the fee model's R$7.9m; a principal desk that does not close deals burns exactly like an advisory desk that does not close mandates. A feature to name: Lucro Real tax is annual and prior-year losses offset at most 30% of profit (Lei 8.981 art. 42), so a lumpy campaign pays real tax in the years it closes and gets nothing back in the years it does not — the conservative case pays R$1.5m of tax on a lifetime pre-tax loss of R$1.0m, and that is what will happen, not an artefact.
Settlement float with the chain working is R$6.2m at P50 / R$11.9m at P90 (25% of the largest L for three days); if the chain fails, the largest single unconditional seller payment is R$15.2m / R$30.8m, which is a different business. So Deal 1 is sized at the R$60–100m documented end, not R$250m. From deal 3–5, a R$5m committed revolving settlement line — drawn 3–8 days per deal, secured on the acquired book and the assigned onward receivables, CDI+6–9% (≈21% at CDI 13.90%, VERIFIED), 1.0% arrangement, 1.5% undrawn, ≈R$125k a year — arranged after deal 2, before deal 4, and never from a party that is also an exit buyer. Warranty reserve: R$1.5m of accumulated contribution held back from distribution until deal 5 has passed its claim period. Total commitment at deal 1: R$3.0m of at-risk cash plus a R$5m line = R$8.0m, of which R$3.0m can actually be lost — against the fee model's R$7.9m, all of which could be lost, for a fifteenth of the return.
7.5 The 48-month campaign
Supply adapted from the fee model's estate engine rather than reinvented: vehicles sit inside estates (Trustee 63, Reag 110, Master 53, VERIFIED), opening one releases its remaining inventory, and exhaustion is abrupt; rescaled to the R$60m floor, pool 76 workable vehicles and new-orphan flow 27 / 18 / 10 / 6 a year. Hurdle ladder R$1.5m → R$2.0m → R$2.5m. Cycle 2–3 months exclusivity-to-resolution on deals 1–3, 1–2 thereafter. 2,500 paths per scenario, integer deals, because with one to four closes a year the lumpiness is the cash story.
Base case, R$m
Y1
Y2
Y3
Y4
Total
Approaches made
29.8
29.1
23.4
11.5
93.7
Exclusivities granted
10.0
12.4
12.2
6.4
41.1
Deals closed
0.9
1.8
2.2
1.3
6.2
Documented face bought
103.8
209.7
269.4
163.0
745.8
Locked onward proceeds
12.0
24.3
31.1
18.9
86.3
Paid to sellers
7.2
14.6
18.8
11.5
51.9
Locked gross contribution
4.17
8.50
10.96
6.70
30.33
All cash cost (of which dead-deal 5.74; fixed stack 5.38)
3.51
4.35
4.68
3.36
15.90
Pre-tax result
1.32
5.35
7.64
4.11
18.43
Tax paid
0.97
2.08
2.80
1.66
7.51
After-tax cash
0.35
3.27
4.84
2.46
10.92
Partner-day utilisation
71%
100%
91%
47%




P10 / P50 / P90 on the base: closes 2 / 6 / 10; lifetime pre-tax −R$2.5m / +R$15.4m / +R$42.5m; after tax −R$3.5m / +R$9.4m / +R$26.8m; maximum drawdown −R$2.8m at P50, −R$6.7m at P10. All three scenarios:
Scenario
Closes
P10 / P50 / P90
Lifetime pre-tax
Peak-year pre-tax / month
Capital at risk P90
Conservative
1.6
0 / 1 / 3
−R$1.3m
R$0.02m
R$8.5m
Base
6.2
2 / 6 / 10
+R$18.4m
R$0.64m
R$6.7m
Upside
14.4
9 / 14 / 20
+R$62m
R$1.85m
R$4.2m


Under the alternative tax characterisations, base case re-run (1,500 paths, MODEL): factoring reading 5.8 closes, R$16.9m pre-tax, R$9.3m after; adverse gross-receita reading 4.0 closes, R$8.9m pre-tax, R$3.9m after. The tax opinion is therefore worth roughly two closes and R$10m of lifetime pre-tax on the median path — which is the number to have in mind when the R$12–18k invoice arrives.
The KPI. Locked profit per partner-day: R$28.0k at deal level and R$9.8k campaign-level after tax and fixed cost on the base (R$46.4k / R$23.0k upside; R$12.8k / −R$6.1k conservative), against ≈R$1.5k in the fee model — 19× at base, 31× at upside. Two warnings inside it: only 26 of the 172 partner-days per close are live-deal work, so the KPI is dominated by the funnel and optimising the ten-day cycle optimises 15% of the cost of a close; and the base case runs both partners over capacity for 13 months of 48, the upside for 19 — the upside is not deliverable by MGC and GC alone and needs a third dealmaker from around deal 5.
The three numbers most likely to be wrong, and what settles each. The Premium strip (8.0 of 150 documented at 75¢ — 43% of proceeds alone; if it is really 4.0, the bid falls through the seller's floor and the size floor moves to ≈R$95m): one real seller tape, reconciled, inside Deal 0, a one-week answer. The seller's reservation as a share of L (deep-gap median 62%; at 55% the campaign closes 7.8 and earns R$27m, at 70% it closes 4.7 and earns R$12m): ten real approaches with a written indicative band, and the two numbers that come back — what he says he needs, what he signs. The tax base: the signed parecer, worth about R$1m of biddable price per deal and two closes over the campaign.
7.6 The honest comparison with the fee model


Fee model (killed)
Principal model
Revenue per deal
R$2.98m take (Structure D)
R$4.85m gross contribution
Deals per year, base
1.1
1.6
Fixed cost
R$230k / month
R$112k / month
Committed capital
R$7.9m, all at risk
R$3.0m at risk + R$5m self-liquidating line (P90 at risk R$6.7m)
Dead work
70% of engagements; 87% of lifetime pre-tax
36% of cash cost; ~75% of exclusives die
Tax exposure
Presumido + ISS, 16–19% of revenue
37–40% of the spread; base GATED
Ceiling, base peak year
R$0.6–0.9m / month gross
R$0.64m / month pre-tax
Lifetime pre-tax, base
+R$2.0m
+R$18.4m
Locked profit per partner-day
≈R$1.5k
R$28k deal-level; R$9.8k campaign-level


Where it is worse, and these are not small: it takes real title risk with cash on settlement day and no fee to fall back on; it is exposed to tax reclassification in a way the fee model was not; it depends on buyers firming before the seller bid — 25% of post-exclusivity deaths in the base case, the mechanism the entire model rests on, never observed; one buyer carries 61% of proceeds on the reference book; one late leg turns a matched trade into a financed one; and the conservative case is not obviously better than the fee model's. The principal model's advantage is entirely conditional on the funnel working — which is why Part 9 spends its first 120 days testing the funnel and not the Oracle.

Part 8 — Red team, condensed
Sixteen attacks, every one run through the compiled document's own worked example, because arguing about a book nobody has seen is how red teams get ignored. Each carries a verdict and the named change that retires it. The tax attack (Part 0.1) and the Claims attack (Part 0.3) are not repeated here.
#
Attack
Verdict
Named change
1
Seller cannot deliver title to enough of the book. CC art. 291: among competing assignments the one completed by tradição of the title prevails — possession, not date, not documents, not any registry for legacy paper. Art. 288 form failures may sit in VAZANTE's own acquisition. The warranty runs against a dissolving estate (0–20% recovery, 24–48 months).
FATAL as designed; survivable with three changes
20–25% of price in a conta vinculada in the fund's name for 180 days released on a title-clean certificate; CERC + Núclea participant contracts in VAZANTE's own name before Deal 1; tradição of títulos and the full lastro archive as a condition precedent with the custodiante's written release; all C1-U and X2 face priced at zero.
2
Buyers retrade after the "firm" quote. "Locked" is currently a label VAZANTE applies to a buyer's word; the questionnaire even asks buyers when they retrade. One 25% retrade on the largest parcel takes the showcase trade to zero.
Survivable with a named change
LOCKED = executed promessa de cessão signed by an officer with power to bind + arras ≥ 10% in escrow + expiry ≥ seller closing + 5 business days. Anything else enters the max bid at zero. At least two exits with different counterparties before the firm bid; no counterparty above ~45% of proceeds.
3
Matched settlement fails on the day. No DvP for a cessão; someone is naked for a day; a new Ltda's first R$7.5m in / R$11m out from a fund in BCB liquidation triggers PLD review of 5–15 business days. The only party who can bridge is a buyer — the fix breaks rule 4.
FATAL without a named change; fires on ~1 deal in 5
One escrow agent holds all legs under a multi-signature termo de liquidação; "irrevocably available" means "in the escrow account"; a committed bridge from a non-buyer sized at the largest exit parcel (R$3–4m); open the account and run a R$500k test flow with the bank's written comfort before Deal 1.
5
The Oracle is confidently wrong on Deal 1 — 30% of the Premium parcel fails the buyer's third-party-cash re-test.
Survivable pre-tax; fatal with the tax attack
No Premium parcel priced above residual unless 24 months of CNAB covering ≥ 95% of its face is loaded and reconciled; the buyer's confirmatory re-test runs inside the exclusivity window, at his cost, before the firm seller bid; a 15% model-error reserve on Premium for deals 1–3.
6
The seller who can sell will not sell at VAZANTE's price. The signer does not own the loss and his cheapest defence is pleasant delay. In a contested book a balance-sheet buyer decomposes in house without a 1.45× margin and wins every time.
Partly priced in; partly fatal to the stated economics
VAZANTE wins only books that are never contested: purchase price below every balance-sheet buyer's minimum ticket (≈R$4–15m), un-underwritable in the time without the Oracle, seller with no capacity to run a process. That is the real buy box, and it caps contribution per trade.
7
Supply is not 10–30. Relaxing the encargo gate but adding the price gate yields ~7 executable trades over the life on the attack's own hypothesis.
Priced in; not absorbed by the design
Write 6–10. Apply the consequence: no forensic hire, no warehouse, nothing that needs more than ten deals to amortise, no plan that assumes a second cohort. At six to seven deals this is a very good use of two partners' time for two years and a bad use of a company.
9
VAZANTE becomes the named defendant. As principal, the remedy sought is anulação or ineficácia of the cessão, not damages; the Oracle output is the documentary proof VAZANTE knew the value; unwinding leaves a R$11m obligation against R$7.5m returned on a company with no balance sheet.
Survivable; the change costs price
Never buy from a liquidante alone — an assembly resolution or homologation inside an existing RJ docket; build the seller's file for him (hold-at-CDI benchmark, two rejected indications); disclose the existence of a resale-in-parcels strategy in the SPA with seller acknowledgment — never the prices or the routing; a 10–20% seller earn-out above a stated threshold (R$350–700k on the reference trade); restore the conflicts policy.
10
Buyers go around VAZANTE.
Overstated on the buyer side; understated on the seller side
What protects the desk is that VAZANTE buys the garbage bag (F/NV at −2¢): Prisma going direct must own it too. The real risk is a seller learning the method and selling in two lots. Track the share of approached sellers who counter with "we'll sell it in parcels"; above ~30% the desk harvests, it does not invest.
11
"One price, whole book, carve private" fails in practice. A fiduciary's counsel will ask for the decomposition; the assembly resolution that makes a sale defensible presupposes a process; the onward buyers are the same ten names the seller's counsel will call.
Survivable with a named change
Offer the seller a two-round whole-book mini-process that VAZANTE structures — an indicative round of three or four whole-book bidders, then a firm round in which VAZANTE, having done the Oracle work, bids last. Nobody else wants the whole book, so it is uncontested by construction, and it gives the seller the file. The rule "if a book has an advisor and a deadline, don't bid" is about someone else's process on parcels; it stands.
12
The finite life is shorter than 10–30. Duplicata escritural full regime January 2028, not mid-2028; 2026 has 17 BCB liquidations, an outlier; a copyist arrives (p ≈ 0.45) but takes a pool that empties anyway.
Priced in; wrong in the dates by a year
Fix the calendar everywhere. Full spread H2 2026–H2 2027; roughly halves in 2028; closed by 2029. About 24 months of executable window = 7–10 deals, converging with #7 from an independent direction — the most reliable number in the review.
13
1.20× caps the required upside and permits an uncapped loss. A trade passing at exactly 1.20× puts R$8.3m at risk to make R$1.7m pre-tax; kill condition 4 is a qualitative test applied by the two people who want the deal, three days before closing.
Survivable with a named change
Two mechanical caps: unhedged basis per trade ≤ 3× the after-tax locked contribution; aggregate basis across concurrent trades ≤ committed capital in the bank, in writing. On the showcase numbers the first cap sizes the trade at R$2.3m of basis — the collision is the point: either contribution per trade rises or trade size falls.
14
There is no committed capital, and matched settlement conceals that. The trade moves R$7.5m through VAZANTE's account and spends R$0.5–0.8m before any exit is certain.
Survivable with a named change
A written capital commitment sized at the largest single exit parcel plus escrow plus six months of cost — R$3.5–4.5m — signed before the first exclusivity letter. If unavailable, buy only at R$1.5–3m of purchase price and say so out loud.
15
The warranty split is asymmetric in VAZANTE's disfavour. A liquidating estate gives a warranty with no survival and no security; institutional buyers with counsel take a full one from VAZANTE.
Survivable with a named change
Cap VAZANTE's aggregate warranty per deal at 20% of that buyer's price, 12-month survival, and make acceptance of the cap a pre-condition of counting the exit as locked. A buyer who will not cap is indicative, not locked. Plus the back-to-back assignment of seller warranty claims (Part 6.4).
16
Channel and counterparty concentration on GC and Prisma. Rule 4 is not at risk of being broken; the structure breaks it.
Survivable with a named change
Prisma is a buyer or a funder on any given trade, never both; no counterparty above 40% of locked proceeds on any trade; a written conflicts disclosure to every seller naming the relationship. Concentration is the reason the desk can exist; govern it, do not deny it.


8.1 The five numbers most likely to be wrong, and the cheapest test of each
#
Number
Cheapest test
Falsified if
1
6¢ whole book vs 9¢ pieces — an illustration with no transaction behind it; 1.50× where the after-tax arithmetic needs 1.54×
Deal 0 run as a paired question: one public ex-Reag / ex-Trustee book, full tape, to four buyers, parcel bid and whole-book bid in the same email. R$5–8k, 40 partner-hours, 21 days
Sum of parcel bids < 1.55× the best whole-book bid on 2 of 3 books
2
Firm-quote retrade rate — never observed
Do not ask; observe. Four buyers, a real small parcel, a one-page take-out form with expiry and 10% arras. Count who signs. R$5k, 20 days
Fewer than 2 of 4 sign anything binding pre-asset — the rule cannot be satisfied by construction
3
Executable seller count — the funnel was built for an encargo test, not a price test
One written question to 12 named administradores / liquidantes from the cad_fi diff, routed through Prisma / EMCASH / the OAB firm, never cold: "we are a cash buyer of whole carteiras; for fund X our range is R$A–B, 5–7 centavos of informe face — transactable, yes or no?" 30 days
Fewer than 3 of 12 say the range is transactable
4
Claims-parcel survival — 23.5% against a design that carries it at 100%
Three funds, top-20 cedentes by face: Minha Receita + CENPROT + court aggregator + Lei 13.775 inadimplementos, and read the actual termos de cessão for the recompra clause and any aval. < R$6k, 20 days
Under 25% of Claims-routed face sits behind evidenced recourse and a collectable party — Claims is then zero-basis upside and every max bid falls ~R$0.6m
5
Tax characterisation — two mainstream readings at ~17.5% of gross; one tail at 7–10× the spread; CBS/IBS an unasked binary from 1 Jan 2027
One signed parecer on a one-page funds flow (Appendix A). R$12–18k, 25 days
Total transaction tax > 20% of gross onward proceeds under the best available vehicle, or no firm will opine on art. 10 §3


8.2 The paragraph to read aloud to GC
VAZANTE is a two-person principal desk that would buy whole broken FIDC carteiras for cash at around six centavos on the real and resell them in three pieces at around nine, keeping the difference; the machine that prices the book is real and good, the sellers exist, and the buyers are people GC can call today. But the entire economic case was computed before tax, and that one omission moves everything: the showcase trade returns R$0.8m after tax on the mainstream readings, not R$2.7m, and fails our own R$1.5m minimum; the 1.20× rule that was meant to absorb a 24.5% miss absorbs 8.5% and has to be restated as 1.45×; the "9¢ versus 6¢" margin that is the reason the business exists is 1.50× when the after-tax arithmetic requires 1.54×; and pricing the Claims parcel at what a buyer will actually pay for it takes the maximum defensible bid on that same trade from R$7.5m to R$5.3m, which means the showcase trade never happens. Three exposures are new to the principal model: we are the obvious defendant if cotistas or the MPF later say the fund was sold too cheap, and the remedy is unwinding, not damages; the whole design turns on a same-day matched settlement no bank has yet been asked about; and one low-probability tax reading would produce R$25m of tax on a R$3.5m spread. None of that says the business is wrong. It says the arithmetic in front of us is a pre-tax arithmetic for a post-tax business, that six to ten deals is the honest count, and that four documents and one deliberately tiny trade — well under R$50,000 and about 120 days — would settle every one of these questions before a single real of capital is exposed.

Part 9 — The decision
GO WITH CONDITIONS.
Not because the economics as written work — they do not. Because every finding in this document is an arithmetic or documentation problem, not a market problem, and each is falsifiable for money that is trivial next to the R$7.5m the compiled design proposes to move on day one. The Oracle is real, the supply exists at six to ten trades, the buyers are reachable, and the seller-side insight — a liquidante who cannot contract a fee can sell an asset — is correct and valuable. What is not established is that a two-person company can safely own R$150m of contested Brazilian receivables for twenty-four hours. That is the thing to establish next, cheaply.
NO GO if condition 1 or condition 4 fails.


9.1 Five dated conditions
#
Condition
By
Falsified if → consequence
1
Signed tax parecer on the one-page funds flow (Appendix A): total transaction tax as a % of gross onward proceeds; express positions on Decreto 4.524/2002 art. 10 §3, Lei 9.718 art. 14 VI, LC 214/2025 from 1 Jan 2027; Ltda vs FIDC vs SPE compared
15 Oct 2026
Total tax > 20% of gross under the best available vehicle, or no firm will opine on art. 10 §3 → NO GO in the current corporate form; re-test only with a fund vehicle
2
Registradora participant contracts (CERC + Núclea) executed in the acquiring entity's own name, with consulta de duplicidade demonstrated on a live sample
31 Oct 2026
Neither will contract, or duplicidade cannot run on unregistered legacy duplicatas → the C1-E grade cannot exist; restrict to registered-paper books and re-plan supply
3
Binding-quote test. Four buyers, one-page take-out form with parcel hash, price, expiry and 10% arras
31 Oct 2026
Fewer than 2 of 4 will sign before seeing the assets → the rule cannot be satisfied by construction; the desk is a brokerage and should be redesigned as one
4
Paired bid tape. Three public broken books; parcel bids and whole-book bids solicited in the same email from the same four buyers
15 Nov 2026
Sum of parcel bids < 1.55× the best whole-book bid on 2 of 3 books → no manufacturing margin after tax → NO GO
5
One settled micro-trade. Purchase price ≤ R$3m; Premium + Residual only; zero Claims value in the bid; all legs through one escrow agent; tax actually paid
28 Feb 2027
Does not settle within 45 days of the seller's signature, or after-tax contribution < R$250k, or any buyer retrades a signed take-out → STOP and re-scope to advisory or to co-investment alongside Prisma's balance sheet

9.2 Deal 0 and a tiny Deal 1, in parallel
The compiled design sequences "Deal 0, then hunt Deal 1". That is the single most important sequencing change in this document: run Deal 0 as pricing calibration and a deliberately small Deal 1 as execution calibration, at the same time. No document retires attacks 6, 8 and 11 — whether a fiduciary will sign, whether a buyer will settle, what the bank will do — and Deal 0 as a paper exercise on a public book does not retire them either.
Deal 0 is Fictor Invest FIDC, on public data, with no counterparty: R$272m PL, redemption closure, administrador renúncia 19 Feb 2026, assembleia 9 Mar 2026 with a liquidation proposal, and a subsequently observed outcome (accounts found essentially zeroed) to score the Oracle against. Rebuild the full forensic bridge from public filings and check whether the Oracle would have called it. Supplement with the BRB/Tirreno public record as an existence benchmark — the BCB's "insubsistência dos ativos" is regulator-grade ground truth, and the piecemeal CCB sales are printed clearing prices — and with one real anonymised tape from Prisma under NDA, which is the highest-return single action in the whole programme: it costs one conversation with a counterparty who is already a payer. Deal 0's pass rule stands as written: if the Oracle says R$10.8m and three buyers independently say R$9.8–10.9m, proceed; if the Oracle says R$11m and the buyers say R$5m, stop and find out why. Run it as the paired question (condition 4) so the same email tests the manufacturing margin.
Deal 1 is tiny. Purchase price R$1.5–3m, one Premium parcel and one Residual, zero Claims value in the bid, sold and settled within 30 days through a real bank account with tax actually paid; target R$300–600k of after-tax contribution. The money is not the point; the artefact is. In one transaction it produces the observed retrade rate, the real settlement calendar, the tax actually charged, the bank's actual PLD behaviour, the buyers' signed documents and a seller reference that makes the second seller conversation a different conversation. A trade small enough that losing all of it costs less than the tax opinion is not a risk; it is the cheapest data the business will ever buy. Its shape is the Part 3.6 screen's first output, not a name; if the screen is empty in October, a defined tranche of an in-kind holder's paper (archetype G) is the fallback.
9.3 The first 120 days
When
What
Owner and gate
Week 1
Send the tax consulta (Appendix A). Ask CERC and Núclea whether they will contract with the Ltda. Put the three captive-FIDC questions to two candidate administradores in writing. Open the settlement account; brief the bank on the funds flow. Restate 1.45× / 6–10 / January 2028 in every document. Correct the reference trade.
MGC. Nothing is spent on the fund until the answers are in writing.
Week 1–2
Prisma calibration session (Claims) — run it, fix the pack the same afternoon. Ask Prisma for one anonymised tape under NDA. JiveMauá first backstop meeting — target agreement in principle on a standing monthly box.
GC. Stage 1 of the yes ladder is the test, not the meeting.
Week 2–3
SRM / Empírica (Premium). Revise the pack once. First engineering task, twenty minutes: download one informe month, list the ZIP members, diff every header against Suplemento G, freeze the mapping. Run the Part 3.6 screen and the fund-versus-class test on 200 funds. Build the labelled break-date set from the Master / Reag / Trustee / Banvox lineages.
GC; developer. The screen's output is the Deal 1 calling list.
Week 3–6
Deal 0 on Fictor: full bridge from public filings; paired parcel / whole-book question to four buyers (condition 4). Binding-quote test with the same four (condition 3). Twelve written price questions to named administradores, routed warm (P6 test 3). Möbius, Recovery, Paramis, Fram sessions.
Both. Conditions 3 and 4 are decided here.
By 15 Oct
Tax parecer in hand — condition 1. Decide the vehicle. If Ltda: objeto social per Part 6.1, CNAE justified in writing, COAF registration.
MGC. NO GO if it fails.
By 31 Oct
Registradora contracts (condition 2). Master SPA and three master onward-sale contracts reviewed by the OAB firm: escrow in the seller's name, tradição as CP, art. 295 affirmed, art. 288 form, back-to-back warranty assignment, the retrade clause, the all-or-none settlement instruction. LGPD RIPD and the five pre-portfolio artefacts. R$500k test flow through the escrow with the bank's written comfort.
Counsel; MGC.
Nov–Feb
Tiny Deal 1 from the screen: pre-exclusivity pack → Day-1 call with the two-page sheet → exclusivity → tape → three FIRM take-outs with arras → firm whole-book bid → matched settlement → tax paid. Log indicative-to-firm.
Both. Condition 5, by 28 Feb 2027.
On passing 5
Committed capital letter (R$3.5–4.5m). Settlement line arranged after deal 2. Migrate to the captive FIDC-NP from deal 4 if the three gated questions cleared. Third dealmaker decision after deal 3. Hurdle to R$2.0m at deal 6.
MGC.

9.4 The operating rules, on one page
The five absolute rules, restated. (1) Never a firm seller bid until FIRM onward exits — signed, with arras, expiring after the seller closing — cover all-in basis with tax inside by 1.20× (1.45× pre-tax). (2) Never value uncontracted or conditional recoveries: no exit whose price depends on the solvency of a party the Oracle graded counts as locked unless the buyer pays unconditionally on closing day. (3) Never serious work without exclusivity. (4) Never one counterparty as both funder and exit; no counterparty above 40% of locked proceeds; Prisma a buyer or a funder on a given trade, never both. (5) Never turn a fast trade into a recovery business; never a partial closing.
Kill conditions, mechanical. Title not transferable to enough value. Exits below the rule. After-tax contribution below R$1.5m / R$2.0m / R$2.5m. An unresolved fact that could exceed the contribution. Unhedged basis above 3× after-tax contribution. Aggregate basis above committed capital in the bank.
Seller rules. Sell to us only if the loss is booked or the signer has no NAV to protect. Whole book, one price; the carve's prices and routing stay private; the existence of a resale-in-parcels strategy is acknowledged in the SPA. Never from a liquidante alone. Never in someone else's process. Offer our own two-round whole-book mini-process where the seller needs a file. Arras to the seller capped at 3–5% of price. Track the share of sellers who counter "we'll sell in parcels"; above 30%, harvest.
Buyer rules. Standing boxes before tapes. Only FIRM enters the numerator. Two live residual grids, never one. Never sell a strip to a fomento mercantil vehicle. Premium buyers are performing-receivables gestoras, not risco-sacado platforms. Enforce / BTG only under the three conditions. A buyer who will not cap VAZANTE's warranty at 20% is indicative, not locked.
Words. Never laudo, parecer or auditoria to a seller. Never a fee, a mandate or a report. The sentence is: "we buy your whole carteira, cash, one price, ten business days."
Numbers on the wall. 73¢ per R$1 of FIRM proceeds is the ceiling on any seller bid (72¢ as factoring, 80¢ inside a FIDC). R$60m documented is the floor. Ten deals is the plan. January 2028 is the clock. Indicative-to-firm 0.85–1.15. R$28k of locked profit per partner-day is the KPI.

Appendix A — The one-page question to tax counsel
Send exactly this. Do not add narrative. Ask for one written answer with citations and the counsel's own view on each of the three readings of receita bruta, with an express degree of confidence (provável / possível / remoto) on each position.
CONSULTA TRIBUTÁRIA — OPERAÇÃO ÚNICA, RESPOSTA ESCRITA. Sutphin Ltd. — Confidencial.
1. Os fatos. Sociedade brasileira ("SOCIEDADE"), não financeira, sem autorização do BCB ou da CVM, com recursos exclusivamente próprios: (a) adquire, mediante cessão civil onerosa e pro soluto, sem coobrigação do cedente quanto à solvência do devedor, a totalidade de uma carteira de direitos creditórios de um FIDC, por R$ 7.500.000,00; (b) a carteira tem valor de face documentado de R$ 150.000.000,00, na maior parte vencida e inadimplida, composta de duplicatas, direitos creditórios lastreados em NF-e e, eventualmente, CCB; (c) entre 1 e 30 dias após a aquisição, a SOCIEDADE aliena a carteira, fracionada em três lotes, a três adquirentes independentes (FIDCs e/ou companhias securitizadoras), por R$ 3.000.000,00 + R$ 2.000.000,00 + R$ 6.000.000,00 = R$ 11.000.000,00, também mediante cessão onerosa pro soluto; (d) a SOCIEDADE não cobra de ninguém honorário, comissão, taxa de êxito ou remuneração por serviços; não presta assessoria creditícia, gestão de crédito, seleção de riscos ou administração de contas a receber; não realiza cobrança dos sacados; não concede mútuo, financiamento ou desconto; (e) custos de transação dedutíveis estimados: R$ 500.000,00; (f) a operação será repetida 6 a 10 vezes ao longo de aproximadamente três anos, com vendedores e adquirentes distintos.
2. As perguntas. 2.1 Receita bruta. Qual é a receita bruta da SOCIEDADE para IRPJ, CSLL, PIS e COFINS: (i) R$ 3.500.000,00 (preço de alienação menos custo de aquisição); (ii) R$ 11.000.000,00 (preço de alienação); ou (iii) R$ 142.500.000,00 (valor nominal menos custo, na literalidade do §32 do PN Cosit nº 5/2014 e do art. 10, §3º, do Decreto nº 4.524/2002)? Manifestação expressa sobre a aplicabilidade a carteira inadimplida e revendida sem cobrança, e sobre a SC Cosit nº 169/2018 ("valor efetivamente recebido"). 2.2 Base de aquisição: custo dedutível/oponível e momento de realização. 2.3 Regime: obrigatoriedade do lucro real pelo art. 14, VI ou VII, da Lei nº 9.718/1998; em caso negativo, percentual de presunção (art. 15 da Lei nº 9.249/1995) considerando a LC nº 224/2025 e a IN RFB nº 2.305/2025; manifestação sobre o Acórdão CARF nº 3101-004.842, de 02/07/2026. 2.4 Limite de R$ 78 milhões: qual receita se compara ao limite e em quantas operações anuais ele é atingido. 2.5 PIS/COFINS: regime, base, créditos sobre o custo de aquisição, aplicabilidade do art. 3º, §2º, IV, da Lei nº 9.718/1998 e do Decreto nº 8.426/2015, considerando o Acórdão CARF nº 3302-014.811. 2.6 IOF: incidência na aquisição (art. 2º, I, "b"; art. 3º, §3º, II; art. 4º, p.ú., do Decreto nº 6.306/2007) e na alienação a FIDC, securitizadora, instituição financeira e empresa de fomento; contribuinte, responsável, base, alíquota e prazo em carteira já vencida; alíquotas após os Decretos nº 12.466/2025 e 12.499/2025. 2.7 ISS: itens 10.04, 15.01 e 17.23 da LC nº 116/2003; risco na entrega de arquivo de evidências sem preço destacado. 2.8 Retenções: IRRF e CSRF (art. 30 da Lei nº 10.833/2003). 2.9 CBS/IBS: enquadramento no regime específico de serviços financeiros da LC nº 214/2025 (arts. 182 e 193); base, alíquota, creditamento; o que muda em 2026, 2027 e 2029–2032; diferença se a adquirente for FIDC classificado como entidade de investimento (art. 193, §5º). 2.10 Prazo de detenção: o que muda se o título for detido 1 dia em vez de 30; risco de requalificação da SOCIEDADE como mera intermediária se a aquisição for contratualmente condicionada à revenda simultânea, e os elementos contratuais e contábeis que o mitigam. 2.11 Veículo: entre Ltda, S.A. fechada, SCP, FIDC-NP próprio com cotistas pessoas físicas e companhia securitizadora (Lei nº 14.430/2022), qual apresenta a menor carga lícita, considerando a Lei nº 14.754/2023 e a Res. CMN nº 5.111/2023; no FIDC, se os 15% na fonte são definitivos para cotista PF e se o fundo captivo satisfaz o requisito de entidade de investimento. 2.12 PLD: sujeição à Lei nº 9.613/1998, art. 9º, p.ú., V, e à Res. Coaf nº 41/2022.
3. Forma da resposta. Parecer escrito, com dispositivos, soluções de consulta e jurisprudência, e indicação expressa do grau de segurança de cada posição (CPC 25 / IAS 37). Resposta obrigatória: carga tributária total como percentual do preço de alienação.


Appendix B — The Day-1 sheet, eighteen fields
Page 1 is what GC says. Page 2 is what he says it from. Built by the machine and signed by a human in 3.5–5 hours from the flag.
Page 1 — the call
#
Field
1
Fund — denominação, CNPJ, class / subclass (and the subclass identifier where the informe is class-level).
2
Counterparties and status — administrador (situação: normal / liquidação extrajudicial / substituído, dated), gestor, custodiante, auditor, controlador, diretor responsável; every change in 24 months, dated.
3
Who can sell and under what authority — liquidante / administrador / gestor / assembleia / senior cotista — with the regulamento clause number; if a liquidation regime is running, the 180-day substitution deadline and its expiry date.
4
Informe face (latest), reference month, filing date, days late, restated or not.
5
PL; sênior / mezanino / subordinada split; subordination %; RESG_SOLIC outstanding.
6
THE INDICATIVE RANGE — R$X–Y, whole portfolio, one cash price, subject to verification — with cents on informe face alongside.
7
The exclusivity ask — 7–10 business days — and the three things needed on day 1, named now: (a) the position-level tape with CNPJ do sacado and CNPJ do cedente per line; (b) the termos de cessão and any aval / coobrigação schedules; (c) the registradora opt-in executed in VAZANTE's CNPJ plus the custodiante's last art. 38 report.
8
The three sentences that prove we have read the fund — the recompra fact with dates; the sacado fact with a name; the quota fact.
9
What we do NOT need — no report, no fee, no mandate, no ninety-day engagement. He is selling us an asset.


Page 2 — the evidence
#
Field
10
24-month chart strip — carteira; recompras + alienações ao cedente; 180+ bucket; PDD coverage; senior quota return; RESG_SOLIC.
11
Break diagnosis — t_peak, t_stop, which of conditions A–D fired and when, which of E–M confirmed, and the V1 / V2 / V3 vintage partition with face in each and where the freshest paper sits.
12
Top-25 sacados — CNPJ, face, % PL, situação cadastral, início de atividade, capital social, protests, courts, verdict; four-way split (alive / RJ / dead / shell) by face and by value.
13
Named cedentes and coobrigados — from a.11 / b.11, the lâmina, the regulamento, the rating report, the fund's own litigation — capital-social-to-face-owed, protests, RJ, avalistas identified.
14
Relatedness flags — shared sócios, shared addresses, shared gestor / custodiante / auditor / diretor with other known-broken funds.
15
Regulamento extracts — eligibility criteria; coobrigação / recompra clause; encargos; who may dispose of the carteira; assembly quorum for a sale.
16
Range decomposition, one line each — informe face → ledger → documented (with the lineage tier that set the prior) → named parcel → unnamed parcel → onward estimate → ÷ 1.20 with tax inside → less costs → indicative range.
17
Confidence — the width, its decomposition, and the ONE fact that would most narrow it (nearly always the position-level tape with cedente CNPJs).
18
Kill flags already visible — any of the four kill conditions already probable from public data.


Appendix C — Verification register and open items
What was fetched from a primary source and what was not, so that nothing in this document is relied on past its evidence.
Claim
Status
Source / the check that closes it
Lei 9.718 art. 14 VI forces Lucro Real on factoring; art. 14 VII on securitização de crédito (as amended by Lei 14.430 art. 35)
VERIFIED / wording GATED
Planalto; consolidated text truncated on fetch — obtain certified text
Decreto 4.524/2002 art. 10 §3 — receita bruta = face − cost for factoring
VERIFIED text; application GATED
Counsel; search CARF for assessments on NPL portfolio buyers
PN Cosit 5/2014 §32; SC Cosit 169/2018; SC Cosit 99/2023
VERIFIED
Receita; econeteditora
CARF 3101-004.842, 2 Jul 2026 — services element required for factoring; IOF cancelled
VERIFIED (administrative, single turma, not binding)
rotadajurisprudencia
Decreto 6.306 art. 3 §3 II, art. 4 p.ú., art. 5 II — IOF trigger and contribuinte; Decreto 12.466/2025 rates
VERIFIED; rate table on closing date GATED
Planalto; check on the closing date
LC 224/2025 presunção +10 points; LC 214/2025 arts. 182, 193 §5
VERIFIED; STF challenge status GATED
Planalto; Migalhas
Lei 8.981 art. 42 trava dos 30%
VERIFIED
Planalto
CC arts. 286–298 (esp. 288, 290, 291, 294, 295, 296, 298); arts. 417–420; 408 / 412; 225; 991
VERIFIED
Planalto / legjur
Cap on the art. 295 warranty enforceable against a professional buyer
GATED
Counsel's written view
Res. CVM 175 Anexo II arts. 15, 38, 42, 44 §3, 70, 72, 84, 86
VERIFIED in substance; art. 70 verbatim GATED
conteudo.cvm.gov.br; a first fetch returned an art. 73 list a second could not reproduce — disregarded. Obtain certified arts. 69–73
ICVM 489 art. 11 — provision on evidence of impairment
VERIFIED
CVM
Res. CVM 160 art. 8
GATED, and not relevant unless a strip is wrapped
CVM PDF timed out
Lei 6.024 art. 16 — liquidante needs prior BCB authorisation to alienate bens da massa
VERIFIED
Planalto
Lei 14.430 arts. 18, 29–31, 35
VERIFIED
Planalto
Lei 14.754/2023; Res. CMN 5.111/2023 — 15% at the cotista; entidade de investimento
VERIFIED; definitive-vs-antecipação for PF GATED; captive fund passing the test GATED
Counsel; candidate administrador in writing
STJ 4ª Turma 16 Dec 2025 — RJ does not suspend actions against coobrigados
VERIFIED
Earlier work
Duplicata escritural calendar — full regime January 2028
VERIFIED
Convenção BACEN Nov 2024 under Lei 13.775 / Decreto 10.769
Informe Mensal structure (Tabelas I–X; Tabela VIII 25 maiores sacados; a.11 / b.11 cedentes > 10% PL)
VERIFIED (Suplemento G); CSV headers GATED
Download one month, diff headers, freeze the mapping
CVM open data present and current (updated 7 Sep 2026)
VERIFIED listing; bulk download blocked from sandbox
Run from a Brazilian desk
Fund-versus-class filing of Tabela VIII
GATED (3× error if wrong)
Σ Valor / PL vs Σ %PL on 200 funds
CENPROT São Paulo detail; court aggregator coverage
GATED
Twenty known CNPJs through each
BRB / Tirreno facts (R$12.2bn; R$2.6bn provision 7 Jan 2026; Quadra expiry 6 Jul; R$370m CCBs 28 Aug)
VERIFIED
Press and BCB
Trustee / Banvox 63 funds R$14.1bn liquidated 3 Sep 2026; Reag 110 funds 15 Jan 2026; Master 53 funds, 52 adrift; 46 dark FIDCs July 2026
VERIFIED
BCB decrees; NeoFeed; ANBIMA
Fictor Invest facts; Electra RJ 27 May 2026 (0009800-26.2026.8.16.0194); Casas Bahia FIDCs; JiveMauá, IOX, Recovery, Möbius, Paramis figures
VERIFIED
Fundos.NET; TJPR; NeoFeed 24 Jun 2026; Bloomberg Línea 26 Aug 2026; Capital Aberto Oct 2025
CDI 13.90%
VERIFIED
B3 / BCB, 10 Sep 2026
Registradoras will contract with a two-person Ltda
GATED
Condition 2
Buyers will sign binding pre-asset take-outs
GATED
Condition 3
Seller reservation as a share of L (62% deep-gap median); the funnel rates; the lastro-gap prior (n = 1); Claims survival factors; retrade rate; assembly-cover share (45%)
ASSUMPTION
Ten real approaches; Deal 0; Deal 1
Every campaign figure in Part 7
MODEL
P5_model.py, 2,500 paths; tax sensitivity re-run 1,500 paths


End of document. Companion: "VAZANTE — Pacote de Compradores" (calibration pack, three standing buy boxes, openers, Deal 0 protocol). Working files: /v3/P1–P6, P5_model.py.

FORENSIC ORACLE LAYER
VAZANTE transactions may involve portfolios affected by fictitious receivables, duplicate assignments, undisclosed related parties, circular funding, cedente-funded collections, missing lastro, invalid title, document manipulation, hidden substitutions/recompras and other serious data-integrity problems.
Therefore portfolio analysis is not merely a credit-scoring exercise.
The system must independently test the factual assertions embedded in the portfolio before those assertions may support a VAZANTE purchase price.
The objective is NOT to declare that a person or company committed fraud.
The objective is to identify objective evidence, contradictions, missing evidence and related-party patterns that determine whether an asset may safely carry value.
FIVE EVIDENCE DIMENSIONS
Maintain separate evidence states for:
E — EXISTENCE
Does the underlying invoice/credit/document actually exist as represented?
T — TITLE / EXCLUSIVITY
Does the seller/fund appear to own the right and is there evidence of prior or competing assignment, pledge, replacement or repurchase?
C — CASH
Is historical payment supported by genuine third-party debtor cash, rather than cedente support, related-party funding or unmatched flows?
D — DEBTOR / COMMERCIAL REALITY
Did the debtor exist and operate, and is the claimed commercial relationship economically plausible?
R — RECOURSE
If debtor value fails, is there evidenced recourse against a cedente, guarantor, co-obligor or other party?
Never combine these into one grade until all five have been separately computed.
FUND-LEVEL PRE-FORENSICS
Before analyzing seller-supplied position data, reconstruct at least 24 months of available public fund history.
Where available, ingest:
CVM FIDC Informe Mensal;
CVM fund/class registration data;
relevant event filings;
financial statements and balancetes;
assembly minutes;
administrator, manager, custodian and auditor changes;
public regulator correspondence/documents.
Calculate and preserve by month:
portfolio face;
overdue buckets;
defaults;
provisions;
acquisitions;
write-offs;
recompras;
substituições;
recompras + substituições as percentage of portfolio;
churn-to-default;
cedente concentration;
subordinated coverage;
senior quota return and return variance;
missing/re-filed reporting periods;
relevant service-provider changes.
Do not classify high recompras alone as misconduct.
Promote a fund-level anomaly only through combinations of independent signals, including where relevant:
high recompras/substituições;
high churn-to-default;
suppressed ageing/default migration;
coverage gaps;
unusually flat senior-quota performance;
material filing gaps;
provider replacement or regulatory event.
CROSS-FUND CONTAGION GRAPH
Maintain a permanent graph linking:
fund
cedente
sacado
administrator
manager
custodian
auditor
collection agent
shareholder/administrator
address
other supported relationship attributes.
Use it to identify concentration of the same parties across previously problematic vehicles.
A relationship is a signal, not proof of wrongdoing.
100% STRUCTURAL SWEEP
Run deterministic offline checks across every portfolio position before paid or credentialed external checks.
Include where applicable:
CPF/CNPJ checksum;
NF-e 44-digit access-key validation;
NF-e check digit;
emitter identity encoded in NF-e key;
emitter versus cedente identity;
issue date;
assignment date;
acquisition date;
maturity date;
impossible date sequences;
exact duplicate document IDs;
exact duplicate NF-e keys;
duplicate series/document numbers;
same NF-e supporting multiple claimed receivables;
exact and fuzzy duplicated receivables;
repeated amount/date/debtor combinations;
round-number clustering;
terminal-digit clustering;
unnatural sequential numbering;
negative balances;
face/balance inconsistencies;
acquisition-price anomalies;
positions paid before assignment;
unexplained replacements/recompras;
internally inconsistent debtor/cedente identifiers.
Never silently delete duplicates.
Flag them and quantify affected face.
GLOBAL ASSET FINGERPRINT DATABASE
Every analyzed position must generate a persistent fingerprint.
Use combinations of:
NF-e key;
normalized document identifier;
emitter/cedente CNPJ root;
debtor/sacado CNPJ root;
issue date;
due date;
original face;
normalized series/document number.
Before accepting a position as unique, compare it against every prior VAZANTE portfolio.
Produce:
EXACT_CROSS_PORTFOLIO_MATCH
PROBABLE_CROSS_PORTFOLIO_MATCH
POSSIBLE_MATCH
NO_MATCH
A cross-portfolio match is a title/anomaly finding and requires adjudication; it is not automatically proof of duplicate assignment.
NF-e / DOCUMENT EXISTENCE
For each material NF-e-backed position, where authorized access is available:
validate the seller/custodian XML structurally;
verify its digital signature;
extract issuer, recipient, value, issue date and access key;
retrieve/validate the corresponding official authorization/protocol information;
inspect authorization status and cancellation/denial where applicable;
compare protocol/access-key data to the supplied XML;
validate the official digest/integrity value where supported;
verify that the economic value represented in the portfolio is consistent with the underlying fiscal document;
preserve the raw official response and seller XML as evidence objects.
A valid NF-e key alone does not prove that the portfolio's stated receivable amount is correct.
Do not rely on DANFE alone where XML is expected.
Any cryptographic/digest mismatch must be HUMAN_ADJUDICATION before becoming a hard-negative classification.
TITLE / REGISTRADORA
Where the asset and authorization permit:
query the relevant authorized registration infrastructure for evidence of:
current holder;
registration;
assignment;
encumbrance;
competing interests;
duplicate/overlapping registration;
replacement;
repurchase;
historical title events.
Do not interpret absence of registration for legacy paper as proof that the asset does not exist.
Use:
TITLE_CONFIRMED
TITLE_PARTIAL
TITLE_CONFLICT
TITLE_UNREGISTERED_LEGACY
TITLE_UNVERIFIED
ACCESS_UNAVAILABLE
Material TITLE_CONFLICT findings must be priced at zero until resolved or explicitly accepted by the specific buyer.
CASH RECONSTRUCTION
Require seller/fund bank statements and CNAB retorno files for the longest practical historical period, target 24 months.
Never use a fund-reported collection figure without reconstructing payer identity where data permits.
For every incoming payment:
identify:
amount;
date;
bank reference;
payer CPF/CNPJ where available;
payer corporate-group root;
position/document matched;
recipient account;
associated cedente;
associated sacado.
Classify each payment as:
SACADO_THIRD_PARTY
CEDENTE_GROUP
RELATED_PARTY
RECOMPRA
UNMATCHED
UNKNOWN
Create by position, sacado and cedente:
gross reported collections;
verified third-party debtor cash;
cedente-group funded cash;
related-party cash;
unmatched cash;
third-party cash ratio;
cedente-support ratio;
months since last genuine debtor payment.
Historical recovery assumptions used for valuation must be built from genuine third-party cash only unless an alternative classification is explicitly supported.
Build static-pool/vintage cash triangles by cedente using third-party cash.
ENTITY REALITY / RELATED-PARTY GRAPH
For all material cedentes, sacados, guarantors and relevant owners:
obtain legally accessible/current data regarding:
CNPJ situation;
registration/opening date;
CNAE;
registered address;
capital social;
QSA;
corporate-group relationships;
court/RJ status;
protests where an authorized source is available;
bureau information where contracted;
sanctions/integrity data where appropriate.
Test:
company existed before claimed commercial activity;
debtor activity is plausibly consistent with transaction type;
invoice size relative to basic company characteristics;
shared owners between debtor and cedente;
shared addresses;
supported shared management/contact/accountant signals;
clusters of newly formed companies;
unusual concentration among connected counterparties.
CNAE mismatch, low capital or common address may be risk features.
They are not standalone hard negatives.
Require multiple independent relationship signals before material escalation.
JUDICIAL / INSOLVENCY
Search legally accessible public/contracted judicial sources for material:
sacados;
cedentes;
guarantors;
co-obligors;
relevant shareholders.
Capture facts including:
judicial-recovery filing;
bankruptcy;
execution proceedings;
material collection proceedings;
proceedings concerning the underlying contract/receivable;
disputes over assignment/title;
material recent procedural events.
Store case number, court, filing date, latest relevant movement and evidence pull.
The system identifies procedural facts.
Legal consequences are LEGAL_REVIEW.
RECOURSE ENGINE
Analyze seller-supplied assignment/master agreements and guarantee documents.
Extract, without independently giving legal opinions:
recompra clauses;
substitution clauses;
co-obligation language;
existence representations;
indemnities;
guarantees;
aval;
fiança;
confissão de dívida;
guarantor identity;
triggering events;
cure periods;
relevant dates.
Link observed factual events to contract provisions.
Example:
FACT:
R$X of associated NF-e is shown as cancelled.
DOCUMENT:
Clause Y refers to mandatory repurchase upon cancellation.
OUTPUT:
POTENTIAL_RECOURSE_EVENT — R$X face — LEGAL_REVIEW.
Do not describe a contractual remedy as enforceable unless counsel-approved rules expressly permit that conclusion.
PROTEST / BUREAU / INTEGRITY
Where contracted and lawful, integrate protest and commercial-credit data.
Treat these primarily as:
current solvency indicators;
cedente/guarantor quality indicators;
buyer-eligibility inputs;
recourse-value inputs.
They do not independently establish that a receivable is fictitious.
Where appropriate, query public corporate-sanction databases and flag material findings.
COUNTERPARTY CONFIRMATION
Where expressly authorized by the seller/fund and approved operationally:
record debtor responses using only:
RECOGNIZED
RECOGNIZED_WITH_DIFFERENCE
ALREADY_PAID
NOT_RECOGNIZED
UNDELIVERABLE
NO_RESPONSE
NO_RESPONSE is not positive evidence.
Never convert silence into confirmation unless a specific counsel-approved rule applicable to that exact procedure is encoded in the legal ruleset.
ORACLE-RESULT STATES
Every external query must return an explicit technical/evidence state.
At minimum:
FOUND_POSITIVE
FOUND_NEGATIVE
NO_RECORD
SOURCE_UNAVAILABLE
ACCESS_DENIED
RATE_LIMITED
INVALID_QUERY
NOT_APPLICABLE
NOT_TESTABLE
PENDING_HUMAN_REVIEW
SOURCE_UNAVAILABLE, ACCESS_DENIED, RATE_LIMITED and technical failure must never be interpreted as NO_RECORD.
NO_RECORD must never automatically be interpreted as a substantive negative or positive unless that oracle's documented semantics support it.
EVIDENCE WRAPPER
All external calls must use the common pull() wrapper.
Store for every call:
pull_id;
deal_id;
position/entity ID;
provider/source;
product/endpoint;
parameters;
authorization/credential identity;
request timestamp;
response timestamp;
response/result status;
raw response;
SHA-256 of raw response;
parser version;
parsed facts;
retry history.
No material derived fact may enter underwriting without an evidence reference or an explicit ASSUMPTION status.
CHECK COVERAGE
TIER 0:
100% of portfolio — offline structural/reconciliation checks.
TIER 1:
100% of economically relevant entities — corporate identity, relationship and low-cost public checks where lawful and economical.
TIER 2:
Deep oracle/document testing on:
positions comprising at least the top 80% of face;
every position supporting a firm buyer take-out;
every position above the configured materiality threshold;
every anomaly cluster regardless of size.
TIER 3:
Human adjudication for:
cryptographic/XML mismatch;
material title conflict;
suspected cross-portfolio duplicate;
large related-party cluster;
material cash-source anomaly;
material recourse event;
any finding capable of moving the seller bid by more than the configured tolerance.
UNDERWRITING IMPACT
Every finding must state:
affected positions;
affected face;
evidence dimension E/T/C/D/R;
evidence status;
severity;
source references;
whether it is objective or inferential;
buyer(s) affected;
eligibility impact;
pricing/haircut impact;
whether current firm take-outs remain valid;
seller cure/document required;
human/legal review required.
Never output a generic "fraud score" as the primary decision variable.
The system exists to produce a defensible purchase price from individually supported facts.
FINAL FORENSIC BRIDGE
Before buyer routing and purchase pricing, output:
SELLER-REPORTED FACE
→ CANONICAL FACE
→ EXISTENCE-SUPPORTED FACE
→ TITLE-SUPPORTED FACE
→ THIRD-PARTY-CASH-SUPPORTED FACE
→ BUYER-ELIGIBLE FACE
→ FIRM-TAKEOUT FACE
→ ZERO / UNRESOLVED FACE
Reconcile every bridge numerically.
Then run buyer routing and VAZANTE maximum-bid calculations.
No unverified asset may enter LOCKED_PROCEEDS merely because its inclusion is necessary for the transaction to pass.

THESE CAN CHNAGE NOTTHING HERE IS PERMINT THIS THE WORKING IDEA OF THE BUSSINESS KISS VAZANTE is a short-duration principal trading desk for broken credit portfolios.

It does four things:

Finds an ugly portfolio that is hard to trust or value.

Uses the Oracle to figure out what is actually there — existence, title, cash history, related parties, duplicates, recourse, legal flags.

Matches the good pieces to buyers using buyer-specific buy boxes and live pricing.

Buys the whole portfolio from the seller at one cash price, then resells the pieces to buyers at a higher total value and keeps the spread.

That is the business.

Very simply:

Seller has one messy portfolio.
VAZANTE understands it better than anyone else.
Buyers value different pieces differently.
VAZANTE buys the whole thing wholesale and sells the pieces retail.
The difference is VAZANTE’s profit.

The key rule is:

Never give the seller a firm bid until enough onward buyer proceeds are already locked to make the trade profitable.

So if VAZANTE can sell the pieces for R$10m, total costs/reserves are R$0.5m, and it wants at least R$1.5m locked profit, then it should pay no more than about R$8m.

The seller sees:

“VAZANTE will buy the entire portfolio for R$8m cash.”

The buyers see:

“VAZANTE has R$X of exactly the asset you buy, already verified and organized.”

VAZANTE is not a broker, advisor, collector, or long-term distressed fund.

It is a finite 10–30 deal trading operation designed to make roughly R$1.5m–R$4m+ per good trade, get in, get out quickly, and stop when the opportunity set is gone.

The three things that make it work are:

Oracle = tells you what the portfolio really contains.
Buyer buy boxes = tell you who will buy each part and at what price.
Discipline = only buy when the exit is substantially known before the entry.

That’s VAZANTE.>>
