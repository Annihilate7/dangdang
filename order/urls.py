from django.urls import path
from order import views


app_name = 'order'

urlpatterns=[
    path('indent/', views.indent, name = "indent"),
    path('add_address/', views.add_address, name = "add_address"),
    path('choce/', views.choce, name = "choce"),
    path('return_car/', views.return_car, name = "return_car"),
    path('indent_ok/', views.indent_ok, name = "indent_ok")
]