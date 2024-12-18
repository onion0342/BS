import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PriceMatchHub.settings')

def configure_django():
    django.setup()
    print("Django Setup Successfully.")
    
def clear_database():
    from api.models import Platform
    Platform.objects.all().delete()
    print("Platforms in Database are deleted.")

def add_platform(name):
    from api.views import add_platform
    platform_id = add_platform(name)
    return platform_id

if __name__ == '__main__':
    configure_django()
    clear_database()
    add_platform('淘宝')
    add_platform('天猫')
    add_platform('京东')
    add_platform('拼多多')
    print("Platform Database Initialized Successfully.")