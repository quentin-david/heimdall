from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
#from .models import Nextcloud
#import easywebdav
from os import listdir
from os.path import isfile, join


"""
def nextcloudHome(request):
    nextcloud = Nextcloud
    webdav = easywebdav.connect(nextcloud.domain, username=nextcloud.user, password=nextcloud.password, protocol=nextcloud.protocol, port='80')
    file_list = webdav.ls("/nextcloud/remote.php/webdav/")
    return render(request, 'nextcloud/nextcloud_home.html', locals())

"""

def nextcloudHome(request):
    path = '/var/www/html/heimdall/media/nextcloud/david/Library'
    #file_list = [f for f in listdir(path) if isfile(join(path, f))]
    file_list = [f for f in listdir(path)]
    
    #test_list = 
    #test_list = [['d1fic1','d1fic2'],['d2fic1'], ['d3fic1','d3fic2']]
    return render(request, 'nextcloud/nextcloud_home.html', locals())