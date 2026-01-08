"""Tests for PayFast client"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import Request
from fastapi.responses import HTMLResponse

from fastapi_payfast import (
    PayFastClient,
    PayFastConfig,
    PayFastPaymentData,
    PayFastITNData,
    PaymentStatus,
    SignatureVerificationError,
    InvalidMerchantError
)


@pytest.fixture
def config():
    """Fixture for PayFast configuration"""
    return PayFastConfig(
        merchant_id="10000100",
        merchant_key="46f0cd694581a",
        passphrase="jt7NOE43FZPn",
        sandbox=True
    )


@pytest.fixture
def client(config):
    """Fixture for PayFast client"""
    return PayFastClient(config)


@pytest.fixture
def payment_data(config):
    """Fixture for payment data"""
    return PayFastPaymentData(
        merchant_id=config.merchant_id,
        merchant_key=config.merchant_key,
        amount=100.00,
        item_name="Test Product",
        return_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        notify_url="https://example.com/notify"
    )


class TestPayFastClient:
    """Test suite for PayFastClient"""
    
    def test_client_initialization(self, config):
        """Test client initialization"""
        client = PayFastClient(config)
        assert client.config == config
    
    def test_create_payment(self, client, payment_data):
        """Test creating payment request"""
        result = client.create_payment(payment_data)
        
        assert 'action_url' in result
        assert 'data' in result
        assert result['action_url'] == "https://sandbox.payfast.co.za/eng/process"
        assert 'signature' in result['data']
        assert result['data']['merchant_id'] == "10000100"
        assert result['data']['amount'] == 100.00
    
    def test_create_payment_signature_included(self, client, payment_data):
        """Test that signature is included in payment data"""
        result = client.create_payment(payment_data)
        
        assert 'signature' in result['data']
        assert len(result['data']['signature']) == 32  # MD5 hash
    
    def test_create_payment_removes_none_values(self, client, config):
        """Test that None values are removed from payment data"""
        payment_data = PayFastPaymentData(
            merchant_id=config.merchant_id,
            merchant_key=config.merchant_key,
            amount=100.00,
            item_name="Test Product",
            item_description=None  # None value
        )
        
        result = client.create_payment(payment_data)
        assert 'item_description' not in result['data']
    
    def test_generate_payment_form(self, client, payment_data):
        """Test generating payment form HTML"""
        html = client.generate_payment_form(payment_data)
        
        assert isinstance(html, str)
        assert '<!DOCTYPE html>' in html
        assert 'sandbox.payfast.co.za' in html
        assert 'merchant_id' in html
        assert 'signature' in html
    
    def test_generate_payment_response(self, client, payment_data):
        """Test generating payment HTMLResponse"""
        response = client.generate_payment_response(payment_data)
        
        assert isinstance(response, HTMLResponse)
        assert '<!DOCTYPE html>' in response.body.decode()
    
    @pytest.mark.asyncio
    async def test_verify_itn_success(self, client, config):
        """Test successful ITN verification"""
        # Create mock request with form data
        form_data = {
            'merchant_id': config.merchant_id,
            'pf_payment_id': '12345',
            'payment_status': 'COMPLETE',
            'item_name': 'Test Product',
            'amount_gross': '100.00',
            'amount_fee': '5.00',
            'amount_net': '95.00',
        }
        
        # Generate valid signature
        from fastapi_payfast.utils import generate_signature
        form_data['signature'] = generate_signature(form_data, config.passphrase)
        
        # Create mock request
        request = Mock(spec=Request)
        request.form = AsyncMock(return_value=form_data)
        request.client = Mock()
        request.client.host = "197.97.145.144"
        
        # Verify ITN
        itn_data = await client.verify_itn(request)
        
        assert isinstance(itn_data, PayFastITNData)
        assert itn_data.pf_payment_id == '12345'
        assert itn_data.payment_status == PaymentStatus.COMPLETE
        assert itn_data.amount_gross == 100.00
    
    @pytest.mark.asyncio
    async def test_verify_itn_missing_signature(self, client, config):
        """Test ITN verification with missing signature"""
        form_data = {
            'merchant_id': config.merchant_id,
            'pf_payment_id': '12345',
            'payment_status': 'COMPLETE',
            'item_name': 'Test Product',
            'amount_gross': '100.00',
            'amount_fee': '5.00',
            'amount_net': '95.00',
        }
        
        request = Mock(spec=Request)
        request.form = AsyncMock(return_value=form_data)
        
        with pytest.raises(SignatureVerificationError, match="Missing signature"):
            await client.verify_itn(request)
    
    @pytest.mark.asyncio
    async def test_verify_itn_invalid_signature(self, client, config):
        """Test ITN verification with invalid signature"""
        form_data = {
            'merchant_id': config.merchant_id,
            'pf_payment_id': '12345',
            'payment_status': 'COMPLETE',
            'item_name': 'Test Product',
            'amount_gross': '100.00',
            'amount_fee': '5.00',
            'amount_net': '95.00',
            'signature': 'invalid_signature_123'
        }
        
        request = Mock(spec=Request)
        request.form = AsyncMock(return_value=form_data)
        
        with pytest.raises(SignatureVerificationError, match="Signature mismatch"):
            await client.verify_itn(request)
    
    @pytest.mark.asyncio
    async def test_verify_itn_invalid_merchant(self, client, config):
        """Test ITN verification with invalid merchant ID"""
        form_data = {
            'merchant_id': 'wrong_merchant_id',
            'pf_payment_id': '12345',
            'payment_status': 'COMPLETE',
            'item_name': 'Test Product',
            'amount_gross': '100.00',
            'amount_fee': '5.00',
            'amount_net': '95.00',
        }
        
        from fastapi_payfast.utils import generate_signature
        form_data['signature'] = generate_signature(form_data, config.passphrase)
        
        request = Mock(spec=Request)
        request.form = AsyncMock(return_value=form_data)
        
        with pytest.raises(InvalidMerchantError):
            await client.verify_itn(request)
    
    def test_validate_payment_amount_exact_match(self, client):
        """Test payment amount validation with exact match"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.COMPLETE,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert client.validate_payment_amount(itn_data, 100.00)
    
    def test_validate_payment_amount_within_tolerance(self, client):
        """Test payment amount validation within tolerance"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.COMPLETE,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert client.validate_payment_amount(itn_data, 100.005)
    
    def test_validate_payment_amount_outside_tolerance(self, client):
        """Test payment amount validation outside tolerance"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.COMPLETE,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert not client.validate_payment_amount(itn_data, 105.00)
    
    def test_validate_payment_amount_custom_tolerance(self, client):
        """Test payment amount validation with custom tolerance"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.COMPLETE,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert client.validate_payment_amount(itn_data, 105.00, tolerance=5.0)
    
    def test_is_payment_successful_complete(self, client):
        """Test is_payment_successful with COMPLETE status"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.COMPLETE,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert client.is_payment_successful(itn_data)
    
    def test_is_payment_successful_failed(self, client):
        """Test is_payment_successful with FAILED status"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.FAILED,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert not client.is_payment_successful(itn_data)
    
    def test_is_payment_successful_pending(self, client):
        """Test is_payment_successful with PENDING status"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.PENDING,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert not client.is_payment_successful(itn_data)
    
    def test_is_payment_successful_cancelled(self, client):
        """Test is_payment_successful with CANCELLED status"""
        itn_data = PayFastITNData(
            pf_payment_id="12345",
            payment_status=PaymentStatus.CANCELLED,
            item_name="Test",
            amount_gross=100.00,
            amount_fee=5.00,
            amount_net=95.00,
            merchant_id="10000100",
            signature="abc123"
        )
        
        assert not client.is_payment_successful(itn_data)