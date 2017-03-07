from django import forms
from .models import Foreman

class ForemanForm(forms.ModelForm):
    class Meta:
        model = Foreman
        fields = '__all__'