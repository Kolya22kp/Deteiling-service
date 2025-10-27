import json

from django.shortcuts import render
from .models import ImageGallery, Privacypolicy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import CallbackRequest
from .forms import CallbackForm
from .utils import send_email_notification, send_telegram_notification, format_callback_for_telegram

# Create your views here.
def index_view(request):
    context = {
        "images": ImageGallery.objects.all()
    }
    return render(request, "pages/index.html", context=context)


def about_us_view(request):
    return render(request, 'pages/about_us.html', {'callback_form': CallbackForm()})

def privacy_policy_view(request):
    p = Privacypolicy.objects.latest('id').privacy_policy
    lines = []
    for item in p.split('\n'):
        if not item.strip():
            lines.append({"type": "empty"})
        elif item.startswith("[T]"):
            lines.append({"type": "title", "text": item[3:].strip()})
        else:
            lines.append({"type": "paragraph", "text": item.strip()})

    context = {
        'policy_lines_json': json.dumps(lines, ensure_ascii=False),
        'updated_at': Privacypolicy.objects.latest('id').updated_at
    }

    return render(request, "pages/privacy_policy.html", context)



@csrf_protect
@require_POST
def submit_callback(request):
    form = CallbackForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


    name = form.cleaned_data['name']
    phone = form.cleaned_data['phone']

    callback = CallbackRequest.objects.create(name=name, phone=phone)

    # email_subject = "📞 Новая заявка на обратный звонок"
    # email_message = (
    #     f"Имя: {callback.name}\n"
    #     f"Телефон: {callback.phone}\n"
    #     f"Дата: {callback.created_at.strftime('%d.%m.%Y %H:%M')}"
    # )
    telegram_text = format_callback_for_telegram(callback)
    send_telegram_notification(telegram_text)
    # send_email_notification(email_subject, email_message)

    return JsonResponse({'success': True})
