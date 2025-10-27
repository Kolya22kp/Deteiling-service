import requests
from decouple import config
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import Settings
from typing import TYPE_CHECKING
from datetime import datetime


def send_email_notification(subject: str, message: str):
    try:
        site_settings = Settings.load()
        send_mail(
            subject=subject,
            message=message,
            from_email=django_settings.DEFAULT_FROM_EMAIL,
            recipient_list=[site_settings.salon_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


def send_telegram_notification(text: str):
    try:
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

if TYPE_CHECKING:
    from .models import CallbackRequest, BookingRequest



def escape_markdown_v2(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)

    escape_chars = r'_*[]()~`>#+-=|{}.!'
    for char in escape_chars:
        text = text.replace(char, '\\' + char)

    return text


def format_datetime(dt: datetime) -> str:
    formatted = dt.strftime('%d.%m.%Y %H:%M')
    return escape_markdown_v2(formatted)


def format_callback_for_telegram(callback: 'CallbackRequest') -> str:
    name = escape_markdown_v2(callback.name)
    phone = escape_markdown_v2(callback.phone)
    created = format_datetime(callback.created_at)

    message = f"""\
📞 *Новая заявка на звонок*

👤 {name}
📱 `{phone}`
🕒 {created}"""

    return message


def format_booking_for_telegram(booking: 'BookingRequest') -> str:
    name = escape_markdown_v2(booking.name)
    phone = escape_markdown_v2(booking.phone)

    message = f"""\
🚗 *Новая заявка на оклейку*

👤 {name}
📱 `{phone}`"""

    if booking.email:
        email = escape_markdown_v2(booking.email)
        message += f"\n✉️ {email}"

    vehicle_type = escape_markdown_v2(booking.vehicle_type.name)
    film_type = escape_markdown_v2(booking.film_type.name)

    message += f"""
🚘 {vehicle_type}
🎞 {film_type}"""

    price_str = f"{int(booking.total_price):,}".replace(',', ' ')
    price_escaped = escape_markdown_v2(price_str)
    message += f"\n💰 *{price_escaped}* ₽"

    if booking.appointment_datetime:
        appointment = format_datetime(booking.appointment_datetime)
        message += f"\n📅 {appointment}"

    selected_parts = booking.selected_parts.all()
    if selected_parts.exists():
        message += "\n\n🛠 *Выбранные детали:*"
        for part in selected_parts:
            part_name = escape_markdown_v2(part.body_part.name)
            message += f"\n— {part_name}"

    selected_options = booking.selected_options.all()
    if selected_options.exists():
        message += "\n\n🛠 *Доп\\. услуги:*"
        for option in selected_options:
            option_name = escape_markdown_v2(option.option.name)
            message += f"\n— {option_name}"

    if booking.comment:
        comment = escape_markdown_v2(booking.comment)
        message += f"""

📝 *Комментарий:*
{comment}"""

    return message
