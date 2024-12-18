import time
from DrissionPage import ChromiumPage, ChromiumOptions
import re
import json
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PriceMatchHub.settings')

def configure_django():
    django.setup()
    print("Django Setup Successfully.")

def clear_database():
    from api.models import Product, PriceHistory
    Product.objects.all().delete()
    PriceHistory.objects.all().delete()
    print("Products in Database are deleted.")

def get_product(keyword, account, password):
    from api.views import add_product, add_priceHistory
    co = ChromiumOptions().headless(on_off=False)
    # co.set_argument('--headless=new')
    # co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    # co.add_argument("--proxy-server=http://{}".format(proxy_address))
    # co.set_argument('--disable-extensions')
    # co.set_argument('--disable-blink-features=AutomationControlled')
    # co.set_argument('--no-sandbox')
    # co.set_argument('--disable-dev-shm-usage')
    # co.set_argument('--disable-gpu')
    # co.set_argument('--start-maximized')
    cp = ChromiumPage(co)
    # cp = ChromiumPage()

    cp.get('https://login.taobao.com/member/login.jhtml')
    
    cp.ele('css:#fm-login-id').clear()
    cp.ele('css:#fm-login-id').input(account)
    cp.ele('css:#fm-login-password').input(password)
    cp.ele('css:.fm-button.fm-submit.password-login').click()

    cp.ele('css:#q').input(keyword)
    cp.ele('css:.btn-search').click()

    cp.listen.start('h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0')
    # time.sleep(10)
    data_packets = cp.listen.wait(count=2, timeout=20)

    bodys = []

    if isinstance(data_packets, bool):
        print('error')
        return
    
    for data_packet in data_packets:
        bodys.append(str(data_packet.response.body))
    # print(str(bodys[1])[:1000])

    for matching_body in bodys:
        # print(matching_body[:1000])
        l = re.findall(r' mtopjsonp\d+\((.*)\)', matching_body)
        
        if(len(l) == 0):
            continue
        # print(l[:1000])
        string = l[0]
        mtop_data = json.loads(string)

        items_array = mtop_data['data']['itemsArray']
        print(len(items_array))
        for item in items_array:
            # print(item)
            data = {}
            data['product_name'] = item['title']
            data['platform'] = '淘宝'
            data['deal'] = item['realSales']
            data['shop_name'] = item['nick']
            data['location'] = item['procity']
            data['img'] = item['pic_path']
            data['web'] = item['auctionURL']
            product_id = add_product(data=data)
            if product_id == -1:
                print(data)
                break
            # print(data)

            data = {}
            data['product'] = product_id
            data['price'] = item['price']
            priceHistory_id = add_priceHistory(data=data)
            if priceHistory_id == -1:
                print(data)
                break
            # print(data)
        # print(items_array)

    cp.quit()
if __name__ == '__main__':
    configure_django()
    # clear_database()
    # get_product('键盘')
    # get_product('鼠标')