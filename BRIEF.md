# BRIEF — auditor-headers-seguranca

## Entregas

Projeto de auditoria de headers HTTP de seguranca (area Cibersegurança), MVP.

Local:
`C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\auditor-headers-seguranca\`

Arquivos criados:
- `pyproject.toml` — declaracao do projeto Python (dependencia: requests >= 2.31.0) e entry point CLI `auditor-headers`.
- `src/auditor_headers_seguranca/__init__.py` — exportacao do pacote.
- `src/auditor_headers_seguranca/auditor.py` — `SecurityHeadersAuditor`: verifica Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options e Referrer-Policy; emite score 0-100 (cada header vale 20 pontos) e lista de headers ausentes. Busca de headers e case-insensitive. Sessao injetavel para testes sem rede.
- `src/auditor_headers_seguranca/__main__.py` — interface de linha de comando (`python -m auditor_headers_seguranca <URL>`).
- `tests/test_auditor.py` — 5 testes pytest com respostas HTTP falsificadas (stubs locais, sem rede).
- `README.md` — documentacao completa bilíngue PT-BR + EN (titulo, descricao, stack, headers verificados, score, como instalar, como usar, exemplos de saida, testes, licenca MIT, autor Kelvin Oliveira).
- `BRIEF.md` — este arquivo.

## Stack

Python 3.10+, requests. Testes com pytest.

## Critérios de aceitação

- [x] Score de seguranca (0-100)
- [x] Lista de headers faltantes
- [x] Headers verificados: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- [x] Testes que passam (sem rede)
- [x] README completo PT-BR + EN

## Como verificar

1. Instalar o projeto:
   ```bash
   cd C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\auditor-headers-seguranca\
   pip install -e .
   ```
2. Rodar a CLI contra qualquer URL:
   ```bash
   python -m auditor_headers_seguranca https://exemplo.com
   ```
3. Rodar a suíde de testes:
   ```bash
   python -m pytest -q
   ```
   Resultado esperado: `5 passed`.

## Autor

Kelvin Oliveira — licenca MIT.
