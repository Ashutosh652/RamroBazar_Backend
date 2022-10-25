from django.contrib import admin
from .models import Category, Item, ItemSpecification, Brand, Media, SoldStatus, Comment


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
        "slug",
    )


class ItemSpecificationAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "id",
        "key",
        "value",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
    )


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemSpecification, ItemSpecificationAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(SoldStatus)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Media)
admin.site.register(Comment)
