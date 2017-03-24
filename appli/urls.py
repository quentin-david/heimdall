from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', login_required(views.home), name='home'),
    url(r'^accounts/login', auth_views.login, {'template_name': 'auth/connexion.html'}, name='login'),
    url(r'^accounts/profile/$', login_required(views.profile), name='profile'),
    url(r'^accounts/logout$', auth_views.logout, {'next_page': 'home'},name='logout'),
    
    url(r'^about/statistics$', login_required(views.statistics), name='statistics'),
]