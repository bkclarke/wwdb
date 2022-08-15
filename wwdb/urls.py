# wwdb/urls.py
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    #path('', views.index, name='index'),
    #path('wire/<int:wire_id>/', views.wire, name='wire'),
    #path('wirelist/', views.wirelist, name='wirelist'),
    #path('startcast/', views.startcast, name='startcast'),
    #path('endcast/', views.endcast, name='endcast'),
    #path('castcomplete/', views.castcomplete, name='castcomplete'),
    path('home/', views.home, name='home'),
    path('castlist/', CastList.as_view(), name='castlist'),
    path('cast/<int:pk>/', CastDetail.as_view(), name='castdetail'),
    path('cast/<int:pk>/endcastdetail', EndCastDetail.as_view(), name='endcastdetail'),
    path('startcast/', StartCast.as_view(), name='startcast'),
    path('cast/<int:pk>/edit/', EditCast.as_view(), name='editcast'),
    path('cast/<int:pk>/delete/', DeleteCast.as_view(), name='deletecast'),
    path('cast/<int:pk>/endcast/', EndCast.as_view(), name='endcast'),
    path('usersettings/', UserSettings.as_view(), name='usersettings'),
    path('adduser/', AddUser.as_view(), name='adduser'),
    path('user/<int:pk>/', UserDetail.as_view(), name='userdetail'),
]