
from django import forms

class DigitUploadForm(forms.Form):
    digit_image = forms.ImageField()
