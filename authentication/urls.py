from django.urls import path

from authentication.views import *

urlpatterns = [
    path('register/', sign_up, name="register"),
    path('login/', sign_in, name="login"),
    path('logout/', sign_out, name="logout"),
    path('profile/', profile, name="profile"),
]
