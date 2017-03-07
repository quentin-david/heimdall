from django import forms
from .models import Bugzilla
from django.contrib.auth.models import User
from mapping.models import Application

class BugzillaForm(forms.ModelForm):
    class Meta:
        model = Bugzilla
        #fields = '__all__'
        exclude = ['owner']

class BugzillaSearchForm(forms.Form):
    qs_title = forms.CharField(max_length=10,required=False,widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    qs_owner = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    qs_application = forms.ModelChoiceField(queryset=Application.objects.all(),required=False)
    states = (('','--------'),('open','Open'),('close', 'Close'),('info','Info'),)
    qs_state = forms.ChoiceField(choices=states,required=False)