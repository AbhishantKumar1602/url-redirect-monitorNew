from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from email.mime.text import MIMEText
import smtplib, time, os

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"),
    options=chrome_options
)

YOUR_EMAIL = os.getenv("YOUR_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SEND_TO = os.getenv("SEND_TO")

def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = YOUR_EMAIL
    msg["To"] = SEND_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.sendmail(YOUR_EMAIL, SEND_TO, msg.as_string())


START = 435
END = 437
BASE_URL = "https://ultimateskincaretips.com/landpage.php?mn="

for mn in range(START, END + 1):
    url = f"{BASE_URL}{mn}"
    print(f"Checking: {url}")

    try:
        driver.get(url)
        time.sleep(10)
        final_url = driver.current_url

        if final_url != url:
            print(f"FOUND HIT! mn={mn}")
            print("Final URL:", final_url)

            subject = f"[HIT FOUND] mn={mn}"
            message = f"mn={mn}\nOriginal: {url}\nRedirected to: {final_url}"
            send_email(subject, message)
        else:
            print("No redirect.")

    except Exception as e:
        print("Error:", e)

driver.quit()
