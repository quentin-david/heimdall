from django import forms
from .models import Munin

class MuninForm(forms.ModelForm):
    class Meta:
        model = Munin
        fields = '__all__'