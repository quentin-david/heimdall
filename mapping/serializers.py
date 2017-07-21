from rest_framework import serializers
#from ember_drf.serializers import SideloadSerializer
from .models import Application

#from rest_framework.compat import OrderedDict

#class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name', 'description', 'identifier')
        
#class ApplicationsSideloadSerializer(SideloadSerializer):
    #class Meta:
        #base_serializer = ApplicationSerializer