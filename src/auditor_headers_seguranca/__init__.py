"""Auditor de headers HTTP de seguranca."""

from .auditor import (
    AuditReport,
    HeaderResult,
    MAX_SCORE,
    SECURITY_HEADERS,
    SecurityHeadersAuditor,
)

__all__ = [
    "AuditReport",
    "HeaderResult",
    "MAX_SCORE",
    "SECURITY_HEADERS",
    "SecurityHeadersAuditor",
]
