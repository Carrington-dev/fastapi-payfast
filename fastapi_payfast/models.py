"""PayFast data models"""

from typing import Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field, validator, HttpUrl


class PaymentStatus(str, Enum):
    """PayFast payment status codes"""
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"


class SubscriptionType(int, Enum):
    """Subscription type codes"""
    SUBSCRIPTION = 1
    ADHOC = 2


class FrequencyType(int, Enum):
    """Payment frequency codes"""
    MONTHLY = 3
    QUARTERLY = 4
    BIANNUAL = 5
    ANNUAL = 6


class PayFastPaymentData(BaseModel):
    """PayFast payment request data model"""
    
    # Required fields
    merchant_id: str
    merchant_key: str
    amount: float = Field(..., gt=0, description="Payment amount in ZAR")
    item_name: str = Field(..., min_length=1, max_length=100)
    
    # Optional transaction details
    item_description: Optional[str] = Field(None, max_length=255)
    
    # URLs
    return_url: Optional[HttpUrl] = None
    cancel_url: Optional[HttpUrl] = None
    notify_url: Optional[HttpUrl] = None
    
    # Buyer information
    name_first: Optional[str] = Field(None, max_length=100)
    name_last: Optional[str] = Field(None, max_length=100)
    email_address: Optional[str] = Field(None, max_length=100)
    cell_number: Optional[str] = Field(None, max_length=20)
    
    # Custom fields
    m_payment_id: Optional[str] = Field(None, description="Unique payment ID")
    custom_str1: Optional[str] = Field(None, max_length=255)
    custom_str2: Optional[str] = Field(None, max_length=255)
    custom_str3: Optional[str] = Field(None, max_length=255)
    custom_str4: Optional[str] = Field(None, max_length=255)
    custom_str5: Optional[str] = Field(None, max_length=255)
    custom_int1: Optional[int] = None
    custom_int2: Optional[int] = None
    custom_int3: Optional[int] = None
    custom_int4: Optional[int] = None
    custom_int5: Optional[int] = None
    
    # Subscription fields
    subscription_type: Optional[SubscriptionType] = None
    billing_date: Optional[str] = Field(None, description="Format: YYYY-MM-DD")
    recurring_amount: Optional[float] = Field(None, gt=0)
    frequency: Optional[FrequencyType] = None
    cycles: Optional[int] = Field(None, ge=0, description="0 for infinite")
    
    # Email confirmation
    email_confirmation: Optional[Literal[0, 1]] = None
    confirmation_address: Optional[str] = Field(None, max_length=100)
    
    @validator('amount', 'recurring_amount')
    def round_amount(cls, v):
        """Round amounts to 2 decimal places"""
        if v is not None:
            return round(v, 2)
        return v
    
    class Config:
        use_enum_values = True


class PayFastITNData(BaseModel):
    """PayFast ITN (Instant Transaction Notification) data model"""
    
    m_payment_id: Optional[str] = None
    pf_payment_id: str
    payment_status: PaymentStatus
    item_name: str
    item_description: Optional[str] = None
    amount_gross: float
    amount_fee: float
    amount_net: float
    
    # Custom fields
    custom_str1: Optional[str] = None
    custom_str2: Optional[str] = None
    custom_str3: Optional[str] = None
    custom_str4: Optional[str] = None
    custom_str5: Optional[str] = None
    custom_int1: Optional[int] = None
    custom_int2: Optional[int] = None
    custom_int3: Optional[int] = None
    custom_int4: Optional[int] = None
    custom_int5: Optional[int] = None
    
    # Buyer details
    name_first: Optional[str] = None
    name_last: Optional[str] = None
    email_address: Optional[str] = None
    
    # Merchant verification
    merchant_id: str
    signature: str
    
    class Config:
        use_enum_values = True

