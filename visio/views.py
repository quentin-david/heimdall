from django.shortcuts import render
from django.http import HttpResponse
import concurrent.futures
import requests

def visioHome(request):
    return render(request, 'visio_home.html', locals())


def visioVideo(request):
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        url = 'http://82.66.210.9:20000/html/cam_pic_new.php'
        cmd = executor.submit(requests.get, url,verify=False,stream=True)
        try:
            data = cmd.result()
        except Exception as exc:
            return False
        else:
            if str(data.status_code) == '404':
                return False
            else:
                return HttpResponse(data.raw,content_type="image/png")
    """
    url = 'http://82.66.210.9:20000/html/cam_pic_new.php?time=1496581866996&pDelay=40000'
    return HttpResponse(requests.get(url,verify=False,stream=True),content_type="image/png")
    #return HttpResponse(requests.get(url,verify=False,stream=True))