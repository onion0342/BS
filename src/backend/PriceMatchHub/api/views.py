from django.shortcuts import render
from api.models import Product

def add_product(data):
    new_product = Product()

    return new_product.product_id