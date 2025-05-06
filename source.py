import scapy.all as scapy
import socket
import nmap
import time
import logging
from datetime import datetime
import smtplib
from email.message import EmailMessage
from twilio.rest import Client  
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

logging.basicConfig(filename='device_log.txt', level=logging.INFO)

# Dictionary of known MAC addresses
KNOWN_DEVICES = {
    '00:11:22:33:44:55': 'My Laptop',
    'aa:bb:cc:dd:ee:ff': 'Office Printer'
}

# Email and Twilio config from environment variables
ALERT_EMAIL = os.getenv('ALERT_EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
FROM_WHATSAPP = os.getenv('FROM_WHATSAPP')
TO_WHATSAPP = os.getenv('TO_WHATSAPP')

def send_email_alert(device_info):
    msg = EmailMessage()
    msg.set_content(f"New device detected:\n\n{device_info}")
    msg['Subject'] = '⚠️ New Network Device Alert'
    msg['From'] = ALERT_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(ALERT_EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("[ALERT] Email sent!")
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")

def send_whatsapp_alert(device_info):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"📢 New device detected on your network:\n{device_info}",
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        print("[ALERT] WhatsApp message sent!")
    except Exception as e:
        print(f"[ERROR] WhatsApp alert failed: {e}")

def get_vendor(mac):
    try:
        nm = nmap.PortScanner()
        vendor = nm.scanmac(mac)
        return vendor
    except:
        return "Unknown Vendor"

def get_device_name(ip):
    try:
        name = socket.gethostbyaddr(ip)[0]
        return name
    except socket.herror:
        return "Unknown Device"

def scan(ip_range):
    arp_req = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered = scapy.srp(arp_req_broadcast, timeout=2, verbose=False)[0]

    devices = []
    for element in answered:
        ip = element[1].psrc
        mac = element[1].hwsrc
        name = get_device_name(ip)
        devices.append({
            "ip": ip,
            "mac": mac,
            "name": name
        })
    return devices

def monitor_network(ip_range):
    seen_macs = set()
    print("🔍 Starting network scan...")
    while True:
        devices = scan(ip_range)
        for device in devices:
            ip = device['ip']
            mac = device['mac']
            name = device['name']
            manufacturer = get_vendor(mac)
            device_info = f"{datetime.now()} | Name: {name} | IP: {ip} | MAC: {mac} | Manufacturer: {manufacturer}"

            if mac not in seen_macs:
                print(f"🆕 New Device Found: {device_info}")
                logging.info(device_info)
                seen_macs.add(mac)

                if mac not in KNOWN_DEVICES:
                    send_email_alert(device_info)
                    send_whatsapp_alert(device_info)
            else:
                print(f"✔️ Active: {name} ({ip}) [{mac}]")
        time.sleep(30)

if __name__ == "__main__":
    target_range = "10.1.160.0/19"  # Change this as per your network
    monitor_network(target_range)
