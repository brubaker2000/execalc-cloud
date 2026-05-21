from __future__ import annotations

import logging
import re
import uuid
from datetime import UTC, datetime
from typing import List, Optional, Tuple

from src.service.qualitative_capture.models import AtomicNugget, ConversationEvent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Signal patterns — detect which claim type a sentence expresses.
# Reuses the vocabulary from the GAQP ingress gate patterns in detection mode
# (not rejection mode — we are matching signal, not enforcing structure).
# ---------------------------------------------------------------------------

_CLAIM_SIGNALS: List[Tuple[str, List[str]]] = [
    ("doctrine", [
        "we will", "we do not", "we always", "we never", "non-negotiable",
        "our approach is", "we are committed", "standing rule", "organizational commitment",
    ]),
    ("principle", [
        "should always", "ought to", "must always", "never ", "as a principle",
        "governing rule", "our standard", "we require", "we mandate",
    ]),
    ("risk", [
        "risk ", "danger ", "exposure to", "vulnerability", "threat of",
        "downside risk", "we are exposed", "risk that",
    ]),
    ("opportunity", [
        "opportunity to", "potential upside", "we could", "untapped",
        "if we", "growth potential", "opening for",
    ]),
    ("objective", [
        "our goal", "our target", "we aim to", "we seek to", "our objective",
        "we want to achieve", "strategic priority", "we are trying to",
    ]),
    ("causal_claim", [
        "because ", "leads to", "lead to", "results in", "result in",
        "drives ", "causes ", "caused by", "due to", "as a result",
        "therefore ", "consequently", "which means",
    ]),
    ("tradeoff", [
        " versus ", " vs. ", " vs ", "at the cost of", "trade-off", "tradeoff",
        "in exchange for", "either ", "sacrifice ", "on the other hand",
    ]),
    ("heuristic", [
        "rule of thumb", "generally ", "typically when", "in practice",
        "as a pattern", "we tend to", "historically",
    ]),
    ("observation", [
        "i notice", "we notice", "it appears", "data shows", "the pattern",
        "i see that", "we see that", "evidence suggests", "we have observed",
    ]),
    ("threshold_condition", [
        "if ", "when ", "once ", "above ", "below ", "exceeds",
        "falls below", "triggers ", "crosses ",
    ]),
    ("declaration_of_value", [
        "we believe", "we value", "what matters", "our conviction",
        "at our core", "we stand for", "we care about",
    ]),
    ("constraint", [
        "must not", "cannot ", "limited to", " cap ", "hard limit",
        "no more than", "maximum ", "minimum ", "not exceed",
    ]),
]

_MIN_SENTENCE_LENGTH = 30
_EPHEMERAL_MARKERS = ("today", "yesterday", "this week", "right now", "as of now")


def _detect_claim_type(text: str) -> Optional[str]:
    lower = text.lower()
    for claim_type, signals in _CLAIM_SIGNALS:
        if any(s in lower for s in signals):
            return claim_type
    return None


def _detect_polarity(text: str) -> str:
    lower = text.lower()
    negative_signals = ("risk", "danger", "threat", "weakness", "cannot", "must not", "fail")
    positive_signals = ("opportunity", "growth", "advantage", "strength", "achieve", "succeed")
    cautionary_signals = ("however", "but ", "caution", "warning", "concern", "careful")
    n = sum(1 for s in negative_signals if s in lower)
    p = sum(1 for s in positive_signals if s in lower)
    c = sum(1 for s in cautionary_signals if s in lower)
    if n > p and n > c:
        return "negative"
    if p > n and p > c:
        return "positive"
    if c > 0:
        return "cautionary"
    return "neutral"


def _detect_durability(text: str) -> str:
    lower = text.lower()
    if any(m in lower for m in _EPHEMERAL_MARKERS):
        return "ephemeral"
    ephemeral_patterns = ("q1", "q2", "q3", "q4", "this year", "next year", "this quarter")
    if any(p in lower for p in ephemeral_patterns):
        return "medium_term"
    return "enduring"


def _split_sentences(text: str) -> List[str]:
    raw = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in raw if len(s.strip()) >= _MIN_SENTENCE_LENGTH]


def _is_admission_eligible(text: str) -> bool:
    lower = text.lower()
    boilerplate = ("n/a", "not applicable", "none identified", "see above", "no major")
    if any(lower.startswith(b) for b in boilerplate):
        return False
    if text.strip().endswith("?"):
        return False
    return True


def deconstruct_event(
    event: ConversationEvent,
    *,
    domain: str = "strategy",
) -> List[AtomicNugget]:
    """
    Extract GAQP-classified atomic nuggets from a conversation event.

    V1 uses rule-based pattern matching. Each sentence that carries a
    detectable claim signal and passes admission tests becomes a nugget.

    Returns an empty list if no eligible claims are found — callers should
    treat empty deconstruction as a normal outcome.
    """
    sentences = _split_sentences(event.message_text)
    nuggets: List[AtomicNugget] = []

    for sentence in sentences:
        if not _is_admission_eligible(sentence):
            continue

        claim_type = _detect_claim_type(sentence)
        if claim_type is None:
            continue

        polarity = _detect_polarity(sentence)
        durability = _detect_durability(sentence)
        is_rail_candidate = claim_type in ("doctrine", "principle", "risk", "opportunity", "objective")

        nugget = AtomicNugget(
            nugget_id=uuid.uuid4().hex,
            tenant_id=event.tenant_id,
            session_id=event.session_id,
            source_event_id=event.event_id,
            claim_text=sentence,
            claim_type=claim_type,
            domain=domain,
            confidence_level="seed",
            confidence_score=0.50,
            provenance_source=f"session:{event.session_id}",
            provenance_author=event.user_id,
            activation_scope="tenant_specific",
            activation_triggers=[f"session:{event.session_id}", f"claim_type:{claim_type}"],
            polarity=polarity,
            durability_class=durability,
            evidence_status="argued",
            freshness_class="timeless" if durability == "enduring" else "date_sensitive",
            selection_method="machine_extracted",
            generation_depth=1,
            rail_candidate=is_rail_candidate,
            created_at=datetime.now(UTC),
        )
        nuggets.append(nugget)

    if nuggets:
        logger.debug(
            "QCR deconstruct: event=%s tenant=%s produced %d nuggets",
            event.event_id, event.tenant_id, len(nuggets),
        )

    return nuggets
