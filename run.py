from os import getenv
import requests
from time import sleep
from sys import exc_info
from cryptography import x509
import socket
import ssl
from datetime import datetime, timezone

URL = getenv('URL') or "https://example.com"
CONTAINS = getenv('CONTAINS') or ""
INTERVAL = int(getenv('INTERVAL') or 300)
TIMEOUT = int(getenv('TIMEOUT') or 3)
SSL_CERT_EXPIRY_DAYS = int(getenv('SSL_CERT_EXPIRY_DAYS') or 28)
NTFY_TOPIC = getenv('NTFY_TOPIC') or "SiteMonitor"


def main():
    lastStateOk = True
    while True:
        print(f"> {URL} ... ", end="", flush=True)
        error = checkSite(URL, CONTAINS)
        if error:
            print("Error:", error, flush=True)
            if lastStateOk:
                lastStateOk = False
                send_notification("Site error", f"{URL} - {error}", True)
        else:
            print("OK", flush=True)
            if not lastStateOk:
                lastStateOk = True
                send_notification("Site ok", f"{URL} OK")
        sleep(INTERVAL)


def checkSite(url: str, contains=""):
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        return "Request timeout"
    except:
        return exc_info()[1]
    if not contains in response.text:
        return f"Site does not contain '{contains}'"
    if "https://" in url:
        hostname = url.split("/")[2]
        days = ssl_cert_days_to_expiry(hostname)
        if days <= SSL_CERT_EXPIRY_DAYS:
            return f"The SSL certificate is expiring in {days} days"
    return False


def ssl_cert_days_to_expiry(hostname):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            data = ssock.getpeercert(True)
            pem_data = ssl.DER_cert_to_PEM_cert(data)
            cert_data = x509.load_pem_x509_certificate(str.encode(pem_data))
            days_to_expiry = (cert_data.not_valid_after_utc -
                              datetime.now(timezone.utc)).days
    return days_to_expiry


def send_notification(title: str, message: str, warning: bool = False):
    prio = "3"
    tag = "+1"
    if warning:
        prio = "5"
        tag = "warning"
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message,
            headers={"Title": title, "Priority": prio, "Tags": tag}
        )
        print("Notification sent", flush=True)
    except Exception as e:
        print(e, end=" ", flush=True)


if __name__ == "__main__":
    main()
