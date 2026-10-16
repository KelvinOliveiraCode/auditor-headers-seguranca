"""Interface de linha de comando do auditor de headers de seguranca."""

from __future__ import annotations

import sys
from typing import Sequence

from .auditor import SecurityHeadersAuditor


def format_report_line(report) -> str:
    """Formata uma linha resumida do relatorio."""

    status = "OK" if not report.missing else "FALTANDO HEADERS"
    return f"{report.url} | score {report.score}/100 | {report.present}/{report.total} | {status}"


def main(argv: Sequence[str] | None = None) -> int:
    """Ponto de entrada da CLI.

    Args:
        argv: Argumentos da linha de comando (padrao: sys.argv[1:]).

    Returns:
        Codigo de saida do processo (0 auditoria concluida, 1 erro, 2 uso invalido).
    """

    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Uso: auditor-headers <URL>", file=sys.stderr)
        return 2
    url = args[0]
    auditor = SecurityHeadersAuditor()
    try:
        report = auditor.audit(url)
    except Exception as exc:  # CLI nao deve estourar traceback para o usuario
        print(f"Erro ao auditar {url}: {exc}", file=sys.stderr)
        return 1
    print(format_report_line(report))
    for header in report.missing:
        print(f"  faltando: {header}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
