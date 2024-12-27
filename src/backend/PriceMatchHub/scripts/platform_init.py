import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PriceMatchHub.settings')

def configure_django():
    django.setup()
    print("Django Setup Successfully.")
    
def clear_database():
    from api.models import Platform, BasicUser
    BasicUser.objects.all().delete()
    Platform.objects.all().delete()
    print("Platforms in Database are deleted.")
    add_platform('淘宝')
    add_platform('天猫')
    add_platform('京东')
    add_platform('拼多多')
    add_platform('唯品会')
    from scripts.web_init import add_product
    data = {}
    data['product_name'] = '订阅测试'
    data['platform'] = '淘宝'
    data['deal'] = 'none'
    data['shop_name'] = 'none'
    data['location'] = 'none'
    data['img'] = 'https://img.alicdn.com/imgextra/i1/2217006857331/O1CN01q7ziIc241eSkqZjsM_!!2217006857331.jpg_.webp'
    data['web'] = ''
    data['price'] = 100
    add_product(data=data)

def add_platform(name):
    from api.views import add_platform
    platform_id = add_platform(name)
    return platform_id

if __name__ == '__main__':
    configure_django()
    clear_database()
    print("Platform Database Initialized Successfully.")