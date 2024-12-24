from django.urls import path
from api.views import email_confirm, register_user, login
from api.views import get_user_detail, user_pwd_change
from api.views import user_email_change, user_phone_change
from api.views import user_taobao_change, user_jingdong_change
from api.views import get_products

urlpatterns = [
    path('email/confirm/', email_confirm, name='email_confirm'),
    path('user/add/', register_user, name='register_user'),
    path('user/login/', login, name='login'),
    path('user/get/', get_user_detail, name='get_user_detail'),
    path('user/password/change', user_pwd_change, name='user_pwd_change'),
    path('user/email/change', user_email_change, name='user_email_change'),
    path('user/phone/change', user_phone_change, name='user_phone_change'),
    path('user/taobao/set', user_taobao_change, name='user_taobao_change'),
    path('user/jingdong/set', user_jingdong_change, name='user_jingdong_change'),
    path('get/products', get_products, name='get_products'),
]