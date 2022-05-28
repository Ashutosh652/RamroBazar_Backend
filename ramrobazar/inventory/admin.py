from django.contrib import admin
from .models import Category, Product, Service, Brand, Media, ProductSoldStatus, ServiceSoldStatus, Comment



admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Brand)
admin.site.register(ProductSoldStatus)
admin.site.register(ServiceSoldStatus)
admin.site.register(Category)
admin.site.register(Media)
admin.site.register(Comment)