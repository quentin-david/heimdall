from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from mapping.models import ServiceWebServer, Application
from notes.forms import BookmarkForm, CommunityForm
from notes.models import Category, Notes, NotesFile, Community, CommunityUsers
from datetime import datetime, timedelta
from django.db.models import Q

def home(request):
    service_list = ServiceWebServer.objects.order_by('name')
    application_list = Application.objects.all()
    #communities = Community.objects.filter((Q(community_users=request.user) & Q(communityusers__user_visa=True)) | Q(owner=request.user)).distinct()
    community_list = Community.get_communities_by_user(request.user)
    recent_notes_list = Notes.objects.filter(date_update__gte=(datetime.today() - timedelta(days=3))) #Last 3 day topics
    bookmark_form = BookmarkForm(None, user=request.user)

    return render(request, 'appli/home.html', locals())


def profile(request):
    user = User.objects.get(username=request.user.username)
    community_list = Community.get_communities_by_user(request.user)
    personal_communities = user.community_set.all()
    my_communities = CommunityUsers.objects.filter(user=request.user)
    form = CommunityForm(None)
    return render(request, 'profile/profile.html', locals())


def statistics(request):
    user_list = User.objects.all()
    note_list = Notes.objects.all()
    file_list = NotesFile.objects.all()
    return render(request, 'about/statistics.html', locals())