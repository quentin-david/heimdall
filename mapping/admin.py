from django.contrib import admin
from .models import Application, Host, Node, Network, Service

admin.site.register(Application)
admin.site.register(Host)
admin.site.register(Node)
admin.site.register(Network)
admin.site.register(Service)
