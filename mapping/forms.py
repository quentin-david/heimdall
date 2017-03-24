from django import forms
from django.forms import ModelChoiceField
from .models import Application, Host, Node, Network, NetworkLink
from .models import ServiceWebServer, ServiceReverseProxy, ServiceDatabase, Service
from django.forms import formset_factory

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
        fields = ['description', 'short_description', 'application', 'munin_server', 'collect_profile','managed_by_heimdall']

class NodeFullForm(forms.ModelForm):
    class Meta:
        model = Node
        #fields = '__all__'
        exclude = ['application', 'foreman_status_label']
    
    #def __init__(self, *args, **kwargs):
        #super(NodeFullForm, self).__init__(*args, **kwargs)
        #network_list = Network.objects.all() # QT test to display NetworkLink in the form
        #NetworkLinkFormFormset = formset_factory(NetworkLinkForm)
        #self.fields['network_links'].widget = NetworkLinkFormFormset()
       
class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = '__all__'

class NetworkLinkForm(forms.ModelForm):
    class Meta:
        model = NetworkLink
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
        
        