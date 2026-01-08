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

