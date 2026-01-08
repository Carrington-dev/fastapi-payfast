"""Basic usage example"""

from fastapi import FastAPI, Request
from datetime import datetime

from fastapi_payfast import (
    PayFastClient,
    PayFastConfig,
    PayFastPaymentData,
    PaymentStatus,
    SignatureVerificationError,
    InvalidMerchantError
)

# Initialize FastAPI app
app = FastAPI(title="PayFast Integration Example")

# Configure PayFast (use environment variables in production)
config = PayFastConfig(
    merchant_id="10000100",
    merchant_key="46f0cd694581a",
    passphrase="jt7NOE43FZPn",
    sandbox=True
)

# Initialize PayFast client
payfast = PayFastClient(config)


@app.post("/checkout")
async def create_checkout(
    amount: float,
    item_name: str,
    item_description: str = None,
    customer_email: str = None
):
    """Create a payment checkout"""
    
    # Create payment data
    payment_data = PayFastPaymentData(
        merchant_id=config.merchant_id,
        merchant_key=config.merchant_key,
        amount=amount,
        item_name=item_name,
        item_description=item_description,
        email_address=customer_email,
        return_url="https://yoursite.com/payment/success",
        cancel_url="https://yoursite.com/payment/cancel",
        notify_url="https://yoursite.com/payment/notify",
        m_payment_id=f"ORDER-{int(datetime.now().timestamp())}"
    )
    
    # Return HTML response that redirects to PayFast
    return payfast.generate_payment_response(payment_data)


@app.post("/payment/notify")
async def payment_notification(request: Request):
    """Handle ITN (Instant Transaction Notification) from PayFast"""
    
    try:
        # Verify and parse ITN data
        itn_data = await payfast.verify_itn(request)
        
        # Check if payment was successful
        if payfast.is_payment_successful(itn_data):
            # Validate amount (if you have stored order data)
            # expected_amount = get_order_amount(itn_data.m_payment_id)
            # if not payfast.validate_payment_amount(itn_data, expected_amount):
            #     return {"status": "error", "message": "Amount mismatch"}
            
            # Process successful payment
            print(f"✓ Payment successful!")
            print(f"  PayFast Payment ID: {itn_data.pf_payment_id}")
            print(f"  Order ID: {itn_data.m_payment_id}")
            print(f"  Amount: R{itn_data.amount_gross:.2f}")
            print(f"  Fee: R{itn_data.amount_fee:.2f}")
            print(f"  Net: R{itn_data.amount_net:.2f}")
            
            # Update your database, send confirmation email, etc.
            # update_order_status(itn_data.m_payment_id, "paid")
            # send_confirmation_email(itn_data.email_address)
            
        elif itn_data.payment_status == PaymentStatus.FAILED:
            print(f"✗ Payment failed for order {itn_data.m_payment_id}")
            # Handle failed payment
            
        elif itn_data.payment_status == PaymentStatus.CANCELLED:
            print(f"✗ Payment cancelled for order {itn_data.m_payment_id}")
            # Handle cancelled payment
        
        # Always return success to PayFast
        return {"status": "ok"}
        
    except (SignatureVerificationError, InvalidMerchantError) as e:
        print(f"✗ Payment verification failed: {e.message}")
        return {"status": "error", "message": e.message}


@app.get("/payment/success")
async def payment_success():
    """Handle successful payment return"""
    return {
        "message": "Payment successful! Thank you for your purchase.",
        "status": "success"
    }


@app.get("/payment/cancel")
async def payment_cancel():
    """Handle cancelled payment return"""
    return {
        "message": "Payment was cancelled.",
        "status": "cancelled"
    }