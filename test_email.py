#!/usr/bin/env python3
"""
Simple test script to verify email functionality.
Run this before using the main bot to ensure email settings work.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email():
    """Test email functionality."""
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    
    if not all([sender_email, sender_password, receiver_email]):
        print("❌ Missing email configuration. Please check your .env file.")
        return False
    
    try:
        print("📧 Testing email configuration...")
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "🧪 Prenotami Bot - Test Email"
        
        body = f"""
        <html>
        <body>
            <h2>Email Configuration Test</h2>
            <p>This is a test email from your Prenotami Bot.</p>
            <p><strong>Sent at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>If you received this email, your configuration is working correctly!</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        print(f"📤 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print("🔐 Authenticating...")
        server.login(sender_email, sender_password)
        
        print("📮 Sending test email...")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        print(f"✅ Test email sent successfully to {receiver_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {str(e)}")
        return False

if __name__ == "__main__":
    if test_email():
        print("\n✅ Email configuration is working! You can now run the main bot.")
    else:
        print("\n❌ Please fix the email configuration before running the main bot.")
