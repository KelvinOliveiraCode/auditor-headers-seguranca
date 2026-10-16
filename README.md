# auditor-headers-seguranca

Auditor de headers HTTP de seguranca. Verifica se um site envia os headers de seguranca da cabeca da resposta e gera uma pontuacao de 0 a 100 com a lista do que esta faltando.

## PT-BR

### O que faz

Recebe uma URL, consulta os headers de resposta e verifica a presenca de cinco headers de seguranca:

- Content-Security-Policy (CSP)
- Strict-Transport-Security (HSTS)
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

Cada header presente vale 20 pontos. O relatorio mostra a pontuacao (0-100) e quais headers estao ausentes.

### Stack

- Python 3.10+
- requests

### Como instalar

```bash
pip install -e .
```

Ou somente a dependencia:

```bash
pip install requests
```

### Como usar

Linha de comando:

```bash
python -m auditor_headers_seguranca https://exemplo.com
```

Saida com todos os headers presentes:

```
https://exemplo.com | score 100/100 | 5/5 | OK
```

Saida com headers faltando:

```
https://exemplo.com | score 60/100 | 3/5 | FALTANDO HEADERS
  faltando: Strict-Transport-Security
  faltando: Referrer-Policy
```

Em Python:

```python
from auditor_headers_seguranca import SecurityHeadersAuditor

auditor = SecurityHeadersAuditor()
report = auditor.audit("https://exemplo.com")

print(report.score)      # 0 a 100
print(report.missing)    # lista de headers ausentes
print(report.percentage) # 0.0 a 100.0
```

Os testes nao usam rede: as respostas HTTP sao falsificadas com stubs locais.

### Testes

```bash
python -m pytest -q
```

Resultado: 5 passed. Cobrem score 100, score 0, score parcial, cabecalhos case-insensitive e auditoria com sessao falsificada.

### Licenca

MIT

### Autor

Kelvin Oliveira

## EN

### What it does

Receives a URL, queries the response headers and checks the presence of five security headers:

- Content-Security-Policy (CSP)
- Strict-Transport-Security (HSTS)
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

Each present header is worth 20 points. The report shows a score (0-100) and which headers are missing.

### Stack

- Python 3.10+
- requests

### Install

```bash
pip install -e .
```

Or just the dependency:

```bash
pip install requests
```

### Usage

Command line:

```bash
python -m auditor_headers_seguranca https://example.com
```

Output with all headers present:

```
https://example.com | score 100/100 | 5/5 | OK
```

Output with missing headers:

```
https://example.com | score 60/100 | 3/5 | MISSING HEADERS
  missing: Strict-Transport-Security
  missing: Referrer-Policy
```

In Python:

```python
from auditor_headers_seguranca import SecurityHeadersAuditor

auditor = SecurityHeadersAuditor()
report = auditor.audit("https://example.com")

print(report.score)      # 0 to 100
print(report.missing)    # list of missing headers
print(report.percentage) # 0.0 to 100.0
```

Tests do not use the network: HTTP responses are faked with local stubs.

### Tests

```bash
python -m pytest -q
```

Result: 5 passed. Covers score 100, score 0, partial score, case-insensitive headers and audit with a faked session.

### License

MIT

### Author

Kelvin Oliveira
