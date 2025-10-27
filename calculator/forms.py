from captcha.fields import CaptchaField
from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    vehicle_type_id = forms.IntegerField()
    film_type_id = forms.IntegerField()
    selected_parts = forms.JSONField()
    selected_options = forms.JSONField(required=False)
    total_price = forms.DecimalField(max_digits=12, decimal_places=2)
    discount_applied = forms.FloatField()
    comment = forms.CharField(required=False)
    appointment_datetime = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M']
    )
    captcha = CaptchaField(label="Подтвердите, что вы не робот")