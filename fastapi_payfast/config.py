"""PayFast configuration module"""

from typing import Optional
from pydantic import BaseModel, Field


class PayFastConfig(BaseModel):
    """PayFast configuration settings"""
    
    merchant_id: str = Field(..., description="PayFast merchant ID")
    merchant_key: str = Field(..., description="PayFast merchant key")
    passphrase: str = Field(..., description="PayFast passphrase for security")
    sandbox: bool = Field(default=True, description="Use sandbox environment")
    validate_ip: bool = Field(default=True, description="Validate PayFast IP addresses")
    
    class Config:
        frozen = True  # Make config immutable
    
    @property
    def process_url(self) -> str:
        """Get the appropriate PayFast process URL"""
        if self.sandbox:
            return "https://sandbox.payfast.co.za/eng/process"
        return "https://www.payfast.co.za/eng/process"
    
    @property
    def validate_url(self) -> str:
        """Get the appropriate PayFast validation URL"""
        if self.sandbox:
            return "https://sandbox.payfast.co.za/eng/query/validate"
        return "https://www.payfast.co.za/eng/query/validate"
    
    @property
    def valid_ips(self) -> list[str]:
        """Get list of valid PayFast IP addresses"""
        return [
            "197.97.145.144",
            "41.74.179.194",
        ]

