"""Vocabulary of the Oracle (docs/03_forensic_oracle_layer.md). The five dimensions are never collapsed into one grade."""
from __future__ import annotations

from enum import Enum


class Dimension(str, Enum):
    E = "E"  # existence — does the invoice / title exist as a fiscal document at this value?
    T = "T"  # title / exclusivity — does the seller own the right and can he transfer it?
    C = "C"  # cash — who actually sent the money over 24 months?
    D = "D"  # debtor / commercial reality
    R = "R"  # recourse — against whom, and is that party collectable?


class ExistenceState(str, Enum):
    CONFIRMED = "E_CONFIRMED"          # NF-e authorised at SEFAZ and digVal matched against the delivered XML
    PARTIAL = "E_PARTIAL"              # key structurally valid; XML not delivered or status not consulted
    WEAK = "E_WEAK"                    # seller spreadsheet only
    HARD_NEGATIVE = "E_HARD_NEGATIVE"  # cancelled / denied / adjudicated digest mismatch / nonexistent
    NOT_TESTABLE = "E_NOT_TESTABLE"    # the named missing item makes it untestable


class TitleState(str, Enum):
    TITLE_CONFIRMED = "TITLE_CONFIRMED"
    TITLE_PARTIAL = "TITLE_PARTIAL"
    TITLE_CONFLICT = "TITLE_CONFLICT"  # priced at zero until resolved or expressly accepted by the specific buyer
    TITLE_UNREGISTERED_LEGACY = "TITLE_UNREGISTERED_LEGACY"  # absence of registration is not proof of nonexistence
    TITLE_UNVERIFIED = "TITLE_UNVERIFIED"
    ACCESS_UNAVAILABLE = "ACCESS_UNAVAILABLE"


class CashClass(str, Enum):
    SACADO_THIRD_PARTY = "SACADO_THIRD_PARTY"
    CEDENTE_GROUP = "CEDENTE_GROUP"
    RELATED_PARTY = "RELATED_PARTY"
    RECOMPRA = "RECOMPRA"
    UNMATCHED = "UNMATCHED"
    UNKNOWN = "UNKNOWN"


class DebtorResponse(str, Enum):
    RECOGNIZED = "RECOGNIZED"
    RECOGNIZED_WITH_DIFFERENCE = "RECOGNIZED_WITH_DIFFERENCE"
    ALREADY_PAID = "ALREADY_PAID"
    NOT_RECOGNIZED = "NOT_RECOGNIZED"
    UNDELIVERABLE = "UNDELIVERABLE"
    NO_RESPONSE = "NO_RESPONSE"  # never positive evidence


class OracleResultState(str, Enum):
    FOUND_POSITIVE = "FOUND_POSITIVE"
    FOUND_NEGATIVE = "FOUND_NEGATIVE"
    NO_RECORD = "NO_RECORD"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    ACCESS_DENIED = "ACCESS_DENIED"
    RATE_LIMITED = "RATE_LIMITED"
    INVALID_QUERY = "INVALID_QUERY"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_TESTABLE = "NOT_TESTABLE"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"


# Technical failures are never read as NO_RECORD, and NO_RECORD is never a substantive answer on its own.
FAILURE_STATES = frozenset(
    {
        OracleResultState.SOURCE_UNAVAILABLE,
        OracleResultState.ACCESS_DENIED,
        OracleResultState.RATE_LIMITED,
        OracleResultState.INVALID_QUERY,
    }
)


class CrossPortfolioMatch(str, Enum):
    EXACT_CROSS_PORTFOLIO_MATCH = "EXACT_CROSS_PORTFOLIO_MATCH"
    PROBABLE_CROSS_PORTFOLIO_MATCH = "PROBABLE_CROSS_PORTFOLIO_MATCH"
    POSSIBLE_MATCH = "POSSIBLE_MATCH"
    NO_MATCH = "NO_MATCH"


class PriceStatus(str, Enum):
    """Only FIRM enters locked proceeds. A grid is a price list, not a bid."""

    FIRM = "FIRM"
    RECENT_OBSERVED = "RECENT_OBSERVED"
    GRID = "GRID"
    HISTORICAL = "HISTORICAL"
    ESTIMATE = "ESTIMATE"


class Confidence(str, Enum):
    CONFIRMED = "CONFIRMED"  # the buyer said it
    OBSERVED = "OBSERVED"    # derived from actual transactions
    INFERRED = "INFERRED"    # deduced from examples or emails
    UNKNOWN = "UNKNOWN"


class EvidenceTag(str, Enum):
    """The five tags every load-bearing figure in the business case carries. Carry them into code and output."""

    VERIFIED = "VERIFIED"      # primary source fetched
    MODEL = "MODEL"            # an output of the arithmetic
    ASSUMPTION = "ASSUMPTION"  # a parameter we set
    GATED = "GATED"            # cannot be settled from a desk; the condition that settles it is named
    DECISION = "DECISION"      # a choice, not a finding


class Exit(str, Enum):
    PREMIUM = "PREMIUM"
    CLAIMS = "CLAIMS"
    RESIDUAL = "RESIDUAL"
    ZERO = "ZERO"


# Fixed ranking of evidence. Nothing from the bottom three tiers ever raises a grade; it can only flag where to look.
TRUTH_HIERARCHY = (
    "cryptographic_or_official",  # SEFAZ digVal, registradora, Receita
    "bank_originated",            # CNAB
    "registry",                   # RTD, CENPROT, courts
    "executed_documents",         # termos, avais
    "seller_systems",
    "seller_spreadsheets",
    "verbal",
)
