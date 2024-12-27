from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from api.models import Product, Platform, PriceHistory, EmailCode, BasicUser, SubProduct, Cookies
from django.conf import settings
from django.core.mail import send_mail
import os

def draw_num(str_data):
    num_filter = filter(str.isdigit, str_data)
    num_list = list(num_filter)
    num_str = "".join(num_list)
    return num_str

def get_avoid_check_web():
    chrome_options = Options()
    # 必要的 Chrome 选项
    chrome_options.add_argument('--headless')  # 启用无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.binary_location = '/usr/bin/chromium'

    # 添加日志输出
    print("Starting Chrome with options:", chrome_options.arguments)
    
    try:
        driver = webdriver.Chrome(
            executable_path='/usr/bin/chromedriver',
            #executable_path='./scripts/chromedriver.exe',
            chrome_options=chrome_options
        )
        print("Chrome started successfully")
        return driver
    except Exception as e:
        print(f"Error starting Chrome: {str(e)}")
        raise

def add_price_history(price, product_id):
    product = Product.objects.get(product_id=product_id)
    now = datetime.now()
    date_formatted = now.strftime('%Y-%m-%d')
    time_formatted = now.strftime('%H:%M:%S.%f')[:12]
 
    new_priceHistory = PriceHistory.objects.create(
        product=product,
        price=price,
        update_date=date_formatted,
        update_time=time_formatted
    )

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
        price = data['price']
        is_valid = True

        product = Product.objects.filter(
            product_name=product_name,
            shop_name=shop_name,
            platform=platform
        ).first()

        if product:

            latest_price_history = PriceHistory.objects.filter(product=product).order_by('-update_date', '-update_time').first()
            o_price = latest_price_history.price
            if o_price > price:
                for user in BasicUser.objects.all():
                    exist_sub = SubProduct.objects.filter(product=product, user=user).exists()
                    if exist_sub:
                        subject = 'PriceMatchHub'
                        message = f'您订阅的商品{product.product_name}，现有更优惠价格'
                        from_email = settings.DEFAULT_FROM_EMAIL
                        send_mail(subject, message, from_email, [user.email], fail_silently=False)

            add_price_history(product_id=product.product_id, price=price)
            return product.product_id
        else:
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
            add_price_history(product_id=new_product.product_id, price=price)

            return new_product.product_id
    except Exception as e:
        print(str(e))
        return -1