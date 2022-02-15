from django.forms import ModelForm
from .models import Summary
from django import forms
from captcha.fields import CaptchaField


class SummaryForm(ModelForm):
    class Meta:
        model = Summary
        fields = ['name', 'inputData']


class MyForm(forms.Form):
   captcha=CaptchaField()