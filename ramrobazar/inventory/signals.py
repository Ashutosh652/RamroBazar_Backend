# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Item, Product, Service, Brand


# # if ProductOrService.is_product:
# @receiver(post_save, sender=ProductOrService)
# def create_product_or_service(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_product:
#             Product.objects.create(product_or_service=instance, show_price=0, brand=Brand.objects.get(name='None'))
#         if not instance.is_product:
#             Service.objects.create(product_or_service=instance)

# @receiver(post_save, sender=ProductOrService)
# def save_product_or_service(sender, instance, **kwargs):
#     if instance.is_product:
#         instance.product.save()
#     if not instance.is_product:
#         instance.service.save()

# if not ProductOrService.is_product:
# @receiver(post_save, sender=ProductOrService)
# def create_service(sender, instance, created, **kwargs):
#     if created:
#         Service.objects.create(product_or_service=instance)

# @receiver(post_save, sender=ProductOrService)
# def save_service(sender, instance, **kwargs):
#     instance.service.save()