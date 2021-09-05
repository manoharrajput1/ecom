from django.contrib import admin
from django.db import models
from .models import Order, Product, OrderItem, ShippingAddress
# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)