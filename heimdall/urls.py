"""heimdall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf.urls.static import static #test PJ Notes
from django.conf import settings # test PJ Notes
from django.contrib import admin
from appli import views
from mapping import views
from deployment import views
from poc_sport import views
from bugzilla import views
from nextcloud import views
from notes import views
from collect import views
from visio import views
from rest_framework.authtoken.views import obtain_auth_token # essai DRF

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), #tests DRF
    url(r'^', include('appli.urls')),
    url(r'^map/', include('mapping.urls')),
    url(r'^monitoring/', include('monitoring.urls')),
    url(r'^deployment/', include('deployment.urls')),
    url(r'^poc_sport/', include('poc_sport.urls')),
    url(r'^bugzilla/', include('bugzilla.urls')),
    url(r'^nextcloud/', include('nextcloud.urls')),
    url(r'^notes/', include('notes.urls')),
    url(r'^collect/', include('collect.urls')),
    url(r'^visio/', include('visio.urls')),
    url(r'^api-auth-token/', obtain_auth_token), # essai DRF - Ember
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
