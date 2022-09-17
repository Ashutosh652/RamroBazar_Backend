from django.contrib import admin
from .models import Category, Item, Brand, Media, SoldStatus, Comment


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Brand)
admin.site.register(SoldStatus)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Media)
admin.site.register(Comment)