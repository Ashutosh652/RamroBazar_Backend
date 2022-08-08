from django.contrib import admin
from .models import Category, Item, Brand, Media, SoldStatus, Comment


admin.site.register(Item)
admin.site.register(Brand)
admin.site.register(SoldStatus)
admin.site.register(Category)
admin.site.register(Media)
admin.site.register(Comment)