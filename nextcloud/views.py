from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from notes.models import NotesFile, Category
from os import listdir
from os.path import isfile, join
from django.conf import settings


"""
def nextcloudHome(request):
    nextcloud = Nextcloud
    webdav = easywebdav.connect(nextcloud.domain, username=nextcloud.user, password=nextcloud.password, protocol=nextcloud.protocol, port='80')
    file_list = webdav.ls("/nextcloud/remote.php/webdav/")
    return render(request, 'nextcloud/nextcloud_home.html', locals())

"""

def documentHome(request):
    #if not request.user.username == 'david':
        #return redirect('home')
    #topic_list = [ topic for topic in Category.objects.all() ]
    topic_list = Category.get_subcategories_by_user(request.user)
    media_url = settings.MEDIA_URL
    
    return render(request, 'nextcloud/nextcloud_home.html', locals())