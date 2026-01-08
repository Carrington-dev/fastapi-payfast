"""Tests for PayFast exceptions"""

import pytest
from fastapi import HTTPException, status

from fastapi_payfast.exceptions import (
    PayFastException,
    SignatureVerificationError,
    InvalidMerchantError,
    InvalidAmountError
)


class TestPayFastException:
    """Test suite for PayFastException"""
    
    def test_payfast_exception_basic(self):
        """Test basic PayFastException"""
        exc = PayFastException("Test error")
        assert str(exc) == "Test error"
    
    def test_payfast_exception_inheritance(self):
        """Test that PayFastException inherits from Exception"""
        exc = PayFastException("Test error")
        assert isinstance(exc, Exception)


class TestSignatureVerificationError:
    """Test suite for SignatureVerificationError"""
    
    def test_signature_verification_error_default_message(self):
        """Test SignatureVerificationError with default message"""
        exc = SignatureVerificationError()
        assert exc.message == "Invalid signature"
        assert str(exc) == "Invalid signature"
    
    def test_signature_verification_error_custom_message(self):
        """Test SignatureVerificationError with custom message"""
        exc = SignatureVerificationError("Custom error message")
        assert exc.message == "Custom error message"
        assert str(exc) == "Custom error message"
    
    def test_signature_verification_error_inheritance(self):
        """Test that SignatureVerificationError inherits from PayFastException"""
        exc = SignatureVerificationError()
        assert isinstance(exc, PayFastException)
    
    def test_signature_verification_error_to_http_exception(self):
        """Test converting to HTTPException"""
        exc = SignatureVerificationError("Signature mismatch")
        http_exc = exc.to_http_exception()
        
        assert isinstance(http_exc, HTTPException)
        assert http_exc.status_code == status.HTTP_400_BAD_REQUEST
        assert http_exc.detail == "Signature mismatch"


class TestInvalidMerchantError:
    """Test suite for InvalidMerchantError"""
    
    def test_invalid_merchant_error_default_message(self):
        """Test InvalidMerchantError with default message"""
        exc = InvalidMerchantError()
        assert exc.message == "Invalid merchant ID"
        assert str(exc) == "Invalid merchant ID"
    
    def test_invalid_merchant_error_custom_message(self):
        """Test InvalidMerchantError with custom message"""
        exc = InvalidMerchantError("Merchant ID does not match")
        assert exc.message == "Merchant ID does not match"
        assert str(exc) == "Merchant ID does not match"
    
    def test_invalid_merchant_error_inheritance(self):
        """Test that InvalidMerchantError inherits from PayFastException"""
        exc = InvalidMerchantError()
        assert isinstance(exc, PayFastException)
    
    def test_invalid_merchant_error_to_http_exception(self):
        """Test converting to HTTPException"""
        exc = InvalidMerchantError("Invalid merchant")
        http_exc = exc.to_http_exception()
        
        assert isinstance(http_exc, HTTPException)
        assert http_exc.status_code == status.HTTP_400_BAD_REQUEST
        assert http_exc.detail == "Invalid merchant"


class TestInvalidAmountError:
    """Test suite for InvalidAmountError"""
    
    def test_invalid_amount_error_basic(self):
        """Test InvalidAmountError with expected and received amounts"""
        exc = InvalidAmountError(expected=100.00, received=95.00)
        
        assert exc.expected == 100.00
        assert exc.received == 95.00
        assert "expected 100.0" in exc.message
        assert "received 95.0" in exc.message
    
    def test_invalid_amount_error_message_format(self):
        """Test InvalidAmountError message format"""
        exc = InvalidAmountError(expected=100.00, received=105.50)
        
        assert exc.message == "Amount mismatch: expected 100.0, received 105.5"
        assert str(exc) == "Amount mismatch: expected 100.0, received 105.5"
    
    def test_invalid_amount_error_inheritance(self):
        """Test that InvalidAmountError inherits from PayFastException"""
        exc = InvalidAmountError(expected=100.00, received=95.00)
        assert isinstance(exc, PayFastException)
    
    def test_invalid_amount_error_to_http_exception(self):
        """Test converting to HTTPException"""
        exc = InvalidAmountError(expected=100.00, received=95.00)
        http_exc = exc.to_http_exception()
        
        assert isinstance(http_exc, HTTPException)
        assert http_exc.status_code == status.HTTP_400_BAD_REQUEST
        assert "Amount mismatch" in http_exc.detail
    
    def test_invalid_amount_error_different_amounts(self):
        """Test InvalidAmountError with various amounts"""
        test_cases = [
            (50.00, 45.00),
            (1000.00, 1005.00),
            (0.01, 0.02),
            (99.99, 100.00)
        ]
        
        for expected, received in test_cases:
            exc = InvalidAmountError(expected=expected, received=received)
            assert exc.expected == expected
            assert exc.received == received
            assert f"expected {expected}" in exc.message
            assert f"received {received}" in exc.message


class TestExceptionHandling:
    """Test suite for exception handling scenarios"""
    
    def test_catching_payfast_exception(self):
        """Test catching PayFastException base class"""
        try:
            raise SignatureVerificationError("Test error")
        except PayFastException as e:
            assert str(e) == "Test error"
    
    def test_catching_specific_exceptions(self):
        """Test catching specific exception types"""
        exceptions = [
            SignatureVerificationError("Sig error"),
            InvalidMerchantError("Merchant error"),
            InvalidAmountError(100.00, 95.00)
        ]
        
        for exc in exceptions:
            try:
                raise exc
            except PayFastException as e:
                assert isinstance(e, PayFastException)
    
    def test_http_exception_conversion(self):
        """Test converting all custom exceptions to HTTPException"""
        exceptions = [
            SignatureVerificationError("Sig error"),
            InvalidMerchantError("Merchant error"),
            InvalidAmountError(100.00, 95.00)
        ]
        
        for exc in exceptions:
            http_exc = exc.to_http_exception()
            assert isinstance(http_exc, HTTPException)
            assert http_exc.status_code == status.HTTP_400_BAD_REQUEST