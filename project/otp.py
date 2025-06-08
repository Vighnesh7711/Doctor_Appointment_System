

import yagmail

# Your Gmail credentials
email = "studynotes132@gmail.com"
password = "bief icvs zbpc rdti"  # Generated from Google App Passwords

# User's phone number to send SMS
phone_number = "919421539013"

# Carrier SMS Gateway (For Jio)
sms_gateway = f"{phone_number}@sms.jio.com"  # For Airtel, Vi, or BSNL, I'll tell the gateway below 👇

# Message content
message = "Your OTP is 123456. Please do not share it with anyone."

# Sending SMS via Gmail
yag = yagmail.SMTP(email, password)
yag.send(to=sms_gateway, subject="", contents=message)

print("SMS sent successfully from your number!")