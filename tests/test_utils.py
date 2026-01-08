"""Tests for PayFast utility functions"""

import pytest
from fastapi_payfast.utils import generate_signature, generate_payment_form_html


class TestGenerateSignature:
    """Test suite for generate_signature function"""
    
    def test_generate_signature_basic(self):
        """Test basic signature generation"""
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product'
        }
        
        signature = generate_signature(data)
        assert isinstance(signature, str)
        assert len(signature) == 32  # MD5 hash length
    
    def test_generate_signature_with_passphrase(self):
        """Test signature generation with passphrase"""
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product'
        }
        
        signature_without = generate_signature(data)
        signature_with = generate_signature(data, 'test_passphrase')
        
        assert signature_without != signature_with
    
    def test_generate_signature_deterministic(self):
        """Test that signature generation is deterministic"""
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product'
        }
        
        sig1 = generate_signature(data)
        sig2 = generate_signature(data)
        
        assert sig1 == sig2
    
    def test_generate_signature_order_independent(self):
        """Test that signature is independent of dict order"""
        data1 = {
            'merchant_id': '10000100',
            'amount': '100.00',
            'merchant_key': '46f0cd694581a',
            'item_name': 'Test Product'
        }
        
        data2 = {
            'item_name': 'Test Product',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'merchant_id': '10000100'
        }
        
        assert generate_signature(data1) == generate_signature(data2)
    
    def test_generate_signature_ignores_none_values(self):
        """Test that None values are ignored"""
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product',
            'item_description': None
        }
        
        data_without_none = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product'
        }
        
        assert generate_signature(data) == generate_signature(data_without_none)
    
    def test_generate_signature_ignores_empty_strings(self):
        """Test that empty strings are ignored"""
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product',
            'item_description': ''
        }
        
        data_without_empty = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product'
        }
        
        assert generate_signature(data) == generate_signature(data_without_empty)
    
    def test_generate_signature_ignores_signature_field(self):
        """Test that signature field is ignored"""
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product',
            'signature': 'old_signature'
        }
        
        data_without_sig = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product'
        }
        
        assert generate_signature(data) == generate_signature(data_without_sig)
    
    def test_generate_signature_special_characters(self):
        """Test signature generation with special characters"""
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product & Special Chars!',
            'item_description': 'With spaces and @#$%'
        }
        
        signature = generate_signature(data)
        assert isinstance(signature, str)
        assert len(signature) == 32


class TestGeneratePaymentFormHTML:
    """Test suite for generate_payment_form_html function"""
    
    def test_generate_form_basic(self):
        """Test basic form generation"""
        action_url = "https://sandbox.payfast.co.za/eng/process"
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product'
        }
        
        html = generate_payment_form_html(action_url, data)
        
        assert isinstance(html, str)
        assert '<!DOCTYPE html>' in html
        assert action_url in html
        assert 'merchant_id' in html
        assert '10000100' in html
    
    def test_generate_form_all_fields(self):
        """Test form generation with all fields"""
        action_url = "https://sandbox.payfast.co.za/eng/process"
        data = {
            'merchant_id': '10000100',
            'merchant_key': '46f0cd694581a',
            'amount': '100.00',
            'item_name': 'Test Product',
            'item_description': 'Test Description',
            'return_url': 'https://example.com/success',
            'signature': 'abc123'
        }
        
        html = generate_payment_form_html(action_url, data)
        
        for key, value in data.items():
            assert key in html
            assert str(value) in html
    
    def test_generate_form_auto_submit_script(self):
        """Test that form includes auto-submit script"""
        action_url = "https://sandbox.payfast.co.za/eng/process"
        data = {'merchant_id': '10000100'}
        
        html = generate_payment_form_html(action_url, data)
        
        assert 'submit()' in html
        assert '<script>' in html
    
    def test_generate_form_has_styling(self):
        """Test that form includes styling"""
        action_url = "https://sandbox.payfast.co.za/eng/process"
        data = {'merchant_id': '10000100'}
        
        html = generate_payment_form_html(action_url, data)
        
        assert '<style>' in html
        assert 'spinner' in html
        assert 'Redirecting' in html
    
    def test_generate_form_hidden_inputs(self):
        """Test that all fields are hidden inputs"""
        action_url = "https://sandbox.payfast.co.za/eng/process"
        data = {
            'merchant_id': '10000100',
            'amount': '100.00',
            'item_name': 'Test'
        }
        
        html = generate_payment_form_html(action_url, data)
        
        assert html.count('type="hidden"') == len(data)
    
    def test_generate_form_special_characters_escaped(self):
        """Test that special characters are properly handled"""
        action_url = "https://sandbox.payfast.co.za/eng/process"
        data = {
            'merchant_id': '10000100',
            'item_name': 'Product with "quotes" & ampersands',
        }
        
        html = generate_payment_form_html(action_url, data)
        
        # HTML should be valid
        assert 'name="item_name"' in html
        assert 'value=' in html