from django.urls import path
from car import views


app_name = 'car'

urlpatterns = [
    path('car/', views.car, name = 'car'),
    path('add_car/', views.add_car, name = 'add_car'),
    path('del_car/', views.del_car, name = 'del_car'),
]