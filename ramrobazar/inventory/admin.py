from django.contrib import admin
from .models import Category, Product, Service, ProductOrService, Brand, Media, SoldStatus, Comment



admin.site.register(Product)
admin.site.register(ProductOrService)
admin.site.register(Service)
admin.site.register(Brand)
admin.site.register(SoldStatus)
admin.site.register(Category)
admin.site.register(Media)
admin.site.register(Comment)