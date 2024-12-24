from django.db import models
from datetime import datetime, timedelta
import pytz

# Create your models here.
class BasicUser(models.Model):
    basic_user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, null=False, unique=True)
    phone = models.CharField(max_length=20, null=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    pwd_hash = models.CharField(max_length=64, null=False)
    taobao_account = models.CharField(max_length=100, null=True)
    taobao_password = models.CharField(max_length=100, null=True)
    jingdong_account = models.CharField(max_length=100, null=True)
    jingdong_password = models.CharField(max_length=100, null=True)

class EmailCode(models.Model):
    email_code_id = models.AutoField(primary_key=True)
    email = models.EmailField(null=False, unique=False)
    code = models.CharField(max_length=20, null=False)
    datetime = models.DateTimeField()

class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=50, null=False, unique=True)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200, null=False)
    platform = models.ForeignKey('api.Platform', on_delete=models.CASCADE)
    deal = models.CharField(max_length=200, null=False)
    shop_name = models.CharField(max_length=200, null=False)
    location = models.CharField(max_length=200, null=False)
    text = models.TextField()
    img = models.URLField(max_length=2000)
    web = models.URLField(max_length=2000)
    is_valid = models.BooleanField(default=True, null=False)

class PriceHistory(models.Model):
    price_history_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('api.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    update_date = models.DateField() # YYYY-MM-DD
    update_time = models.TimeField() # HH:MM[:ss[.uuuuuu]]

    def get_update_datetime_iso(self):
        utc_zone = pytz.UTC
        combined_datetime = datetime.combine(self.update_date, self.update_time, tzinfo=utc_zone)
        iso_format = combined_datetime.isoformat()
        return iso_format

class SubProduct(models.Model):
    sub_product_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('api.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('api.BasicUser', on_delete=models.CASCADE)
