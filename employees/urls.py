from django.contrib import admin
from django.urls import path

from hierarchy.views import employees_vertical, employees_horizontal, load_children, index, change_manager
from authentication.views import *
from list.views import employee_list, search_employees

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('hierarchy/vertical/', employees_vertical, name='vertical'),
    path('hierarchy/horizontal/', employees_horizontal, name='horizontal'),
    path('employee_list/', employee_list, name='employee_list'),
    path('employee_list/search/', search_employees, name='search_employees'),
    path('change-manager/', change_manager, name='change_manager'),

    path('load-children/', load_children, name='load_children'),
    path('register/', sign_up, name="register"),
    path('login/', sign_in, name="login"),
    path('logout/', sign_out, name="logout"),
    path('profile/', profile, name="profile"),
]
