from __future__ import annotations


class GAQPError(Exception):
    """Base class for GAQP corpus errors."""


class ClaimNotFoundError(GAQPError):
    """Raised when a target claim does not exist in the tenant corpus."""


class SelfContradictionError(GAQPError):
    """Raised when a claim is linked as contradicting itself."""
