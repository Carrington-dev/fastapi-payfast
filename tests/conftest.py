"""Pytest configuration and shared fixtures"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_config():
    """Session-scoped test configuration"""
    return {
        "merchant_id": "10000100",
        "merchant_key": "46f0cd694581a",
        "passphrase": "jt7NOE43FZPn",
        "sandbox": True
    }


@pytest.fixture
def sample_payment_data():
    """Sample payment data for testing"""
    return {
        "merchant_id": "10000100",
        "merchant_key": "46f0cd694581a",
        "amount": 100.00,
        "item_name": "Test Product",
        "item_description": "Test Description",
        "return_url": "https://example.com/success",
        "cancel_url": "https://example.com/cancel",
        "notify_url": "https://example.com/notify"
    }


@pytest.fixture
def sample_itn_data():
    """Sample ITN data for testing"""
    return {
        "merchant_id": "10000100",
        "pf_payment_id": "12345",
        "payment_status": "COMPLETE",
        "item_name": "Test Product",
        "amount_gross": 100.00,
        "amount_fee": 5.00,
        "amount_net": 95.00,
        "custom_str1": "custom_value",
        "custom_int1": 42
    }


@pytest.fixture
def mock_request_factory():
    """Factory for creating mock FastAPI requests"""
    from unittest.mock import Mock, AsyncMock
    from fastapi import Request
    
    def create_mock_request(form_data, client_ip="197.97.145.144"):
        request = Mock(spec=Request)
        request.form = AsyncMock(return_value=form_data)
        request.client = Mock()
        request.client.host = client_ip
        return request
    
    return create_mock_request


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment before each test"""
    yield
    # Cleanup after test if needed


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )