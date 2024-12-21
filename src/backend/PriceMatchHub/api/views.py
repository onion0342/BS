import random
import string
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from scripts.taobao import get_product
from django.core.mail import send_mail
from django.conf import settings

from api.models import Product, Platform, PriceHistory, EmailCode, BasicUser

def add_product(data):
    try:
        product_name = data['product_name']
        platform = Platform.objects.get(platform_name=data['platform'])
        deal = data['deal']
        shop_name = data['shop_name']
        location = data['location']
        text = 'none'
        img = data['img']
        web = data['web']
        is_valid = True

        new_product = Product.objects.create(
            product_name=product_name,
            platform=platform,
            deal=deal,
            shop_name=shop_name,
            location=location,
            text=text,
            img=img,
            web=web,
            is_valid=is_valid
        )

        return new_product.product_id
    except Exception as e:
        print(str(e))
        return -1
    
def add_platform(platform_name):
    try:
        new_platform = Platform.objects.create(
            platform_name=platform_name
        )

        return new_platform.platform_id
    except Exception as e:
        print(str(e))
        return -1

def add_priceHistory(data):
    try:
        product = Product.objects.get(product_id=data['product'])
        price = data['price']

        now = datetime.now()
        date_formatted = now.strftime('%Y-%m-%d')
        time_formatted = now.strftime('%H:%M:%S.%f')[:12]

        new_priceHistory = PriceHistory.objects.create(
            product=product,
            price=price,
            update_date=date_formatted,
            update_time=time_formatted
        )

        return new_priceHistory.price_history_id
    except Exception as e:
        print(str(e))
        return -1

@csrf_exempt
def get_product_data_taobao(request):
    response = {}
    try:
        payload = {}

        response['payload'] = payload
        response['code'] = 0
        response['err'] = ""
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def get_product_data_jingdong(request):
    response = {}
    try:
        payload = {}

        response['payload'] = payload
        response['code'] = 0
        response['err'] = ""
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def email_confirm(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            email = body_data.get('email')

            if not email:
                response['code'] = 1
                response['err'] = '邮箱错误'
            else:
                code = ''.join(random.choices(string.digits, k=6))
                _datetime = datetime.now()
                EmailCode.objects.create(
                    email=email,
                    code=code,
                    datetime=_datetime
                )
                verification_code = code
                
                subject = 'PriceMatchHub 验证码'
                message = f'你的验证码: {verification_code}'
                from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(subject, message, from_email, [email], fail_silently=False)
                
                response['code'] = 0
                response['msg'] = '验证码已发送'
        else:
            response['code'] = 1
            response['err'] = '非法请求，请重试'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

def user_exists(user_name, email, phone):
    try:
        BasicUser.objects.get(user_name=user_name)
        return 1
    except ObjectDoesNotExist:
        pass
 
    try:
        BasicUser.objects.get(email=email)
        return 2
    except ObjectDoesNotExist:
        pass
 
    try:
        BasicUser.objects.get(phone=phone)
        return 3
    except ObjectDoesNotExist:
        pass
 
    return 0

@csrf_exempt
def register_user(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            email = body_data.get('email')
            code = body_data.get('code')
            _datetime = datetime.now()

            try:
                email_code = EmailCode.objects.filter(
                    email=email,
                    datetime__gte=_datetime - timedelta(minutes=5)
                ).order_by('-datetime').first()
            except ObjectDoesNotExist:
                email_code = None

            if email_code == None:
                response['code'] = 1
                response['err'] = '验证码未发送或已过期，请重试'
            elif email_code.code != code:
                response['code'] = 1
                response['err'] = '验证码错误'
            else:
                user_name = body_data.get('user_name')
                phone = body_data.get('phone')
                pwd_hash = body_data.get('pwd_hash')
                check = user_exists(user_name=user_name, email=email, phone=phone)
                if check == 1:
                    response['code'] = 1
                    response['err'] = '该用户名已被注册'
                elif check == 2:
                    response['code'] = 1
                    response['err'] = '该邮箱已被注册'
                elif check == 3:
                    response['code'] = 1
                    response['err'] = '该手机号已被注册'
                else:
                    BasicUser.objects.create(
                        user_name=user_name,
                        phone=phone,
                        pwd_hash=pwd_hash,
                        email=email
                    )
                    response['code'] = 0
                    response['msg'] = '注册成功'
        else:
            response['code'] = 1
            response['err'] = '非法请求，请重试'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def login(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            account = body_data.get('account')
            pwd_hash = body_data.get('pwd_hash')

            try:
                user = BasicUser.objects.get(user_name=account)

                if pwd_hash == user.pwd_hash:
                    payload = {}
                    payload['user_id'] = user.basic_user_id

                    response['code'] = 0
                    response['msg'] = '登陆成功'
                    response['payload'] = payload
                else:
                    response['code'] = 1
                    response['err'] = '用户名或密码错误'
            except ObjectDoesNotExist:
                user = None
                response['code'] = 1
                response['err'] = '用户名不存在'
        else:
            response['code'] = 1
            response['err'] = '非法请求，请重试'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def get_user_detail(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')

            try:
                user = BasicUser.objects.get(basic_user_id=user_id)

                payload = {}
                payload['user_name'] = user.user_name
                payload['phone'] = user.phone
                payload['email'] = user.email

                payload['taobao_account'] = user.taobao_account
                if payload['taobao_account'] == None:
                    payload['taobao_account'] = '-'

                payload['taobao_password'] = user.taobao_password
                if payload['taobao_password'] == None:
                    payload['taobao_password'] = '-'

                payload['jingdong_account'] = user.jingdong_account
                if payload['jingdong_account'] == None:
                    payload['jingdong_account'] = '-'

                payload['jingdong_password'] = user.jingdong_password
                if payload['jingdong_password'] == None:
                    payload['jingdong_password'] = '-'

                response['code'] = 0
                response['msg'] = '返回成功'
                response['payload'] = payload
            except ObjectDoesNotExist:
                user = None
                response['code'] = 1
                response['err'] = '用户不存在'
        else:
            response['code'] = 1
            response['err'] = '非法请求，请重试'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)