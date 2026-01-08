"""Basic usage example"""

import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from dotzen import config
from fastapi_payfast import (
    PayFastClient,
    PayFastConfig,
    PayFastPaymentData,
    PaymentStatus,
    SignatureVerificationError,
    InvalidMerchantError
)




BASE_SITE = "localhost:8000"  # Replace with your domain

# Initialize PayFast client
payfast = PayFastClient(config)




# Initialize FastAPI app
app = FastAPI(
    title="PayFast Integration Example",
    description="Complete PayFast payment integration with FastAPI",
    version="1.0.0"
)

# Configure PayFast from environment variables or defaults
config = PayFastConfig(
    merchant_id=config("PAYFAST_MERCHANT_ID", "10000100"),
    merchant_key=config("PAYFAST_MERCHANT_KEY", "46f0cd694581a"),
    passphrase=config("PAYFAST_PASSPHRASE", "jt7NOE43FZPn"),
    sandbox=config("PAYFAST_SANDBOX", True, cast=bool) == True,
)

# Initialize PayFast client
payfast = PayFastClient(config)


@app.get("/")
async def home():
    """Home page with payment form"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PayFast Payment Demo</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 500px;
                width: 100%;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 28px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 500;
                font-size: 14px;
            }
            input, textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            textarea {
                resize: vertical;
                min-height: 80px;
            }
            .btn {
                width: 100%;
                padding: 14px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            .btn:active {
                transform: translateY(0);
            }
            .info-box {
                background: #f0f4ff;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin-bottom: 25px;
                border-radius: 4px;
                font-size: 13px;
                color: #555;
            }
            .required {
                color: #e74c3c;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛒 PayFast Payment</h1>
            <p class="subtitle">Secure payment processing with PayFast</p>
            
            <div class="info-box">
                ℹ️ This is a <strong>sandbox environment</strong>. No real charges will be made.
            </div>
            
            <form action="/checkout" method="post">
                <div class="form-group">
                    <label for="amount">Amount (ZAR) <span class="required">*</span></label>
                    <input type="number" id="amount" name="amount" step="0.01" min="0.01" 
                           placeholder="e.g. 99.99" required value="123.00">
                </div>
                
                <div class="form-group">
                    <label for="item_name">Item Name <span class="required">*</span></label>
                    <input type="text" id="item_name" name="item_name" 
                           placeholder="e.g. Product Name" required value="Donation">
                </div>
                
                <div class="form-group">
                    <label for="item_description">Description</label>
                    <textarea id="item_description" name="item_description" 
                              placeholder="Brief description of the purchase">Donation to PayFast</textarea>
                </div>
                
                <div class="form-group">
                    <label for="customer_email">Email Address</label>
                    <input type="email" id="customer_email" name="customer_email" 
                           placeholder="your@email.com" value="customer@example.com">
                </div>
                
                <button type="submit" class="btn">
                    Proceed to Payment →
                </button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)




@app.get("/checkout")
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
        return_url=f"https://{ BASE_SITE }/payment/success",
        cancel_url=f"https://{ BASE_SITE }/payment/cancel",
        notify_url=f"https://{ BASE_SITE }/payment/notify",
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