"""PayFast utility functions"""

import hashlib
import urllib.parse
from typing import Dict, Any, Optional


def generate_signature(data: Dict[str, Any], passphrase: Optional[str] = None) -> str:
    """
    Generate MD5 signature for PayFast
    
    Args:
        data: Dictionary of payment data
        passphrase: Optional passphrase for additional security
        
    Returns:
        MD5 hash signature
    """
    # Create parameter string
    param_string = ""
    for key in sorted(data.keys()):
        if key != 'signature' and data[key] is not None and data[key] != '':
            param_string += f"{key}={urllib.parse.quote_plus(str(data[key]))}&"
    
    # Remove last ampersand
    param_string = param_string.rstrip('&')
    
    # Add passphrase if provided
    if passphrase:
        param_string += f"&passphrase={urllib.parse.quote_plus(passphrase)}"
    
    # Generate and return signature
    return hashlib.md5(param_string.encode()).hexdigest()


def generate_payment_form_html(action_url: str, data: Dict[str, Any]) -> str:
    """
    Generate HTML form for payment submission
    
    Args:
        action_url: PayFast process URL
        data: Payment data dictionary
        
    Returns:
        HTML string with auto-submitting form
    """
    form_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Processing Payment - PayFast</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 400px;
            width: 90%;
        }}
        h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 24px;
        }}
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 30px auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        p {{
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }}
        .logo {{
            margin-bottom: 20px;
            font-size: 16px;
            color: #667eea;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🔒 Secure Payment</div>
        <h2>Redirecting to PayFast</h2>
        <div class="spinner"></div>
        <p>Please wait while we securely redirect you to the payment page.</p>
        <p style="margin-top: 10px; font-size: 12px; color: #999;">Do not refresh this page.</p>
        <form id="payfast_form" action="{action_url}" method="POST">
"""
    
    for key, value in data.items():
        form_html += f'            <input type="hidden" name="{key}" value="{value}">\n'
    
    form_html += """        </form>
        <script>
            document.getElementById('payfast_form').submit();
        </script>
    </div>
</body>
</html>"""
    
    return form_html
