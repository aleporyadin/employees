from django.urls import path
from list.views import *

urlpatterns = [
    path('employee-list/', employee_list, name='employee-list'),
    path('employee-list/search/', search_employees, name='search_employees'),
    path('get-employee/', get_employee, name='get_employee'),
    path('employee-list/update-employee/', update_employee, name='update-employee'),
    path('employee-list/delete-employee/', delete_employee, name='delete-employee'),
    path('employees-list-without-selected/', employees_list_without_selected, name='employees_list_without_selected'),
    path('load-more-managers/', load_more_managers, name='load-more-managers'),
]
