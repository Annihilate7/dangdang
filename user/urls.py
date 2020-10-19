from django.urls import path
from user import views

app_name = 'user'


urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('captcha/', views.captcha, name = 'captcha'),
    path('login_logic/', views.login_logic, name = 'login_logic'),
    path('register/', views.register, name = 'register'),
    path('check_user/', views.check_user, name = 'check_user'),
    path('check_captcha/', views.check_captcha, name = 'check_captcha'),
    path('register_logic/', views.register_logic, name = 'register_logic'),
    path('register_ok/', views.register_ok, name = 'register_ok'),
    path('quit/', views.quit, name = 'quit'),
]