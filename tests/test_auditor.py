"""Testes da auditoria de headers de seguranca.

Todas as respostas HTTP sao falsificadas localmente (stub); nao ha acesso a rede.
"""

from __future__ import annotations

from auditor_headers_seguranca import SecurityHeadersAuditor, SECURITY_HEADERS

FULL_HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
}


class StubResponse:
    """Resposta HTTP falsificada (stub sem rede)."""

    def __init__(self, headers: dict[str, str]) -> None:
        self.headers = headers


class StubSession:
    """Sessao falsificada que devolve a mesma resposta para qualquer GET."""

    def __init__(self, headers: dict[str, str]) -> None:
        self._response = StubResponse(headers)

    def get(self, url: str, timeout: float = 10.0) -> StubResponse:  # noqa: ARG002
        return self._response


def test_todos_os_headers_presentes_score_100() -> None:
    report = SecurityHeadersAuditor().audit_headers(FULL_HEADERS, "https://exemplo.com/")
    assert report.score == 100
    assert report.present == 5
    assert report.total == 5
    assert report.missing == []
    assert report.percentage == 100.0


def test_nenhum_header_presente_score_zero() -> None:
    report = SecurityHeadersAuditor().audit_headers({}, "https://exemplo.com/")
    assert report.score == 0
    assert report.present == 0
    assert report.total == 5
    assert report.missing == list(SECURITY_HEADERS)
    assert report.percentage == 0.0


def test_score_partial_proporcional() -> None:
    partial = {
        "Content-Security-Policy": "default-src 'self'",
        "X-Frame-Options": "SAMEORIGIN",
    }
    report = SecurityHeadersAuditor().audit_headers(partial, "https://exemplo.com/")
    assert report.score == 40
    assert report.present == 2
    assert report.missing == [
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]


def test_cabecalhos_sao_case_insensitive() -> None:
    lowercased = {name.lower(): value for name, value in FULL_HEADERS.items()}
    report = SecurityHeadersAuditor().audit_headers(lowercased, "https://exemplo.com/")
    assert report.score == 100
    assert report.missing == []


def test_audit_com_sessao_falsificada_sem_rede() -> None:
    auditor = SecurityHeadersAuditor(session=StubSession(FULL_HEADERS))
    report = auditor.audit("https://exemplo.com/")
    assert report.score == 100
    assert report.url == "https://exemplo.com/"
    assert report.missing == []
