from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import Nextcloud
import easywebdav

def nextcloudHome(request):
    nextcloud = Nextcloud
    webdav = easywebdav.connect(nextcloud.domain, username=nextcloud.user, password=nextcloud.password, protocol=nextcloud.protocol, port='80')
    file_list = webdav.ls("/nextcloud/remote.php/webdav/")
    return render(request, 'nextcloud/nextcloud_home.html', locals())

"""
def fileDownload(request):
    nextcloud = Nextcloud
    webdav = easywebdav.connect(nextcloud.domain, username=nextcloud.user, password=nextcloud.password, protocol=nextcloud.protocol, port='80')
    file_name = request.GET.get('file_name')
    file_get = webdav.download(file_name)
    
    response = HttpResponse(file_get,content_type="image/png")
    return response
"""