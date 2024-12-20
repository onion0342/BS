from django.urls import path
from api.views import email_confirm, register_user, login

urlpatterns = [
    path('email/confirm/', email_confirm, name='email_confirm'),
    path('user/add/', register_user, name='register_user'),
    path('user/login/', login, name='login'),
]