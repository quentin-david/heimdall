from django import forms
from .models import CollectProfile, CollectItem


class CollectProfileForm(forms.ModelForm):
    class Meta:
        model = CollectProfile
        fields = '__all__'
     
class CollectItemForm(forms.ModelForm):
    class Meta:
        model = CollectItem
        fields = '__all__'
