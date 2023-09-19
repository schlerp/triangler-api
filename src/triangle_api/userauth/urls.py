from django.urls import path

from .views import csrf
from .views import login_user
from .views import logout_user

urlpatterns = [
    path("csrf/", csrf, name="csrf"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]
