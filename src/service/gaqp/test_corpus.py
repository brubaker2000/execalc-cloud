from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from unittest.mock import MagicMock, call, patch

import pytest

from src.service.gaqp.corpus import (
    InsertSummary,
    get_claim,
    insert_claim,
    insert_claims,
    list_claims,
    list_claims_by_envelope,
)
from src.service.gaqp.models import (
    CONFIDENCE_SCORE,
    ClaimProvenance,
    CorroborationProfile,
    GAQPClaim,
    compute_fingerprint,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_claim(
    *,
    tenant_id: str = "tenant_001",
    envelope_id: str = "env_001",
    claim_type: str = "tradeoff",
    content: str = "Under a payroll reduction mandate, cost-controlled flexibility outweighs marginal veteran spend.",
    admission_status: str = "admitted",
    corpus_scope: str = "tenant",
) -> GAQPClaim:
    fp = compute_fingerprint(
        tenant_id=tenant_id,
        source_envelope_id=envelope_id,
        claim_type=claim_type,
        content=content,
        activation_scope="situational",
    )
    return GAQPClaim(
        claim_id=uuid.uuid4().hex,
        tenant_id=tenant_id,
        source_envelope_id=envelope_id,
        claim_type=claim_type,  # type: ignore[arg-type]
        domain="strategy",
        content=content,
        confidence_level="seed",
        confidence_score=CONFIDENCE_SCORE["seed"],
        admission_status=admission_status,  # type: ignore[arg-type]
        corpus_scope=corpus_scope,  # type: ignore[arg-type]
        extraction_method="direct_field",
        provenance=ClaimProvenance(
            source_kind="decision_artifact",
            source_ref=envelope_id,
            actor_id="user_001",
            envelope_id=envelope_id,
            origin_surface="extraction_pipeline",
        ),
        activation_scope="situational",
        activation_triggers=["tradeoff_analysis"],
        corroboration_profile=CorroborationProfile(),
        fingerprint=fp,
    )


def _mock_conn(rowcount: int = 1):
    """Build a mock psycopg2 connection with cursor context manager support."""
    cur = MagicMock()
    cur.rowcount = rowcount
    cur.fetchone.return_value = None
    cur.fetchall.return_value = []

    conn = MagicMock()
    conn.__enter__ = lambda s: s
    conn.__exit__ = MagicMock(return_value=False)
    conn.cursor.return_value.__enter__ = lambda s: cur
    conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return conn, cur


# ---------------------------------------------------------------------------
# insert_claim
# ---------------------------------------------------------------------------

class TestInsertClaim:
    def test_admitted_claim_inserted(self):
        claim = _make_claim()
        conn, cur = _mock_conn(rowcount=1)
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            result = insert_claim(claim)
        assert result is True
        cur.execute.assert_called_once()

    def test_returns_false_when_duplicate(self):
        claim = _make_claim()
        conn, cur = _mock_conn(rowcount=0)
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            result = insert_claim(claim)
        assert result is False

    def test_non_admitted_not_inserted(self):
        claim = _make_claim(admission_status="rejected")
        conn, cur = _mock_conn()
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            result = insert_claim(claim)
        assert result is False
        cur.execute.assert_not_called()

    def test_needs_review_not_inserted(self):
        claim = _make_claim(admission_status="needs_review")
        conn, cur = _mock_conn()
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            result = insert_claim(claim)
        assert result is False
        cur.execute.assert_not_called()

    def test_connection_closed_after_insert(self):
        claim = _make_claim()
        conn, _ = _mock_conn()
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            insert_claim(claim)
        conn.close.assert_called_once()


# ---------------------------------------------------------------------------
# insert_claims
# ---------------------------------------------------------------------------

class TestInsertClaims:
    def test_empty_list_returns_zero_summary(self):
        summary = InsertSummary()
        with patch("src.service.gaqp.corpus.get_conn"):
            result = insert_claims([])
        assert result.inserted == 0
        assert result.skipped == 0
        assert result.failed == 0

    def test_all_non_admitted_skipped_before_db(self):
        claims = [
            _make_claim(admission_status="rejected"),
            _make_claim(admission_status="needs_review"),
        ]
        with patch("src.service.gaqp.corpus.get_conn") as mock_conn:
            result = insert_claims(claims)
        mock_conn.assert_not_called()
        assert result.inserted == 0

    def test_counts_inserted_and_skipped(self):
        admitted = _make_claim(admission_status="admitted")
        duplicate = _make_claim(
            admission_status="admitted",
            content="A different claim about capital allocation and constraint management.",
        )

        conn, cur = _mock_conn(rowcount=1)
        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            cur.rowcount = 1 if call_count[0] == 1 else 0

        cur.execute.side_effect = side_effect

        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            summary = insert_claims([admitted, duplicate])

        assert summary.inserted == 1
        assert summary.skipped == 1
        assert summary.failed == 0

    def test_connection_closed_after_batch(self):
        claims = [_make_claim()]
        conn, _ = _mock_conn()
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            insert_claims(claims)
        conn.close.assert_called_once()

    def test_failed_count_on_exception(self):
        claim = _make_claim()
        conn, cur = _mock_conn()
        cur.execute.side_effect = Exception("DB error")
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn), \
             patch("src.service.gaqp.corpus._load_psycopg2_json", return_value=lambda x: x):
            summary = insert_claims([claim])
        assert summary.failed == 1
        assert summary.inserted == 0


# ---------------------------------------------------------------------------
# get_claim
# ---------------------------------------------------------------------------

class TestGetClaim:
    def _make_db_row(self, claim: GAQPClaim):
        return (
            claim.claim_id, claim.tenant_id, claim.source_envelope_id,
            claim.claim_type, claim.domain, claim.content,
            claim.confidence_level, claim.confidence_score,
            claim.admission_status, claim.corpus_scope,
            claim.extraction_method, claim.provenance.to_dict(),
            claim.activation_scope, claim.activation_triggers,
            claim.corroboration_profile.to_dict(),
            claim.contradiction_refs, claim.support_refs,
            claim.fingerprint, claim.schema_version,
            datetime.now(UTC), datetime.now(UTC),
        )

    def test_returns_dict_when_found(self):
        claim = _make_claim()
        conn, cur = _mock_conn()
        cur.fetchone.return_value = self._make_db_row(claim)
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            result = get_claim(claim_id=claim.claim_id, tenant_id=claim.tenant_id)
        assert result is not None
        assert result["claim_id"] == claim.claim_id
        assert result["tenant_id"] == claim.tenant_id

    def test_returns_none_when_not_found(self):
        conn, cur = _mock_conn()
        cur.fetchone.return_value = None
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            result = get_claim(claim_id="nonexistent", tenant_id="tenant_001")
        assert result is None

    def test_connection_closed_after_fetch(self):
        conn, cur = _mock_conn()
        cur.fetchone.return_value = None
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            get_claim(claim_id="x", tenant_id="t")
        conn.close.assert_called_once()


# ---------------------------------------------------------------------------
# list_claims
# ---------------------------------------------------------------------------

class TestListClaims:
    def test_empty_result(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            result = list_claims(tenant_id="tenant_001")
        assert result == []

    def test_limit_clamped_to_200(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            list_claims(tenant_id="t1", limit=999)
        sql_call = cur.execute.call_args[0][0]
        params = cur.execute.call_args[0][1]
        assert params[-1] == 200

    def test_limit_minimum_1(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            list_claims(tenant_id="t1", limit=0)
        params = cur.execute.call_args[0][1]
        assert params[-1] == 1

    def test_claim_type_filter_added(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            list_claims(tenant_id="t1", claim_type="tradeoff")
        sql = cur.execute.call_args[0][0]
        assert "claim_type" in sql

    def test_connection_closed(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            list_claims(tenant_id="t1")
        conn.close.assert_called_once()


# ---------------------------------------------------------------------------
# list_claims_by_envelope
# ---------------------------------------------------------------------------

class TestListClaimsByEnvelope:
    def test_empty_result(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            result = list_claims_by_envelope(tenant_id="t1", source_envelope_id="env_001")
        assert result == []

    def test_passes_correct_params(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            list_claims_by_envelope(tenant_id="tenant_abc", source_envelope_id="env_xyz")
        params = cur.execute.call_args[0][1]
        assert "tenant_abc" in params
        assert "env_xyz" in params

    def test_connection_closed(self):
        conn, cur = _mock_conn()
        cur.fetchall.return_value = []
        with patch("src.service.gaqp.corpus.get_conn", return_value=conn):
            list_claims_by_envelope(tenant_id="t1", source_envelope_id="e1")
        conn.close.assert_called_once()
