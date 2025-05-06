
# 🔍 Network Device Monitor with Email & WhatsApp Alerts

This Python project scans your local network for connected devices and alerts you when an unknown device joins. It uses email and WhatsApp notifications to instantly inform you of any new device detected.

---

## 🚀 Features

- Scans a defined IP range to detect devices.
- Logs all detected devices with timestamps.
- Sends alerts via:
  - 📧 Email (Gmail)
  - 📲 WhatsApp (via Twilio)
- Keeps a list of known devices to avoid duplicate alerts.
- Easy-to-configure via `.env` file (no secrets in code!).

---

## 🛠️ Technologies Used

- [Scapy](https://scapy.net/) – for ARP network scanning
- [Python Nmap](https://pypi.org/project/python-nmap/) – for vendor info
- [Socket](https://docs.python.org/3/library/socket.html) – to resolve hostnames
- [Twilio API](https://www.twilio.com/docs/whatsapp) – for WhatsApp messaging
- [smtplib + email.message](https://docs.python.org/3/library/email.message.html) – for email alerts
- [dotenv](https://pypi.org/project/python-dotenv/) – for environment variable management

---

## 📁 Sample `.env` File

Create a file named `.env` in the root directory of your project and add your credentials as shown:

```env
ALERT_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
TO_EMAIL=recipient_email@gmail.com

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
FROM_WHATSAPP=whatsapp:+14155238886
TO_WHATSAPP=whatsapp:+91xxxxxxxxxx
```

> ⚠️ Make sure you use an **App Password** if you have 2FA enabled on your Gmail account.

---

## ▶️ Usage

Update the target IP range in the Python script if needed:

```python
target_range = "192.168.1.0/24"
```

Then run the script:

```bash
python monitor.py
```
