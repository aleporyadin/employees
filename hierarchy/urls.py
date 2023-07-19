from django.urls import path

from hierarchy.views import employees_vertical, employees_horizontal, load_children, change_manager


urlpatterns = [
    path('hierarchy/vertical/', employees_vertical, name='vertical'),
    path('hierarchy/horizontal/', employees_horizontal, name='horizontal'),
    path('change-manager/', change_manager, name='change_manager'),
    path('load-children/', load_children, name='load_children'),
]
