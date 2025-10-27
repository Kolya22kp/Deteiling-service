from captcha.fields import CaptchaField
from django import forms

class CallbackForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    captcha = CaptchaField(label="Подтвердите, что вы не робот")