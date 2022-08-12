# accounts/urls.py

from django.urls import include, path
from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]