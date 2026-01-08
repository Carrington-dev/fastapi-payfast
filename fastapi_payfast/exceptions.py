"""PayFast custom exceptions"""

from fastapi import HTTPException, status


class PayFastException(Exception):
    """Base exception for PayFast operations"""
    pass


class SignatureVerificationError(PayFastException):
    """Raised when signature verification fails"""
    
    def __init__(self, message: str = "Invalid signature"):
        self.message = message
        super().__init__(self.message)
    
    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.message
        )


class InvalidMerchantError(PayFastException):
    """Raised when merchant ID doesn't match"""
    
    def __init__(self, message: str = "Invalid merchant ID"):
        self.message = message
        super().__init__(self.message)
    
    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.message
        )


class InvalidAmountError(PayFastException):
    """Raised when payment amount doesn't match expected"""
    
    def __init__(self, expected: float, received: float):
        self.expected = expected
        self.received = received
        self.message = f"Amount mismatch: expected {expected}, received {received}"
        super().__init__(self.message)
    
    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.message
        )