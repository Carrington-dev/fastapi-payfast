"""Tests for PayFast configuration"""

import pytest
from fastapi_payfast.config import PayFastConfig


class TestPayFastConfig:
    """Test suite for PayFastConfig"""
    
    def test_config_initialization(self):
        """Test basic configuration initialization"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn",
            sandbox=True
        )
        
        assert config.merchant_id == "10000100"
        assert config.merchant_key == "46f0cd694581a"
        assert config.passphrase == "jt7NOE43FZPn"
        assert config.sandbox is True
        assert config.validate_ip is True
    
    def test_config_sandbox_process_url(self):
        """Test sandbox process URL"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn",
            sandbox=True
        )
        
        assert config.process_url == "https://sandbox.payfast.co.za/eng/process"
    
    def test_config_production_process_url(self):
        """Test production process URL"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn",
            sandbox=False
        )
        
        assert config.process_url == "https://www.payfast.co.za/eng/process"
    
    def test_config_sandbox_validate_url(self):
        """Test sandbox validate URL"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn",
            sandbox=True
        )
        
        assert config.validate_url == "https://sandbox.payfast.co.za/eng/query/validate"
    
    def test_config_production_validate_url(self):
        """Test production validate URL"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn",
            sandbox=False
        )
        
        assert config.validate_url == "https://www.payfast.co.za/eng/query/validate"
    
    def test_config_valid_ips(self):
        """Test valid PayFast IP addresses"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn"
        )
        
        expected_ips = [
            "197.97.145.144",
            "41.74.179.194",
        ]
        
        assert config.valid_ips == expected_ips
    
    def test_config_immutability(self):
        """Test that config is immutable"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn"
        )
        
        with pytest.raises(Exception):
            config.merchant_id = "new_id"
    
    def test_config_missing_required_fields(self):
        """Test that missing required fields raise validation error"""
        with pytest.raises(Exception):
            PayFastConfig(
                merchant_id="10000100",
                merchant_key="46f0cd694581a"
                # Missing passphrase
            )
    
    def test_config_default_values(self):
        """Test default configuration values"""
        config = PayFastConfig(
            merchant_id="10000100",
            merchant_key="46f0cd694581a",
            passphrase="jt7NOE43FZPn"
        )
        
        assert config.sandbox is True
        assert config.validate_ip is True