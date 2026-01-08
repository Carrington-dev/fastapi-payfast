"""PayFast client implementation"""

from typing import Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import HTMLResponse

from .config import PayFastConfig
from .models import PayFastPaymentData, PayFastITNData, PaymentStatus
from .exceptions import (
    SignatureVerificationError,
    InvalidMerchantError,
    InvalidAmountError
)
from .utils import generate_signature, generate_payment_form_html


class PayFastClient:
    """Main client for PayFast API integration"""
    
    def __init__(self, config: PayFastConfig):
        """
        Initialize PayFast client
        
        Args:
            config: PayFast configuration object
        """
        self.config = config
    
    def create_payment(self, payment_data: PayFastPaymentData) -> Dict[str, Any]:
        """
        Create payment request data with signature
        
        Args:
            payment_data: Payment data model
            
        Returns:
            Dictionary with action URL and signed data
        """
        # Convert to dict and remove None values
        data = {k: v for k, v in payment_data.dict().items() if v is not None}
        
        # Override merchant details from config
        data['merchant_id'] = self.config.merchant_id
        data['merchant_key'] = self.config.merchant_key
        
        # Generate signature
        signature = generate_signature(data, self.config.passphrase)
        data['signature'] = signature
        
        return {
            'action_url': self.config.process_url,
            'data': data
        }
    
    def generate_payment_form(self, payment_data: PayFastPaymentData) -> str:
        """
        Generate HTML form for payment
        
        Args:
            payment_data: Payment data model
            
        Returns:
            HTML string with auto-submitting form
        """
        payment_info = self.create_payment(payment_data)
        return generate_payment_form_html(
            payment_info['action_url'],
            payment_info['data']
        )
    
    def generate_payment_response(self, payment_data: PayFastPaymentData) -> HTMLResponse:
        """
        Generate HTMLResponse for payment redirect
        
        Args:
            payment_data: Payment data model
            
        Returns:
            FastAPI HTMLResponse
        """
        form_html = self.generate_payment_form(payment_data)
        return HTMLResponse(content=form_html)
    
    async def verify_itn(self, request: Request) -> PayFastITNData:
        """
        Verify ITN from PayFast
        
        Args:
            request: FastAPI request object
            
        Returns:
            Validated ITN data
            
        Raises:
            SignatureVerificationError: If signature is invalid
            InvalidMerchantError: If merchant ID doesn't match
        """
        # Get form data
        form_data = await request.form()
        data = dict(form_data)
        
        # Extract signature
        received_signature = data.get('signature')
        if not received_signature:
            raise SignatureVerificationError("Missing signature")
        
        # Create data dict for signature verification
        verification_data = {k: v for k, v in data.items() if k != 'signature'}
        
        # Verify signature
        calculated_signature = generate_signature(verification_data, self.config.passphrase)
        
        if calculated_signature != received_signature:
            raise SignatureVerificationError("Signature mismatch")
        
        # Verify merchant ID
        if data.get('merchant_id') != self.config.merchant_id:
            raise InvalidMerchantError(
                f"Merchant ID mismatch: expected {self.config.merchant_id}"
            )
        
        # Validate IP if enabled
        if self.config.validate_ip:
            client_ip = request.client.host if request.client else None
            if client_ip and client_ip not in self.config.valid_ips:
                # Log warning but don't reject (IP validation is optional)
                pass
        
        # Parse and return ITN data
        try:
            itn_data = PayFastITNData(**data)
            return itn_data
        except Exception as e:
            raise SignatureVerificationError(f"Invalid ITN data: {str(e)}")
    
    def validate_payment_amount(
        self,
        itn_data: PayFastITNData,
        expected_amount: float,
        tolerance: float = 0.01
    ) -> bool:
        """
        Validate payment amount
        
        Args:
            itn_data: ITN data from PayFast
            expected_amount: Expected payment amount
            tolerance: Acceptable difference (default 0.01)
            
        Returns:
            True if amounts match within tolerance
        """
        return abs(itn_data.amount_gross - expected_amount) <= tolerance
    
    def is_payment_successful(self, itn_data: PayFastITNData) -> bool:
        """
        Check if payment was successful
        
        Args:
            itn_data: ITN data from PayFast
            
        Returns:
            True if payment status is COMPLETE
        """
        return itn_data.payment_status == PaymentStatus.COMPLETE


