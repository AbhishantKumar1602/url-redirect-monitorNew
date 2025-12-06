import requests
import smtplib
from email.mime.text import MIMEText

# -----------------------------
# EMAIL CONFIG
# -----------------------------
YOUR_EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "your_app_password_here"  # 16-char Gmail App Password
SEND_TO = "yourgmail@gmail.com"

def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = YOUR_EMAIL
    msg['To'] = SEND_TO
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(YOUR_EMAIL, APP_PASSWORD)
            server.sendmail(YOUR_EMAIL, SEND_TO, msg.as_string())
        print("Email Sent!")
    except Exception as e:
        print("Email Failed:", e)

# -----------------------------
# URL MONITORING CONFIG
# -----------------------------
START = 1
END = 1000
BASE_URL = "https://ultimateskincaretips.com/landpage.php?mn="

for mn in range(START, END + 1):
    url = f"{BASE_URL}{mn}"
    print(f"Checking: {url}")

    try:
        r = requests.get(url, timeout=10, allow_redirects=True)
        final_url = r.url

        if final_url != url:
            print(f"HIT FOUND! mn={mn} -> {final_url}")
            subject = f"[HIT FOUND] mn={mn}"
            message = f"mn={mn}\nOriginal: {url}\nRedirected to: {final_url}"
            send_email(subject, message)

    except Exception as e:
        print(f"Error for mn={mn}: {e}")
