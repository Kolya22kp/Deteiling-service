import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import VehicleType, BodyPart, FilmType, AdditionalOption, DiscountTier, BodyZone, SelectedOption
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import BookingRequest, SelectedBodyPart
from .forms import BookingForm
from core.utils import send_email_notification, send_telegram_notification


def calculator_view(request):
    vehicle_types = list(
        VehicleType.objects.filter(is_active=True)
        .values('id', 'name', 'base_multiplier')
    )

    film_types = list(
        FilmType.objects.filter(is_active=True)
        .values('id', 'name', 'price_multiplier')
    )

    additional_options = list(
        AdditionalOption.objects.filter(is_active=True)
        .values('id', 'name', 'price_fixed', 'price_percent', 'applies_to_body_part')
    )
    for opt in additional_options:
        if opt['price_fixed']:
            opt['price_fixed'] = float(opt['price_fixed'])

    discount_tiers = [
        {
            'min_amount': float(t.min_amount),
            'max_amount': float(t.max_amount) if t.max_amount else None,
            'discount_percent': float(t.discount_percent)
        }
        for t in DiscountTier.objects.all()
    ]

    zones = BodyZone.objects.prefetch_related(
        'bodypart_set'
    ).filter(
        bodypart__is_active=True
    ).distinct()

    grouped_parts = {}
    base_prices = {}

    for zone in zones:
        parts_in_zone = zone.bodypart_set.filter(is_active=True)
        part_names = [part.name for part in parts_in_zone]
        if part_names:
            grouped_parts[zone.name] = part_names
            for part in parts_in_zone:
                base_prices[part.name] = float(part.base_price)

    context = {
        'vehicle_types': vehicle_types,
        'grouped_parts_json': json.dumps(grouped_parts, ensure_ascii=False),
        'base_prices_json': json.dumps(base_prices, ensure_ascii=False),
        'film_types': film_types,
        'additional_options': additional_options,
        'discount_tiers_json': json.dumps(discount_tiers, ensure_ascii=False),
        'booking_form': BookingForm(),
    }
    return render(request, 'pages/calculator.html', context)



@csrf_exempt
@require_POST
def submit_booking(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    form = BookingForm(data)

    if not form.is_valid():
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    data = form.cleaned_data

    try:
        booking = BookingRequest.objects.create(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            appointment_datetime=data['appointment_datetime'],
            comment=data.get('comment', ''),
            vehicle_type=VehicleType.objects.get(id=data['vehicle_type_id']),
            film_type=FilmType.objects.get(id=data['film_type_id']),
            total_price=data['total_price'],
            discount_applied=data.get('discount_applied', 0),
        )

        for part_name in data.get('selected_parts', []):
            body_part = BodyPart.objects.filter(name=part_name).first()
            if body_part:
                SelectedBodyPart.objects.create(booking=booking, body_part=body_part, quantity=1)

        for option_id in data.get('selected_options', []):
            option = AdditionalOption.objects.filter(id=option_id).first()
            if option:
                SelectedOption.objects.create(booking=booking, option=option)

        email_subject = "🚗 Новая заявка на оклейку"
        email_message = (
            f"Имя: {booking.name}\n"
            f"Телефон: {booking.phone}\n"
            f"Email: {booking.email or '—'}\n"
            f"Авто: {booking.vehicle_type.name}\n"
            f"Пленка: {booking.film_type.name}\n"
            f"Цена: {booking.total_price} ₽\n"
            f"Дата записи: {booking.appointment_datetime.strftime('%d.%m.%Y %H:%M') if booking.appointment_datetime else '—'}\n"
            f"Комментарий: {booking.comment or '—'}\n\n"
            f"Детали: {', '.join(sp.body_part.name for sp in booking.selected_parts.all()) or '—'}\n"
            f"Опции: {', '.join(so.option.name for so in booking.selected_options.all()) or '—'}"
        )

        from core.utils import format_booking_for_telegram, send_telegram_notification

        telegram_text = format_booking_for_telegram(booking)

        send_telegram_notification(telegram_text)
        send_email_notification(email_subject, email_message)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)