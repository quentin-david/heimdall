from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from mapping.models import ServiceWebServer
from notes.forms import BookmarkForm
from notes.models import Category, Notes, NotesFile
from datetime import datetime, timedelta

def home(request):
    service_list = ServiceWebServer.objects.all()
    root_category_list = Category.objects.filter(parent__isnull=True)
    recent_notes_list = Notes.objects.filter(date_update__gte=(datetime.today() - timedelta(days=3))) #Last 3 day topics
    bookmark_form = BookmarkForm(None)

    return render(request, 'appli/home.html', locals())

def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'appli/profile.html', locals())

def statistics(request):
    user_list = User.objects.all()
    note_list = Notes.objects.all()
    file_list = NotesFile.objects.all()
    return render(request, 'about/statistics.html', locals())