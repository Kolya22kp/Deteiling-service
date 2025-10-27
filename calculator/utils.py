import requests
from django.core.mail import send_mail
from decouple import config

from deteiling import settings
from ..core.models import Settings

def send_email_notification(subject: str, message: str):
    try:
        site_settings = Settings.load()
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[site_settings.salon_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


def send_telegram_notification(text: str):
    try:
        site_settings = Settings.load()
        url = f"https://api.telegram.org/bot{config("TELEGRAM_BOT_TOKEN")}/sendMessage"
        payload = {
            'chat_id': config("TELEGRAM_CHAT_ID"),
            'text': text,
            'parse_mode': 'MarkdownV2',
            'disable_web_page_preview': True,
        }
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False