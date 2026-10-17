# auditor-headers-seguranca

Security HTTP headers auditor. Checks whether a site sends security headers in the response and generates a score from 0 to 100 with the list of what is missing.

## What it does

Receives a URL, queries the response headers and checks the presence of five security headers:

- Content-Security-Policy (CSP)
- Strict-Transport-Security (HSTS)
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

Each present header is worth 20 points. The report shows a score (0-100) and which headers are missing. Header lookup is case-insensitive.

## Stack

- Python 3.10+
- requests

## Install

```bash
pip install -e .
```

Or just the dependency:

```bash
pip install requests
```

## Usage

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

## Tests

```bash
python -m pytest -q
```

Result: 5 passed. Covers score 100, score 0, partial score, case-insensitive headers and audit with a faked session.

## License

MIT

## Author

Kelvin Oliveira
