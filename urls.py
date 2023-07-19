from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('', include('hierarchy.urls')),
    path('', include('authentication.urls')),
    path('', include('list.urls')),
]
