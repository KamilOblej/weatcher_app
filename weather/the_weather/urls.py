from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('details/<city_name>/', views.details, name='details'),
    path('get_back/', views.get_back, name='get_back'),
]
