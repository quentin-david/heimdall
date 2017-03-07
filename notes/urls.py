from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Notes
    url(r'^$', views.NotesList.as_view(), name='notes_list'),
    url(r'new/$', views.notesCreate, name='notes_create'),
    url(r'(?P<notes_id>\d+)/edit$', views.notesCreate, name='notes_update'),
    url(r'^(?P<pk>\d+)/delete$', views.NotesDelete.as_view(), name='notes_delete'),
    # NotesFile
    url(r'^file/(?P<notes_file_id>\d+)/delete', views.notesFileDelete, name='notes_file_delete'),
    # Categories
    url(r'category$', views.categoryList, name='category_list'),
    url(r'category/(?P<pk>\d+)/delete$', views.CategoryDelete.as_view(), name='category_delete'),
    # Bookmarks
    url(r'bookmark$', views.bookmarkList, name='bookmark_list'),
    url(r'bookmark/(?P<bookmark_id>\d+)/delete$', views.bookmarkDelete, name='bookmark_delete'),
    # Topic
    url(r'topic/(?P<category_id>\d+)/view$', views.topicView, name='topic_view'),
]