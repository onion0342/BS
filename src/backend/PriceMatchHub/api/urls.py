from django.urls import path
from api.views import email_confirm

urlpatterns = [
    path('email/confirm/', email_confirm, name='email_confirm'),
]