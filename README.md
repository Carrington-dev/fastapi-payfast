# FastAPI PayFast Package - Complete Project Structure




## 📄 pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fastapi-payfast"
version = "1.0.0"
description = "FastAPI integration package for PayFast payment gateway"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["fastapi", "payfast", "payment", "gateway", "south africa"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Framework :: FastAPI",
]
dependencies = [
    "fastapi>=0.104.0",
    "pydantic>=2.0.0",
    "python-multipart>=0.0.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.24.0",
    "black>=23.7.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
    "mypy>=1.5.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/fastapi-payfast"
Documentation = "https://github.com/yourusername/fastapi-payfast#readme"
Repository = "https://github.com/yourusername/fastapi-payfast"
"Bug Tracker" = "https://github.com/yourusername/fastapi-payfast/issues"

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_calls = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--cov=fastapi_payfast",
    "--cov-report=html",
    "--cov-report=term-missing",
]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["fastapi_payfast"]
omit = [
    "*/tests/*",
    "*/examples/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if False:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

## 📄 .gitignore
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local
.env.*.local

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Temporary files
*.log
*.tmp
```

## 📄 .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        name: isort (python)

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100', '--extend-ignore=E203,W503']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 📄 MANIFEST.in
```
include README.md
include LICENSE
include requirements.txt
include requirements-dev.txt
recursive-include fastapi_payfast *.py
recursive-exclude tests *
recursive-exclude examples *
```

## 📄 LICENSE (MIT)
```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📄 README.md
```markdown
# FastAPI PayFast Integration

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete, production-ready FastAPI integration package for PayFast, South Africa's leading payment gateway.

## Features

✅ **Type-Safe** - Full Pydantic validation and type hints  
✅ **Async Support** - Built for FastAPI's async capabilities  
✅ **Secure** - MD5 signature verification and passphrase support  
✅ **Simple** - Clean API with sensible defaults  
✅ **Complete** - Supports payments, subscriptions, and ITN handling  
✅ **Tested** - Comprehensive test coverage  
✅ **Production-Ready** - Sandbox and production modes

## Installation

```bash
pip install fastapi-payfast
```

For development:
```bash
pip install fastapi-payfast[dev]
```

## Quick Start

### 1. Configure PayFast

```python
from fastapi_payfast import PayFastConfig, PayFastClient

config = PayFastConfig(
    merchant_id="your_merchant_id",
    merchant_key="your_merchant_key",
    passphrase="your_passphrase",
    sandbox=True  # Set to False for production
)

payfast = PayFastClient(config)
```

### 2. Create a Payment

```python
from fastapi import FastAPI
from fastapi_payfast import PayFastPaymentData

app = FastAPI()

@app.post("/checkout")
async def checkout(amount: float, item_name: str):
    payment_data = PayFastPaymentData(
        merchant_id=config.merchant_id,
        merchant_key=config.merchant_key,
        amount=amount,
        item_name=item_name,
        return_url="https://yoursite.com/success",
        cancel_url="https://yoursite.com/cancel",
        notify_url="https://yoursite.com/notify",
    )
    
    return payfast.generate_payment_response(payment_data)
```

### 3. Handle Payment Notifications (ITN)

```python
from fastapi import Request
from fastapi_payfast import PaymentStatus

@app.post("/notify")
async def payment_notify(request: Request):
    try:
        itn_data = await payfast.verify_itn(request)
        
        if payfast.is_payment_successful(itn_data):
            # Process successful payment
            print(f"Payment received: R{itn_data.amount_gross}")
            # Update database, send confirmation, etc.
        
        return {"status": "ok"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Advanced Usage

### Subscriptions

```python
from fastapi_payfast import SubscriptionType, FrequencyType

payment_data = PayFastPaymentData(
    merchant_id=config.merchant_id,
    merchant_key=config.merchant_key,
    amount=99.00,
    item_name="Monthly Subscription",
    subscription_type=SubscriptionType.SUBSCRIPTION,
    billing_date="2024-02-01",
    recurring_amount=99.00,
    frequency=FrequencyType.MONTHLY,
    cycles=12  # 0 for infinite
)
```

### Custom Fields

```python
payment_data = PayFastPaymentData(
    # ... other fields
    m_payment_id="ORDER-12345",
    custom_str1="user_id_123",
    custom_int1=42,
)
```

### Amount Validation

```python
itn_data = await payfast.verify_itn(request)
expected_amount = 99.00

if not payfast.validate_payment_amount(itn_data, expected_amount):
    # Handle amount mismatch
    pass
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `merchant_id` | str | Required | Your PayFast merchant ID |
| `merchant_key` | str | Required | Your PayFast merchant key |
| `passphrase` | str | Required | Security passphrase |
| `sandbox` | bool | True | Use sandbox environment |
| `validate_ip` | bool | True | Validate PayFast IP addresses |

## Payment Statuses

- `COMPLETE` - Payment successful
- `FAILED` - Payment failed
- `PENDING` - Payment pending
- `CANCELLED` - Payment cancelled

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=fastapi_payfast --cov-report=html
```

## Development

Setup development environment:
```bash
# Clone repository
git clone https://github.com/yourusername/fastapi-payfast.git
cd fastapi-payfast

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Security

- Always use HTTPS in production
- Keep your merchant key and passphrase secret
- Use environment variables for sensitive data
- Verify ITN signatures on your server
- Validate payment amounts match your records

## Resources

- [PayFast Documentation](https://developers.payfast.co.za/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Issue Tracker](https://github.com/yourusername/fastapi-payfast/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For PayFast-specific issues, contact [PayFast Support](https://www.payfast.co.za/contact/).

For package issues, please use the [GitHub issue tracker](https://github.com/yourusername/fastapi-payfast/issues).
```

## 📄 Makefile (Optional but helpful)
```makefile
.PHONY: install test lint format clean build publish

install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest --cov=fastapi_payfast --cov-report=html --cov-report=term

lint:
	flake8 fastapi_payfast tests
	mypy fastapi_payfast
	pylint fastapi_payfast

format:
	black fastapi_payfast tests examples
	isort fastapi_payfast tests examples

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

dev:
	uvicorn examples.basic_usage:app --reload --host 0.0.0.0 --port 8000
```

## 📄 .env.example
```bash
# PayFast Configuration
PAYFAST_MERCHANT_ID=10000100
PAYFAST_MERCHANT_KEY=46f0cd694581a
PAYFAST_PASSPHRASE=jt7NOE43FZPn
PAYFAST_SANDBOX=true

# Application Configuration
APP_ENV=development
DEBUG=true
```