import random
import string
import json
from django.shortcuts import render
from api.models import Product, Platform, PriceHistory
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from scripts.taobao import get_product
from django.core.mail import send_mail
from django.conf import settings

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
    response = {'code': 0, 'err': ''}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            email = body_data.get('email')
            print(email)
            if not email:
                response['code'] = 1
                response['err'] = '邮箱错误'
            else:

                verification_code = ''.join(random.choices(string.digits, k=6))
                
                subject = 'PriceMatchHub 验证码'
                message = f'你的验证码: {verification_code}'
                from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(subject, message, from_email, [email], fail_silently=False)
                
                response['code'] = 0
                response['msg'] = 'Verification code sent successfully.'
        else:
            response['code'] = 1
            response['err'] = '非法请求，请重试'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)