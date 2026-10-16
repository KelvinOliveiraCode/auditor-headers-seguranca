"""Auditor de headers HTTP de seguranca.

Verifica a presenca de headers de seguranca em uma resposta HTTP e emite
uma pontuacao de 0 a 100 mais a lista de headers ausentes.

Headers verificados:
- Content-Security-Policy (CSP)
- Strict-Transport-Security (HSTS)
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import requests

SECURITY_HEADERS: tuple[str, ...] = (
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
)

MAX_SCORE = 100


@dataclass(frozen=True)
class HeaderResult:
    """Resultado da verificacao de um unico header de seguranca."""

    name: str
    present: bool
    value: str | None


@dataclass(frozen=True)
class AuditReport:
    """Relatorio de auditoria: pontuacao (0-100) e headers ausentes."""

    url: str
    score: int
    total: int
    present: int
    missing: list[str]
    results: list[HeaderResult]

    @property
    def percentage(self) -> float:
        """Pontuacao expressa como percentual (0.0 a 100.0)."""

        if self.total == 0:
            return 0.0
        return (self.present / self.total) * 100.0


class SecurityHeadersAuditor:
    """Audita headers de seguranca de uma resposta HTTP.

    A sessao e injetavel para permitir testes com respostas falsificadas
    sem acesso a rede. A busca de headers e case-insensitive, independent
    do tipo do mapeamento recebido.
    """

    def __init__(
        self,
        session: requests.Session | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.session = session or requests.Session()
        self.timeout = timeout

    def audit(self, url: str) -> AuditReport:
        """Audita os headers de seguranca de ``url``.

        Args:
            url: Endereco alvo da auditoria.

        Returns:
            AuditReport com pontuacao (0-100) e lista de headers ausentes.

        Raises:
            requests.RequestException: em falha de rede ou timeout.
        """

        response = self.session.get(url, timeout=self.timeout)
        return self.audit_headers(response.headers, url)

    def audit_headers(self, headers: Mapping[str, str], url: str = "") -> AuditReport:
        """Audita um mapeamento de headers ja capturado (sem rede).

        Args:
            headers: Cabecalhos HTTP recebidos na resposta.
            url: Endereco de origem (apenas informativo).

        Returns:
            AuditReport com pontuacao (0-100) e lista de headers ausentes.
        """

        lookup = {str(key).lower(): str(value) for key, value in headers.items()}
        results: list[HeaderResult] = []
        missing: list[str] = []
        present = 0
        for name in SECURITY_HEADERS:
            value = lookup.get(name.lower())
            is_present = value is not None
            results.append(HeaderResult(name=name, present=is_present, value=value))
            if is_present:
                present += 1
            else:
                missing.append(name)
        score = int(round((present / len(SECURITY_HEADERS)) * MAX_SCORE))
        return AuditReport(
            url=url,
            score=score,
            total=len(SECURITY_HEADERS),
            present=present,
            missing=missing,
            results=results,
        )
