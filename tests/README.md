# FastAPI PayFast Tests

Comprehensive test suite for the FastAPI PayFast integration package.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest configuration and shared fixtures
├── test_config.py           # Configuration tests
├── test_models.py           # Data model tests
├── test_utils.py            # Utility function tests
├── test_client.py           # Client functionality tests
├── test_exceptions.py       # Exception handling tests
└── test_integration.py      # Integration tests
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=fastapi_payfast --cov-report=html --cov-report=term
```

### Run specific test file
```bash
pytest tests/test_config.py
```

### Run specific test class
```bash
pytest tests/test_config.py::TestPayFastConfig
```

### Run specific test method
```bash
pytest tests/test_config.py::TestPayFastConfig::test_config_initialization
```

### Run tests by marker
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Run with verbose output
```bash
pytest -v
```

### Run with output capture disabled (see print statements)
```bash
pytest -s
```

## Test Categories

### Unit Tests

**test_config.py** - Configuration tests
- Configuration initialization
- Sandbox/production URL generation
- Valid IP addresses
- Immutability
- Default values

**test_models.py** - Data model tests
- Payment data validation
- ITN data parsing
- Enum values
- Amount rounding
- Field validation

**test_utils.py** - Utility function tests
- Signature generation
- Signature determinism
- HTML form generation
- Special character handling
- Passphrase support

**test_exceptions.py** - Exception tests
- Custom exception creation
- Exception inheritance
- HTTP exception conversion
- Error messages

### Integration Tests

**test_client.py** - Client functionality tests
- Payment creation
- Form generation
- ITN verification
- Amount validation
- Payment status checking

**test_integration.py** - Full workflow tests
- Complete payment flow
- Endpoint integration
- Error handling
- Concurrent requests

## Test Fixtures

### Configuration Fixtures
- `test_config` - Session-scoped test configuration
- `config` - PayFast configuration object
- `client` - PayFast client instance

### Data Fixtures
- `sample_payment_data` - Sample payment data dictionary
- `sample_itn_data` - Sample ITN data dictionary
- `payment_data` - PayFastPaymentData object

### Mock Fixtures
- `mock_request_factory` - Factory for creating mock FastAPI requests
- `app` - FastAPI application instance
- `client` - TestClient for API testing

## Coverage Goals

The test suite aims for:
- **90%+ overall coverage**
- **100% coverage** for critical paths:
  - Signature verification
  - Amount validation
  - Payment status checking
  - Exception handling

## Writing New Tests

### Test Naming Convention
```python
def test_<functionality>_<scenario>():
    """Brief description of what the test does"""
    # Arrange
    # Act
    # Assert
```

### Example Test
```python
def test_validate_payment_amount_exact_match(client):
    """Test payment amount validation with exact match"""
    # Arrange
    itn_data = PayFastITNData(...)
    expected_amount = 100.00
    
    # Act
    result = client.validate_payment_amount(itn_data, expected_amount)
    
    # Assert
    assert result is True
```

### Async Tests
```python
@pytest.mark.asyncio
async def test_verify_itn_success(client):
    """Test successful ITN verification"""
    request = mock_request_factory(valid_data)
    itn_data = await client.verify_itn(request)
    assert itn_data.payment_status == PaymentStatus.COMPLETE
```

## Continuous Integration

Tests are automatically run on:
- Every push to main branch
- Every pull request
- Before package release

### GitHub Actions Workflow
```yaml
- name: Run tests
  run: |
    pytest --cov=fastapi_payfast --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure package is installed in editable mode
pip install -e .
```

**Async Test Errors**
```bash
# Install pytest-asyncio
pip install pytest-asyncio
```

**Coverage Not Generated**
```bash
# Install pytest-cov
pip install pytest-cov
```

### Debug Mode
```bash
# Run with Python debugger
pytest --pdb

# Drop into debugger on failure
pytest --pdb --maxfail=1
```

## Performance Testing

### Measure Test Execution Time
```bash
pytest --durations=10
```

### Profile Tests
```bash
pytest --profile
```

## Test Data

All test data uses PayFast sandbox credentials:
- Merchant ID: `10000100`
- Merchant Key: `46f0cd694581a`
- Passphrase: `jt7NOE43FZPn`

**Never use production credentials in tests!**

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain coverage above 90%
4. Update this README if adding new test categories

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [PayFast API Documentation](https://developers.payfast.co.za/)