from django import forms
from .models import Enlace


class ShortenerForm(forms.ModelForm):
    class Meta:
        model = Enlace
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'input is-rounded is-medium', 'placeholder': 'URL'})
        }
