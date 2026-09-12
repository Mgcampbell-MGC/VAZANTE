# The tape: exactly what we ask for

One page. This is what goes to a gestora the moment they say yes, so that defining the file does not cost a week.
Send it as an attachment to the NDA, not as a negotiation.

**Format.** CSV or XLSX, one row per position, UTF-8 or Latin-1, any column order, any column names. We map it.
Do not clean it, do not summarise it, do not remove anything. A messy complete file beats a tidy partial one.

**Period.** Position-level as at the last closed month, plus 24 months of cash history if it exists.

---

## Tier 1: without these we cannot start

| Field | Why |
|---|---|
| Position identifier | To reconcile and to speak about a line |
| CNPJ do sacado | The debtor. Without it there is no Slice 2 and no debtor check at all |
| CNPJ do cedente | The originator. Without it there is no Slice 3 and no recourse |
| Valor de face | The number everything is a percentage of |
| Valor contabil / provisionado | What the fund carries it at, so we can see the gap |
| Data de emissao | Vintage |
| Data de vencimento | The ageing band, which is the carve |
| Situacao (a vencer / vencido / pago / recomprado / substituido) | Routes the position to its slice |

## Tier 2: each one moves the price, so send whatever exists

| Field | What it unlocks |
|---|---|
| Chave de acesso da NF-e, 44 digits | Existence. We validate the key and the check digit offline, free, in seconds |
| Numero da duplicata and serie | Duplicate detection across this fund and every book we have seen |
| Data da cessao ao fundo | Whether the paper was assigned before or after it went bad |
| Valor pago and data do pagamento | Real cash, the only honest recovery evidence |
| Indicador de coobrigacao or recompra | Slice 3. Which positions the originator guaranteed |
| Historico de recompras and substituicoes | The thing the fund alone knows and the informe cannot show |
| Protesto / acao judicial flags | Slice 4 |

## Tier 3: send if it is one export away

Retorno CNAB for 24 months, with the payer identified. The XML of the NF-e for the largest positions. The termos
de cessao and any aval or confissao de divida. The last two demonstracoes contabeis with the auditor's parecer.

---

## What we do with it, and how fast

**Hour 1.** Reconcile the tape to the fund's own CVM informe. Sum of face against reported carteira, sum of
provision against reported provision, ageing bands against Tabelas V and VI. A tape that does not reconcile to
the fund's own regulatory filing is the single most important thing we can learn, and it is free.

**Hours 2 to 4.** Structural sweep on 100% of positions, offline and at no cost: CPF and CNPJ check digits, NF-e
key validation, duplicate detection within the fund and against every book we hold, impossible date sequences,
positions paid before they were assigned, round-number and terminal-digit clustering.

**Hours 4 to 8.** Resolve every distinct sacado and cedente through the Receita. Alive, dead, inapta, in judicial
recovery, capital, shared addresses and shared partners. This is what turns Slice 2 and Slice 3 from theory into
a list of companies with balance sheets.

**Day 2.** The carve: every position routed to the buyer who wants that piece, with what each slice is worth.

**Day 3.** A written answer to the one question that decides everything: is the not-yet-due block real.

## What we never ask for and never give

We do not ask for the names of your cotistas. We do not ask you to sign anything beyond the NDA. We do not
produce a laudo, a parecer or an auditoria, and we do not use those words. We charge nothing for any of the above.
