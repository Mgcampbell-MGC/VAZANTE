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
