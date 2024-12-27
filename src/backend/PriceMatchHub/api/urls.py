from django.urls import path
from api.views import email_confirm, register_user, login
from api.views import get_user_detail, user_pwd_change
from api.views import user_email_change, user_phone_change
from api.views import user_weipinhui_change, user_jingdong_change
from api.views import get_products, sub_product
from api.views import cancelsub_product, get_qrcode_cookie
from api.views import check_login, get_product_data_jingdong
from api.views import get_product_data_weipinhui

urlpatterns = [
    path('email/confirm/', email_confirm, name='email_confirm'),
    path('user/add/', register_user, name='register_user'),
    path('user/login/', login, name='login'),
    path('user/get/', get_user_detail, name='get_user_detail'),
    path('user/password/change', user_pwd_change, name='user_pwd_change'),
    path('user/email/change', user_email_change, name='user_email_change'),
    path('user/phone/change', user_phone_change, name='user_phone_change'),
    path('user/weipinhui/set', user_weipinhui_change, name='user_weipinhui_change'),
    path('user/jingdong/set', user_jingdong_change, name='user_jingdong_change'),
    path('get/products', get_products, name='get_products'),
    path('sub/product', sub_product, name='sub_product'),
    path('cancelsub/product', cancelsub_product, name='cancelsub_product'),
    path('get/qrcode_cookie', get_qrcode_cookie, name='get_qrcode_cookie'),
    path('check/logged', check_login, name='check_login'),
    path('get/jingdong', get_product_data_jingdong, name='get_product_data_jingdong'),
    path('get/weipinhui', get_product_data_weipinhui, name='get_product_data_weipinhui'),
]