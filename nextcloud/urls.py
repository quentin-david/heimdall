from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
#from .models import Nextcloud

urlpatterns = [
    url(r'^$', views.documentHome, name='document_home'),
    #url(r'file', views.fileDownload, name='nextcloud_file_download'),
]