from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, SoldStatus


@receiver(post_save, sender=Item)
def create_sold_status(sender, instance, created, **kwargs):
    if created:
        SoldStatus.objects.create(item=instance, sold_price=0)

@receiver(post_save, sender=Item)
def save_item(sender, instance, **kwargs):
    instance.sold_status.save()
