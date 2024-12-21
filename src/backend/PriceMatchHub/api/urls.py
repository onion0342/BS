from django.urls import path
from api.views import email_confirm, register_user, login
from api.views import get_user_detail

urlpatterns = [
    path('email/confirm/', email_confirm, name='email_confirm'),
    path('user/add/', register_user, name='register_user'),
    path('user/login/', login, name='login'),
    path('user/get/', get_user_detail, name='get_user_detail'),
]