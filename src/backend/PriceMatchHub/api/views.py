import random
import string
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from api.models import Product, Platform, PriceHistory, EmailCode, BasicUser, SubProduct, Cookies

from scripts.web_init import get_avoid_check_web
from scripts.jingdong import web_check as jingdong_web_check
from scripts.jingdong import jd_search
from scripts.weipinghui import web_check as weipinhui_web_check
from scripts.weipinghui import vph_search

jingdong_webs = {}
weipinhui_webs = {}
    
def add_platform(platform_name):
    try:
        new_platform = Platform.objects.create(
            platform_name=platform_name
        )

        return new_platform.platform_id
    except Exception as e:
        print(str(e))
        return -1

@csrf_exempt
def check_login(request):
    response = {}
    body_data = json.loads(request.body)
    method = body_data.get('method')
    user_id = body_data.get('user_id')
    
    if request.method == 'POST':
        if method == 'check':
            response['jd'] = True
            user = BasicUser.objects.get(basic_user_id=user_id)
            try:
                jd_cookie = Cookies.objects.get(user=user, platform__platform_name='京东')
                if timezone.now() - jd_cookie.datetime > timedelta(days=1):
                    Cookies.objects.filter(user=user, platform__platform_name='京东').delete()
                    raise Cookies.DoesNotExist
            except Cookies.DoesNotExist:
                response['jd'] = False
            
            response['vph'] = True
            try:
                vph_cookie = Cookies.objects.get(user=user, platform__platform_name='唯品会')
                if timezone.now() - vph_cookie.datetime > timedelta(days=1):
                    Cookies.objects.filter(user_id=user, platform__platform_name='唯品会').delete()
                    raise Cookies.DoesNotExist
            except Cookies.DoesNotExist:
                response['vph'] = False

            response['code'] = 0
            response['msg'] = '检查成功'
            
            return JsonResponse(response)
        else:
            return JsonResponse({'error': '非法请求'})

@csrf_exempt
def get_qrcode_cookie(request):
    response = {}
    try:
        body_data = json.loads(request.body)
        platform = body_data.get('platform')
        user_id = body_data.get('user_id')
        payload = {}
        if platform == '京东':
            if user_id not in jingdong_webs:
                web = get_avoid_check_web()
                web.get('https://passport.jd.com/new/login.aspx')
                res = jingdong_web_check(web)
            else:
                res = jingdong_web_check(jingdong_webs[user_id])

            if res[0] == "logged":
                Cookies.objects.create(
                    platform=Platform.objects.get(platform_name=platform),
                    user=BasicUser.objects.get(basic_user_id=user_id),
                    cookie=json.dumps(res[1]),
                )
                response['code'] = 2
                response['msg'] = '扫码成功'
            elif res[0] == 'not logged':
                jingdong_webs[user_id] = res[1]
                payload['qrcode'] = res[2]
                response['payload'] = payload
                response['code'] = 0
                response['msg'] = '二维码获取成功'
        elif platform == '唯品会':
            if user_id not in weipinhui_webs:
                web = get_avoid_check_web()
                web.get('https://passport.vip.com/login')
                res = weipinhui_web_check(web)
            else:
                res = weipinhui_web_check(weipinhui_webs[user_id])

            if res[0] == "logged":
                Cookies.objects.create(
                    platform=Platform.objects.get(platform_name=platform),
                    user=BasicUser.objects.get(basic_user_id=user_id),
                    cookie=json.dumps(res[1]),
                )
                response['code'] = 2
                response['msg'] = '扫码成功'
            elif res[0] == 'not logged':
                weipinhui_webs[user_id] = res[1]
                payload['qrcode'] = res[2]
                response['payload'] = payload
                response['code'] = 0
                response['msg'] = '二维码获取成功'
        else:
            response['code'] = 1
            response['err'] = '当前不支持该平台'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def get_product_data_weipinhui(request):
    response = {}
    try:
        body_data = json.loads(request.body)
        key = body_data.get('key')
        user_id = body_data.get('user_id')
        user = BasicUser.objects.get(basic_user_id=user_id)
        cookie = Cookies.objects.get(user=user, platform__platform_name='唯品会')
        cookies = json.loads(cookie.cookie)
        if user_id not in weipinhui_webs:
            web = get_avoid_check_web()
            web.get('https://www.vip.com/')
            for c in cookies:
                web.add_cookie(c)
            web.get(f'https://category.vip.com/suggest.php?keyword={key}&ff=235|12|1|1/')
        else:
            web = weipinhui_webs[user_id]
        
        vph_search(key, web)
        response['code'] = 0
        response['msg'] = "京东搜索成功"
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def get_product_data_jingdong(request):
    response = {}
    try:
        body_data = json.loads(request.body)
        key = body_data.get('key')
        user_id = body_data.get('user_id')
        user = BasicUser.objects.get(basic_user_id=user_id)
        cookie = Cookies.objects.get(user=user, platform__platform_name='京东')
        cookies = json.loads(cookie.cookie)
        if user_id not in jingdong_webs:
            web = get_avoid_check_web()
            web.get('https://www.jd.com/')
            for c in cookies:
                web.add_cookie(c)
        else:
            web = jingdong_webs[user_id]
        
        jd_search(key, web)
        response['code'] = 0
        response['msg'] = "京东搜索成功"
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def get_products(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            key = body_data.get('key')
            user_id = body_data.get('user_id')
            sub = body_data.get('sub')

            try:
                user = BasicUser.objects.get(basic_user_id=user_id)

                if sub == True:
                    products = Product.objects.filter(subproduct__user=user)
                else:
                    if key == "":
                        all_products = Product.objects.all()
                        cnt = all_products.count()
                        if cnt < 50:
                            products = all_products
                        else:
                            products = random.sample(list(all_products), 50)
                    else:
                        all_products = Product.objects.filter(product_name__icontains=key)
                        cnt = all_products.count()
                        if cnt < 50:
                            products = all_products
                        else:
                            products = random.sample(list(all_products), 50)

                payloads = []

                for product in products:
                    payload = {}
                    payload['id'] = product.product_id
                    payload['name'] = product.product_name
                    payload['salesVolume'] = product.deal
                    payload['storeName'] = product.shop_name
                    payload['storeLocation'] = product.location
                    payload['description'] = product.text
                    payload['imageUrl'] = product.img
                    payload['clickUrl'] = product.web
                    
                    latest_price_history = PriceHistory.objects.filter(product=product).order_by('-update_date', '-update_time').first()
                    payload['price'] = latest_price_history.price
                    payload['priceUpdateTime'] = latest_price_history.get_update_datetime_iso()

                    payload['platform'] = product.platform.platform_name

                    exists = SubProduct.objects.filter(product=product, user=user).exists()
                    if exists:
                        payload['is_sub'] = True
                    else:
                        payload['is_sub'] = False
                    
                    payloads.append(payload)
                
                response['payloads'] = payloads
                response['code'] = 0
                response['msg'] = '获取商品列表成功'
            except ObjectDoesNotExist:
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

                payload['weipinhui_account'] = user.weipinhui_account
                if payload['weipinhui_account'] == None:
                    payload['weipinhui_account'] = '-'

                payload['weipinhui_password'] = user.weipinhui_password
                if payload['weipinhui_password'] == None:
                    payload['weipinhui_password'] = '-'

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

@csrf_exempt
def user_pwd_change(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
            originPwdHash = body_data.get('originPwdHash')
            newPwdHash = body_data.get('newPwdHash')
            try:
                user = BasicUser.objects.get(basic_user_id=user_id)

                if user.pwd_hash == originPwdHash:
                    user.pwd_hash = newPwdHash
                    user.save()
                    response['code'] = 0
                    response['msg'] = '修改成功'
                else:
                    response['code'] = 1
                    response['err'] = '原密码错误'
                
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

@csrf_exempt
def user_email_change(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
            newEmail = body_data.get('newEmail')
            code = body_data.get('code')
            _datetime = datetime.now()
            try:
                user = BasicUser.objects.get(basic_user_id=user_id)

                try:
                    email_code = EmailCode.objects.filter(
                        email=newEmail,
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
                    user.email = newEmail
                    user.save()
                    response['code'] = 0
                    response['msg'] = '邮箱绑定成功'
                
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

@csrf_exempt
def user_phone_change(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
            newPhone = body_data.get('newPhone')
            try:
                user = BasicUser.objects.get(basic_user_id=user_id)

                user.phone = newPhone
                user.save()
                response['code'] = 0
                response['msg'] = '手机号绑定成功'
                
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

@csrf_exempt
def user_weipinhui_change(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
            account = body_data.get('account')
            password = body_data.get('password')
            try:
                user = BasicUser.objects.get(basic_user_id=user_id)

                user.weipinhui_account = account
                user.weipinhui_password = password
                user.save()
                response['code'] = 0
                response['msg'] = '绑定成功'
                
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

@csrf_exempt
def user_jingdong_change(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
            account = body_data.get('account')
            password = body_data.get('password')
            try:
                user = BasicUser.objects.get(basic_user_id=user_id)

                user.jingdong_account = account
                user.jingdong_password = password
                user.save()
                response['code'] = 0
                response['msg'] = '绑定成功'
                
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

@csrf_exempt
def sub_product(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
            product_id = body_data.get('product_id')

            exist_product = Product.objects.filter(product_id=product_id).exists()
            exist_user = BasicUser.objects.filter(basic_user_id=user_id).exists()

            if not exist_user:
                response['code'] = 1
                response['err'] = '用户不存在'
            elif not exist_product:
                response['code'] = 1
                response['err'] = '商品不存在'
            else:
                user = BasicUser.objects.get(basic_user_id=user_id)
                product = Product.objects.get(product_id=product_id)
                exist_sub = SubProduct.objects.filter(product=product, user=user).exists()
                if exist_sub:
                    response['code'] = 1
                    response['err'] = '商品已订阅'
                else:
                    SubProduct.objects.create(
                        product=product,
                        user=user
                    )
                    response['code'] = 0
                    response['msg'] = '成功订阅'
                
        else:
            response['code'] = 1
            response['err'] = '非法请求，请重试'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def cancelsub_product(request):
    response = {}
    try:
        if request.method == 'POST':
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
            product_id = body_data.get('product_id')

            exist_product = Product.objects.filter(product_id=product_id).exists()
            exist_user = BasicUser.objects.filter(basic_user_id=user_id).exists()

            if not exist_user:
                response['code'] = 1
                response['err'] = '用户不存在'
            elif not exist_product:
                response['code'] = 1
                response['err'] = '商品不存在'
            else:
                user = BasicUser.objects.get(basic_user_id=user_id)
                product = Product.objects.get(product_id=product_id)
                exist_sub = SubProduct.objects.filter(product=product, user=user).exists()
                if not exist_sub:
                    response['code'] = 1
                    response['err'] = '商品未订阅'
                else:
                    sub = SubProduct.objects.get(product=product, user=user)
                    sub.delete()
                    response['code'] = 0
                    response['msg'] = '取消订阅'
                
        else:
            response['code'] = 1
            response['err'] = '非法请求，请重试'
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)