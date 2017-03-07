from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mapping.models import ServiceWebServer
from notes.forms import BookmarkForm
from notes.models import Category

def home(request):
    service_list = ServiceWebServer.objects.all()
    root_category_list = Category.objects.filter(parent__isnull=True)
    form = BookmarkForm(request.POST or None)
    if form.is_valid():
        bookmark = form.save(commit=False)
        bookmark.owner = request.user
        bookmark.save()
        return redirect('home')
    return render(request, 'appli/home.html', locals())

def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'appli/profile.html', locals())