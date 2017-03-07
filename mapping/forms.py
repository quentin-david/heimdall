from django import forms
from django.forms import ModelChoiceField
from .models import Application, Host, Node, Network
from .models import ServiceWebServer, ServiceReverseProxy, ServiceDatabase, Service

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = '__all__'

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['description', 'short_description', 'application', 'munin_server', 'collect_profile']
        
class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = '__all__'
        
"""
Services
"""
# Abstract model
class ServiceForm(forms.ModelForm):        
    def __init__(self, *args, **kwargs):
        self.appli = kwargs.pop('application', None)
        super(ServiceForm, self).__init__(*args,**kwargs)
        self.fields['node'].queryset = Node.objects.filter(application=self.appli)

class ServiceWebServerForm(ServiceForm):
    class Meta:
        model = ServiceWebServer
        exclude = ['application']

class ServiceReverseProxyForm(ServiceForm):
    class Meta:
        model = ServiceReverseProxy
        exclude = ['application']
        
class ServiceDatabaseForm(ServiceForm):
    class Meta:
        model = ServiceDatabase
        exclude = ['application']
        
        